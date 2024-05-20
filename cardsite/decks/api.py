from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponse
from django.template import loader
from django.utils.translation import gettext_lazy as text

from .models import Card, CardAllocation, Deck

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
        return HttpResponse( 
                reason_phrase = 'Malformed request: did you state an action?',
                status_code = 400,
            )
    if action == 'countDeckCard':
        return __count( request )
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
    try:
        return HttpResponse(
                CardAllocation.objects.get(
                    deck_id=request.GET['deck_uuid'],
                    card_id=request.GET['card_id']
                ).n_card_in_deck
            )
    except ObjectDoesNotExist:
        return HttpResponse( 0 )
