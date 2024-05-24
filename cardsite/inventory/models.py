from django.db import models

from cardstash.models import CardStash

class StorageLocale( CardStash ):
    """Metadata associated with a collection of cards

    Attributes:
        uuid (UUIDField): A uuid4 string to identify the deck
        name (CharField): A human readable name for the deck
        created (DateTimeField): Date and time the deck was created
        card_allocation (ManyToManyField): Refernces to card instances allocated
            to this deck. See CardAllocation.
    """
    description = models.TextField()
