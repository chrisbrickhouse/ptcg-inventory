from django.apps import AppConfig
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponse
from django.template import loader
from django.utils.translation import gettext_lazy as text

from decks.models import Card, Deck
from cardstash.models import CardAllocation

def api_error( reason ):
    return HttpResponse(
            reason_phrase = 'Malformed request: '+reason,
            status_code = 400
        )

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
    # Refuse to brew coffee with teapot
    return HttpResponse(
            status_code = 418
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
    return HttpResponse( status_code = 200 )

def move_cards_from_to( request, from_stash_uuid, to_stash_uuid ):
    try:
        from_stash_instance = CardStash.objects.get( uuid = from_stash_uuid )
        to_stash_instance = CardStash.objects.get( uuid = to_stash_uuid )
    except ObjectDoesNotExist:
        return api_error('At least one of the stashes does not exist. Check the UUID.')
    try:
        # card_data is a dict where keys are card_id and values are quantity to move
        card_data = request.POST['card_data']
    except KeyError:
        return api_error('No card_data provided')
    card_id_list = card_data.keys()
    calloc_from_set = CardAllocation.objects.filter( 
            stash_id = from_stash_uuid 
        ).filter( 
                card_id__in=card_id_list
            )
    for calloc in calloc_from_set:
        calloc.update( 
                n_card_in_stash = F("n_card_in_stash") - card_data[calloc.card_id]
            )
    calloc_to_set = CardAllocation.objects.filter(
            stash_id = to_stash_uuid
        ).filter(
                card_id__in=card_id_list
            )
    for calloc in calloc_to_set:
        calloc.update(
                n_card_in_stash = F("n_card_in_stash") + card_data[calloc.card_id]
            )
    return HttpResponse( status_code = 200 )

