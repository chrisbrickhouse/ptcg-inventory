from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from django.shortcuts import HttpResponse
from django.template import loader
from django.utils.translation import gettext_lazy as text

from .models import Card, CardAllocation, Deck

def index( request ):
    list_of_decks = Deck.objects.order_by( "created" )
    template = loader.get_template( "decks/index.html" )
    context = {
            "list_of_decks": list_of_decks
        }
    return HttpResponse( template.render( context, request ) )

def new_deck( request, error = None ):
    template = loader.get_template( "decks/new_deck_form.html" )
    context = {
            "form": NewDeckForm().render( "decks/bootstrap_form_group_snippet.html" ),
        }
    return HttpResponse( template.render( context, request ) )

def create_deck_entry( request ):
    try:
        deck_name = request.POST['deck_name']
        game_format = request.POST['game_format']
    except KeyError:
        return new_deck( request )
    new_deck_entry = Deck.objects.create(
            deck_name = deck_name,
            game_format = game_format,
        )
    return HttpResponse( "Deck created" )

def deck_details( request, deck_uuid ):
    deck_instance = Deck.objects.get( deck_uuid = deck_uuid )
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
    deck_instance = Deck.objects.get( deck_uuid = deck_uuid )
    deck_format = deck_instance.game_format
    legal_cards = Card.objects.filter( **format_query( deck_format ) )
    deck_list = CardAllocation.objects.filter( deck_id = deck_instance.deck_uuid )
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
                    deck_id=deck_uuid,
                    card_id=card_id
                ).delete()
            return HttpResponse( "Removed from deck" )
        except ObjectDoesNotExist:
            return HttpResponse( "Moot" )
    # JS should avoid POST if nothing changed to avoid pointless SQL
    obj, created = CardAllocation.objects.update_or_create(
            deck_id = deck_uuid,
            card_id = card_id,
            defaults = { "n_card_in_deck": quantity },
        )
    return HttpResponse( "Entry updated!" )

class NewDeckForm(ModelForm):
    class Meta:
        model = Deck
        fields = [ "deck_name", "game_format" ]
        #exclude = ["deck_id", "created", "card_list"]
        labels = {
                "deck_name": "Deck name",
                "game_format": "Game format",
            }
        error_messages = {
                "deck_name": {
                    "max_length": "This deck name is too long."
                }
            }
