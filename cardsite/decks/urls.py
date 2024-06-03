from django.urls import path

from . import views

urlpatterns = [
        path( "", views.index, name = "deck_index" ),
        path( "new", views.new_deck, name = "new_deck" ),
        path( "new/create", views.create_deck_entry, name = "create_deck" ),
        path( "<uuid:deck_uuid>/", views.deck_details, name = "deck_details" ),
        path( "<uuid:deck_uuid>/edit", views.edit_deck, name = "edit_deck" ),
        path( "<uuid:deck_uuid>/update_calloc", views.update_calloc, name = "update_calloc" ),
    ]

