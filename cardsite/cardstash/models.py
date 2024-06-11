from datetime import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

class CardStash( models.Model ):
    """Metadata associated with a collection of cards


    Attributes:
        uuid (UUIDField): A uuid4 string to identify the stash
        name (CharField): A human readable name for the stash
        created (DateTimeField): Date and time the stash was created
        modified (DateTimeField): Date and time the stash was modified
        card_allocation (ManyToManyField): Refernces to card instances allocated
            to this stash. See CardAllocation.
    """

    # UUID for stash
    uuid = models.UUIDField(
            default = uuid.uuid4,
            unique = True,
            editable = False,
            primary_key = True,
        )
    # Human readable name of the stash
    name = models.CharField(
            max_length = 80,
            help_text = "A memorable name.",
        )
    # Date and time stats
    created = models.DateTimeField( 
            "date created",
            default = datetime.now,
            editable = False
        )
    modified = models.DateTimeField( 
            "date modified",
            default = datetime.now,
            editable = True
        )
    # Which cards are associated with this deck
    card_allocation = models.ManyToManyField(
            'decks.Card',
            through = "CardAllocation",
        )
    
    # User who created the deck

    def n_cards( self ):
        """Return the number of cards allocated to the deck
        """
        calloc = CardAllocation.objects.filter( stash_id = self.uuid )
        return calloc.aggregate( Sum( "n_card_in_stash" ) )['n_card_in_stash__sum']


class CardAllocation( models.Model ):
    """Table storing data on the allocation of cards to stashes.

    Attributes:
        stash (ForeignKey): The uuid of a CardStash entry
        card (ForeignKey): The card_id of a Card entry
        n_card_in_stash (PositiveIntegerField): Number of cards allocated to that deck
    """
    class Meta:
        # Entries must be a unique combination of deck and card
        constraints = [
                models.UniqueConstraint(
                        fields = ['stash_id','card_id'], name = 'unique_stash_entries'
                    )
            ]

    def card_name( self ):
        """Return the name of the card in a record
        """
        return self.card.card_name

    stash = models.ForeignKey( 'cardstash.CardStash', on_delete = models.CASCADE )
    card = models.ForeignKey( 'decks.Card', on_delete = models.CASCADE )
    n_card_in_stash = models.PositiveIntegerField()
