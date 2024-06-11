from django.contrib.auth.models import AnonymousUser, User
from django.contrib.humanize.templatetags import humanize
from django.test import RequestFactory, TestCase
from django.urls import reverse

from decks.models import Card
from .models import StorageLocale
from .views import index, edit_stored_cards, new_storage_locale, create_storage_locale_entry, storage_locale_details

# Create your tests here.
class InventoryViewsTest( TestCase ):
    fixtures = [
            "sv3",
        ]

    def setUp( self ):
        self.request_factory = RequestFactory()
        self.logged_in_user = User.objects.create_user(
                username = "inventory_test",
                email = "inventory@example.com",
                password = "inventory_password",
            )
        self.TestLocale = StorageLocale.objects.create(
                name = "TestLocale",
                description = "This is a test.",
            )

    def test_index( self ):
        request = self.request_factory.get( reverse( "inventory_index" ) )
        response = index( request )
        n_locales = StorageLocale.objects.all().count()
        self.assertContains(
                response,
                "<tr>",
                count = n_locales + 1,
            )

    def test_new_storage_locale_logged_in( self ):
        request = self.request_factory.get( reverse( "new_inventory" ) )
        request.user = self.logged_in_user
        response = new_storage_locale( request )
        self.assertContains(
                response,
                '<form action="new/create" method="post">',
                status_code = 200,
            )

    def logged_out_redirect( self, response, redirect_target ):
        needle = '<form action="/accounts/start_session" method="post">'
        self.assertRedirects(
                response,
                redirect_target,
                status_code = 302,
                target_status_code = 200,
                fetch_redirect_response = True,
            )
        self.assertContains(
                response,
                needle,
                status_code = 200,
            )

    def test_new_storage_locale_logged_out( self ):
        response = self.client.get( reverse('new_inventory'), follow=True)
        redirect_target = '/login/?next='+reverse('new_inventory')
        self.logged_out_redirect(response, redirect_target)

    def test_create_storage_locale_entry( self ):
        test_name = 'TestCreateInventoryEntry'
        request = self.request_factory.get( reverse('create_inventory') )
        request.user = self.logged_in_user
        request.POST = { 
                'name': test_name,
                'decription': 'Lorem ipsum dolor sit',
            }

        response = create_storage_locale_entry( request )
        StorageLocale.objects.get( name = test_name )
        self.assertContains( response, 'Stash created!' )

    def test_storage_locale_details( self ):
        def test_table_heading( response, heading, value ):
            expected = '<tr><th scope="row">'+heading+'</th>'
            expected += '<td>'+str(value)+'</td></tr>'
            self.assertContains(
                    response,
                    expected,
                    html=True
                )

        request = self.request_factory.get( reverse('storage_locale_details',args=[self.TestLocale.uuid]) )

        response = storage_locale_details( request, self.TestLocale.uuid )

        headings = [
                ( 'Created:', humanize.naturaltime(self.TestLocale.created) ),
                ( 'Last modified:', humanize.naturaltime(self.TestLocale.modified) ),
                ( 'Number of cards:', self.TestLocale.n_cards() ),
            ]
        for heading, value in headings:
            test_table_heading( response, heading, value )

    def test_edit_stored_cards_logged_in( self ):
        request = self.request_factory.get( reverse('edit_inventory', args=[self.TestLocale.uuid] ))

        request.user = self.logged_in_user

        response = edit_stored_cards( request, self.TestLocale.uuid )
        n_cards = Card.objects.all().count()

        self.assertContains(response, "<option", count=n_cards)

    def test_edit_stored_cards_logged_out( self ):
        url = reverse( 'edit_inventory', args=[self.TestLocale.uuid] )
        response = self.client.get( 
                url,
                follow = True
            )
        redirect_target = '/login/?next='+url
        self.logged_out_redirect(response, redirect_target)
