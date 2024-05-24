from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelform_factory
from django.shortcuts import HttpResponse
from django.template import loader
from django.utils.translation import gettext_lazy as text

from .models import Card, Deck
from cardstash.models import CardAllocation
import cardstash.views

def index( request ):
    return cardstash.views.index(
            request,
            Deck,
            "list_of_decks",
            "decks/index.html"
        )

def new_deck( request, error = None ):
    fields = [ "name", "game_format" ]
    labels = { "name": "Deck name" }
    return cardstash.views.new_stash(
            request,
            Deck,
            fields,
            labels,
        )

def create_deck_entry( request ):
    headers = [ 'name', 'game_format' ]
    return cardstash.views.create_stash_entry( 
            request,
            Deck,
            headers,
        )

def deck_details( request, deck_uuid ):
    deck_instance = Deck.objects.get( uuid = deck_uuid )
    template = loader.get_template( "decks/deck_details.html" )
    context = {
            'Deck': deck_instance
        }

    return HttpResponse( template.render( context, request ) )

def edit_deck( request, deck_uuid ):
    def format_query( deck_format ):
        match deck_format:
            case 'STD':
                return { 'standard_legal': True }
            case 'EXP':
                return { 'expanded_legal': True }
            case 'GLC':
                return { 'expanded_legal': True }
            case _:
                return { 'unlimited_legal': True }
    deck_instance = Deck.objects.get( uuid = deck_uuid )
    deck_format = deck_instance.game_format
    legal_cards = Card.objects.filter( **format_query( deck_format ) )
    deck_list = CardAllocation.objects.filter( stash_id = deck_instance.uuid )
    template = loader.get_template( "decks/edit_deck.html" )
    context = {
            'Deck': deck_instance,
            'card_list': legal_cards,
            'deck_list': deck_list,
            'post_url': 'update_calloc',
            'api_url': 'http://localhost:8000/decks/api',
        }
    return HttpResponse( template.render( context, request ) )

def update_calloc( request, deck_uuid ):
    print(request)
    try:
        card_id = request.POST['card_id']
        quantity = request.POST['quantity']
    except KeyError:
        return HttpResponse( "JavaScript didn't send expected POST data?" ) 
    if int(quantity) < 1:
        try:
            CardAllocation.objects.get(
                    stash_id=deck_uuid,
                    card_id=card_id
                ).delete()
            return HttpResponse( "Removed from deck" )
        except ObjectDoesNotExist:
            return HttpResponse( "Moot" )
    # JS should avoid POST if nothing changed to avoid pointless SQL
    obj, created = CardAllocation.objects.update_or_create(
            stash_id = deck_uuid,
            card_id = card_id,
            defaults = { "n_card_in_stash": quantity },
        )
    return HttpResponse( "Entry updated!" )
