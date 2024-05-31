from django.forms import modelform_factory
from django.shortcuts import render, HttpResponse
from django.template import loader

from .models import StorageLocale
from decks.models import Card
from cardstash.models import CardAllocation
import cardstash.views

def index( request ):
    return cardstash.views.index(
            request,
            StorageLocale,
            "list_of_storage_locales",
            "inventory/index.html"
        )

def new_storage_locale( request, error = None ):
    fields = [ "name", "description" ]
    labels = { 
              "name": "Location name",
              "description": "Description",
        }
    return cardstash.views.new_stash(
            request,
            StorageLocale,
            fields,
            labels,
        )

def create_storage_locale_entry( request ):
    headers = [ 'name', 'description' ]
    return cardstash.views.create_stash_entry( 
            request,
            StorageLocale,
            headers,
        )

def storage_locale_details( request, storage_uuid ):
    storage_locale_instance = StorageLocale.objects.get( uuid = storage_uuid )
    inventory_list = CardAllocation.objects.filter( stash_id = storage_uuid )
    context = {
            'StorageLocale': storage_locale_instance,
            'stash_list': inventory_list
        }
    return render(
            request,
            'inventory/inventory_details.html',
            context
        )

def edit_stored_cards( request, storage_uuid ):
    storage_instance = StorageLocale.objects.get( uuid = storage_uuid )
    card_list = Card.objects.all()
    stored_card_list = CardAllocation.objects.filter( stash_id = storage_uuid )
    context = {
            'Stash': storage_instance,
            'card_list': card_list,
            'stash_list': stored_card_list,
            'post_url': 'update_calloc',
            'api_url': 'http://localhost:8000/api',
        }
    return render(
            request,
            'cardstash/edit_stash.html',
            context
        )

def update_calloc( request, storage_uuid ):
    return cardstash.views.update_calloc( request, storage_uuid )
