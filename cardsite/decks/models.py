from datetime import datetime
import uuid

import django.contrib.postgres.fields as postgres_fields
from django.db import models

def get_game_formats():
    FORMATS = {
        'STD':'Standard',
        'EXP':'Expanded',
        'GLC':'Gym Leader Challenge',
        'UNL':'Unlimited'
    }
    return FORMATS

class Card( models.Model ):
    card_id = models.CharField(
            max_length = 20,
            primary_key = True
        )
    card_name = models.CharField( max_length = 64 )
    super_type = models.CharField( max_length = 15 )
    subtypes = postgres_fields.ArrayField(
            models.CharField( max_length = 15 )
        )
    hp = models.PositiveIntegerField()
    types = postgres_fields.ArrayField(
            models.CharField( max_length = 15 )
        )
    regulation_mark = models.CharField( max_length = 4 )
    rules = postgres_fields.ArrayField(
            models.TextField()
        )
    expanded_legal  = models.BooleanField()
    standard_legal  = models.BooleanField()
    unlimited_legal = models.BooleanField()

class Deck( models.Model ):
    # UUID for deck
    deck_uuid = models.UUIDField(
            default = uuid.uuid4,
            unique = True,
            editable = False,
            primary_key = True,
        )
    # Human readable name of the deck
    deck_name = models.CharField( max_length = 80 )
    # Date and time deck created
    created = models.DateTimeField( 
            "date created",
            default = datetime.now,
            editable = False
        )
    # What format the deck is legal in
    game_format = models.CharField(
            max_length = 10,
            choices = get_game_formats()
        )
    card_list = models.ManyToManyField(
            'decks.Card',
            related_name = 'deck_uuid'
        )
