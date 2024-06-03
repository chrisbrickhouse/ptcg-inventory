from django.contrib.auth.decorators import login_required
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
    # Deprecated, should probably use API instead
    headers = [ 'name', 'game_format' ]
    return cardstash.views.create_stash_entry( 
            request,
            Deck,
            headers,
        )

def deck_details( request, deck_uuid ):
    deck_instance = Deck.objects.get( uuid = deck_uuid )
    return cardstash.views.stash_details(
            request,
            deck_instance,
            "decks/deck_details.html"
        )

@login_required
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
    deck_list = CardAllocation.objects.filter( stash_id = deck_uuid )
    template = loader.get_template( "cardstash/edit_stash.html" )
    context = {
            'Stash': deck_instance,
            'card_list': legal_cards,
            'stash_list': deck_list,
            'post_url': 'update_calloc',
            'api_url': '/api',
        }
    return HttpResponse( template.render( context, request ) )

def update_calloc( request, deck_uuid ):
    return cardstash.views.update_calloc( request, deck_uuid )
