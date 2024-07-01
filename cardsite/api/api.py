import json

from django.apps import AppConfig
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import HttpResponse, redirect
from django.template import loader
from django.utils.translation import gettext_lazy as text

from decks.models import Card, Deck
from inventory.models import StorageLocale
from cardstash.models import CardAllocation, CardStash

def api_error( reason ):
    return HttpResponseBadRequest('Malformed request: '+reason)

def access_requires_auth( func ):
    def check_auth( request, *args, **kwargs ):
        if not request.user.is_authenticated:
            print('Not authorized!')
            return redirect('/login')
        return func( request, *args, **kwargs )
    return check_auth


def index( request ):
    """Entry point for the api.

    Actions:
        countDeckCard: see __count

    Args:
        request (django.http.HttpRequest): The API request

    Returns:
        django.http.HttpResponse
    """
    try:
        action = request.GET['action']
    except KeyError:
        return api_error('Did you state an action?')
    if action == 'countDeckCard':
        return __count( request )
    if action == 'update':
        return __update( request )
    if action == 'move':
        return __move( request )
    if action == 'getCardList':
        return __getCardList( request )
    if action == 'getBulkMoveTable':
        return __getBulkMoveTable( request )
    # Refuse to brew coffee with teapot
    return HttpResponse(
            status = 418
        )

def __count( request ):
    """Parse countDeckCard request and return answer

    Parameters:
        deck_uuid: The uuid of the deck you want a card count from.
        card_id: The id of the card you want the count of.

    Args:
        request (django.http.HttpRequest): The API request

    Returns:
        django.http.HttpResponse
    """

    stash_uuid = request.GET['deck_uuid']
    return get_n_card_in( request, stash_uuid )

def get_n_card_in( request, stash_uuid ):
    try:
        card_id = request.GET['card_id']
    except KeyError:
        return api_error('No card_id supplied')
    try:
        n_card_in_stash = CardAllocation.objects.get(
                stash_id = stash_uuid,
                card_id = card_id,
            ).n_card_in_stash
        return HttpResponse( n_card_in_stash )
    except ObjectDoesNotExist:
        return HttpResponse( 0 )

def __getCardList( request ):
    try:
        stash_uuid = request.GET['stash_uuid']
    except KeyError:
        return api_error('No stash_uuid supplied')
    return get_card_list( request, stash_uuid )

def get_card_list( request, stash_uuid ):
    calloc_list = CardAllocation.objects.filter(
            stash_id = stash_uuid,
        )
    response_data = []
    for entry in calloc_list:
        card = Card.objects.get( card_id = entry.card_id )
        data_row = {
                'card_name': card.card_name,
                'card_id': card.card_id,
                'quantity': entry.n_card_in_stash,
            }
        response_data.append(data_row)
    return JsonResponse( {'data':response_data} )

def __getBulkMoveTable( request ):
    try:
        from_uuid = request.GET['from_uuid']
        to_uuid = request.GET['to_uuid']
    except KeyError:
        return api_error('No stash_uuid supplied')
    return get_bulk_move_table( request, from_uuid, to_uuid )

def get_bulk_move_table( request, from_stash_uuid, to_stash_uuid ):
    def get_data_from_json( request, from_stash_uuid ):
        json_response = get_card_list( request, from_stash_uuid )
        return json.loads( json_response.content )['data']

    from_stash_data = get_data_from_json( request, from_stash_uuid )
    to_stash_data = get_data_from_json( request, to_stash_uuid )

    merged_data = {}
    for card in from_stash_data:
        entry = {
                'from_quantity': card['quantity'],
                'to_quantity': 0,
                'card_name': card['card_name'],
            }
        merged_data[card['card_id']] = entry
    for card in to_stash_data:
        if card['card_id'] in merged_data:
            merged_data[card['card_id']]['to_quantity'] = card['quantity']
            continue
        entry = {
                'from_quantity': 0,
                'to_quantity': card['quantity'],
                'card_name': card['card_name'],
            }
        merged_data[card['card_id']] = entry
    return JsonResponse(merged_data)

@access_requires_auth
def update_stash( request, stash_uuid ):
    try:
        stash_type = request.POST['stash_type']
    except KeyError:
        return api_error('No stash_type specified')
    if stash_type not in ['Deck','StorageLocale','CardStash']:
        return api_error('stash_type must be one of Deck, StorageLocal, or CardStash')
    stash_model = AppConfig.get_model(stash_type)
    stash_instance = stash_model.objects.get( stash_id = stash_uuid )
    try:
        update_data = request.POST['update_data']
    except KeyError:
        return api_error('No update_data provided')
    stash_instance.update( **update_data )
    return HttpResponse( status=204 )

@access_requires_auth
@transaction.atomic
def __update_calloc( request, quantity, stash_uuid, card_id ):
    try:
        Card.objects.get(card_id=card_id)
    except:
        set_, num = card_id.split('-')
        card_id = set_ + '-' + num.lstrip('0')
    if int(quantity) < 1:
        try:
            CardAllocation.objects.get(
                    stash_id=stash_uuid,
                    card_id=card_id
                ).delete()
            return HttpResponse( "Removed from deck" )
        except ObjectDoesNotExist:
            return HttpResponse( "Moot" )
    # JS should avoid POST if nothing changed to avoid pointless SQL
    obj, created = CardAllocation.objects.update_or_create(
            stash_id = stash_uuid,
            card_id = card_id,
            defaults = { "n_card_in_stash": quantity },
        )
    return (obj,created)

@access_requires_auth
@transaction.atomic
def update_from_decklist( request ):
    data = json.loads(request.body.decode("utf-8"))
    for row in data['update_data']:
        stash_uuid = data['uuid']
        card_id = row['card_id']
        qty = row['quantity']
        __update_calloc( request, qty, stash_uuid, card_id )
    return HttpResponse(status=204)

@access_requires_auth
@transaction.atomic
def update_from_tabular( request ):
    stash_map = {}
    data = json.loads(request.body.decode("utf-8"))
    for row in data['update_data']:
        if 'undefined' in row['card_id']:
            continue
        stash_name = row['stash_name']
        if stash_name not in stash_map:
            stash_result = CardStash.objects.filter(name=stash_name)
            if len(stash_result) == 0:
                stash_inst = StorageLocale.objects.create(name=stash_name,description='Automatically created on import.')
            else:
                stash_inst = stash_result[0]
            stash_map[stash_name] = stash_inst.uuid
        stash_uuid = stash_map[stash_name]
        card_id = row['card_id']
        qty = row['quantity']
        __update_calloc( request, qty, stash_uuid, card_id )
    return HttpResponse(status=204)

@access_requires_auth
@transaction.atomic
def move_cards_from_to( request ):
    def call_update( direction, data ):
        for row in data[ direction ]['update_data']:
            stash_uuid = data[ direction ]['uuid']
            card_id = row['card_id']
            n_card_in_stash = row['n_card_in_stash']
            __update_calloc( request, n_card_in_stash, stash_uuid, card_id )

    data = json.loads(request.body.decode("utf-8"))
    for direction in ['from_stash','to_stash']:
        call_update( direction, data )
    return HttpResponse(status=204)

