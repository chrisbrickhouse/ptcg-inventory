from django.urls import path

from . import views

urlpatterns = [
        path( "", views.index, name = "index" ),
        path( "new", views.new_storage_locale, name = "new" ),
        path( "new/create", views.create_storage_locale_entry, name = "create" ),
        #path( "<uuid:storage_uuid>/", views.deck_details, name = "deck_details" ),
        #path( "<uuid:storage_uuid>/edit", views.edit_deck, name = "edit" ),
        #path( "<uuid:storage_uuid>/update_calloc", views.update_calloc, name = "update_calloc" ),
    ]

