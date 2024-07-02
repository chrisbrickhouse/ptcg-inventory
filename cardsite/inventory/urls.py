from django.urls import path

from . import views
from cardstash import views as cardstash_view
from data_import import views as dataimport_view

urlpatterns = [
        path( "", views.index, name = "inventory_index" ),
        path( "import", dataimport_view.import_tabular, name = "import_tabular" ),
        path( "move", cardstash_view.move_stash, name = "bulk_move" ),
        path( "new", views.new_storage_locale, name = "new_inventory" ),
        path( "new/create", views.create_storage_locale_entry, name = "create_inventory" ),
        path( "<uuid:storage_uuid>/", views.storage_locale_details, name = "storage_locale_details" ),
        path( "<uuid:storage_uuid>/edit", views.edit_stored_cards, name = "edit_inventory" ),
        path( "<uuid:storage_uuid>/update_calloc", views.update_calloc, name = "update_calloc" ),
    ]

