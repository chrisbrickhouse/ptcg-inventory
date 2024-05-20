from datetime import datetime
import uuid

import django.contrib.postgres.fields as postgres_fields
from django.db import models
from django.db.models import Sum

def get_game_formats():
    """Mapping from format codes to human-readable names.
    """
    FORMATS = {
        'STD':'Standard',
        'EXP':'Expanded',
        'GLC':'Gym Leader Challenge',
        'UNL':'Unlimited'
    }
    return FORMATS

class Card( models.Model ):
    """Representation of a Pokemon card.

    Currently missing data like images and attacks which may
    be added in the future.
    """
    # eg pgo-2
    #    ^   ^ Number in set
    #    ^ Set abbreviation
    card_id = models.CharField(
            max_length = 20,
            primary_key = True
        )

    # Plaintext name of the card
    card_name = models.CharField( max_length = 64 )

    # Pokémon | Trainer | Energy
    super_type = models.CharField( max_length = 15 )

    # Basic, Stage 1, Stage 2, V, ex, etc. (for pokemon)
    # Item, Supporter, Pokémon Tool, Stadium (for Trainers)
    # Basic, Special (for Energy)
    subtypes = postgres_fields.ArrayField(
            models.CharField( max_length = 15 )
        )
    # HP on the card, or 0 if not a pokemon
    hp = models.PositiveIntegerField()
    # Array of pokemon types
    types = postgres_fields.ArrayField(
            models.CharField( max_length = 15 )
        )
    # The regulation mark on the card (if it has one)
    regulation_mark = models.CharField( max_length = 4 )
    # The rules written on the card. For trainers this is the
    # card effect. For rule box pokemon, this is the rule in 
    # the rule box (useful for GLC legality)
    rules = postgres_fields.ArrayField(
            models.TextField()
        )

    # Bool fields for which formats the card is legal in
    # None for GLC given that it can be derived from
    # expanded_legal and rules.
    expanded_legal  = models.BooleanField()
    standard_legal  = models.BooleanField()
    unlimited_legal = models.BooleanField()

class Deck( models.Model ):
    """Metadata associated with a collection of cards

    TODO: add a field for modification time

    Attributes:
        deck_uuid (UUIDField): A uuid4 string to identify the deck
        deck_name (CharField): A human readable name for the deck
        created (DateTimeField): Date and time the deck was created
        game_format (CharField): 3-letter code for format. Accepts up to 10
            characters for forward compatibility.
        card_allocation (ManyToManyField): Refernces to card instances allocated
            to this deck. See CardAllocation.
    """
    # UUID for deck
    deck_uuid = models.UUIDField(
            default = uuid.uuid4,
            unique = True,
            editable = False,
            primary_key = True,
        )
    # Human readable name of the deck
    deck_name = models.CharField(
            max_length = 80,
            help_text = "A memorable name for the deck.",
        )
    # Date and time deck created
    created = models.DateTimeField( 
            "date created",
            default = datetime.now,
            editable = False
        )
    # What format the deck is legal in
    game_format = models.CharField(
            max_length = 10,
            choices = get_game_formats(),
            help_text = "The format this deck is legal in.",
        )
    # Which cards are associated with this deck
    card_allocation = models.ManyToManyField(
            Card,
            through = "CardAllocation",
        )

    def get_game_format( self ):
        """Return the human-readable name of the deck's format
        """
        return get_game_formats()[self.game_format]

    def n_cards( self ):
        """Return the number of cards allocated to the deck
        """
        calloc = CardAllocation.objects.filter( deck_id = self.deck_uuid )
        return calloc.aggregate( Sum( "n_card_in_deck" ) )['n_card_in_deck__sum']

    def is_legal( self ):
        """NotYetImplemented: check whether the deck is legal in its stated format.
        """
        if self.n_cards != 60:
            return False
        return False

class CardAllocation( models.Model ):
    """Table storing data on the allocation of cards to decks.

    Attributes:
        deck (ForeignKey): The deck_uuid of a Deck entry
        card (ForeignKey): The card_id of a Card entry
        n_card_in_deck (PositiveIntegerField): Number of cards allocated to that deck
    """
    class Meta:
        # Entries must be a unique combination of deck and card
        constraints = [
                models.UniqueConstraint(
                        fields = ['deck_id','card_id'], name = 'unique_deck_entries'
                    )
            ]

    def card_name( self ):
        """Return the name of the card in a record
        """
        return self.card.card_name

    deck = models.ForeignKey( Deck, on_delete = models.CASCADE )
    card = models.ForeignKey( Card, on_delete = models.CASCADE )
    n_card_in_deck = models.PositiveIntegerField()
