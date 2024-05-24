from django.urls import path

from . import views

urlpatterns = [
        path( "", views.index, name = "index" ),
        path( "new", views.new_storage_locale, name = "new" ),
        path( "new/create", views.create_storage_locale_entry, name = "create" ),
        path( "<uuid:storage_uuid>/", views.storage_locale_details, name = "storage_locale_details" ),
        path( "<uuid:storage_uuid>/edit", views.edit_stored_cards, name = "edit" ),
        path( "<uuid:storage_uuid>/update_calloc", views.update_calloc, name = "update_calloc" ),
    ]

