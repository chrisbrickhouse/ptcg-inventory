from django.urls import path

from . import views, api

urlpatterns = [
        path( "", api.index, name = "api_index"),
        path( "get_n_card_in/<uuid:stash_uuid>", api.get_n_card_in, name="api_get_n_card_in_stash" ),
        path( "update/<uuid:stash_uuid>", api.update_stash, name="api_update_stash" ),
        path( "bulkUpdate", api.move_cards_from_to, name="api_bulk_update" ),
    ]

