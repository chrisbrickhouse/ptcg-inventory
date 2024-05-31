from django.apps import AppConfig


class DecksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'decks'

class CardStashConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cardstash'
