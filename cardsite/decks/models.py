import django.contrib.postgres.fields as postgres_fields
from django.db import models

from cardstash.models import CardAllocation, CardStash

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

class Deck( CardStash ):
    """Metadata associated with a collection of cards

    TODO: add a field for modification time

    Attributes:
        uuid (UUIDField): A uuid4 string to identify the deck
        name (CharField): A human readable name for the deck
        created (DateTimeField): Date and time the deck was created
        game_format (CharField): 3-letter code for format. Accepts up to 10
            characters for forward compatibility.
        card_allocation (ManyToManyField): Refernces to card instances allocated
            to this deck. See CardAllocation.
    """
    # What format the deck is legal in
    game_format = models.CharField(
            max_length = 10,
            choices = get_game_formats(),
            help_text = "The format this deck is legal in.",
        )

    def get_game_format( self ):
        """Return the human-readable name of the deck's format
        """
        return get_game_formats()[self.game_format]

    def is_legal( self ):
        """NotYetImplemented: check whether the deck is legal in its stated format.
        """
        if self.n_cards != 60:
            return False
        return False
