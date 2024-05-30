from django.urls import path

from . import views, api

urlpatterns = [
        path( "", api.index),
        path( "get_n_card_in/<uuid:stash_uuid>", api.get_n_card_in ),
        path( "update/<uuid:stash_uuid>", api.update_stash ),
        path( "bulkUpdate", api.move_cards_from_to ),
    ]
