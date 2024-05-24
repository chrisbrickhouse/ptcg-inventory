from django.forms import modelform_factory
from django.shortcuts import HttpResponse
from django.template import loader

from .models import StorageLocale
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
