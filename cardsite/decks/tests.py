import urllib

from django.contrib.auth.models import AnonymousUser, User
from django.contrib.humanize.templatetags import humanize
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .models import Deck, Card
from .views import create_deck_entry, deck_details, edit_deck, index, new_deck

# Create your tests here.
class DecksViewsTest( TestCase ):
    fixtures = [
            "sv3"
        ]

    def setUp( self ):
        self.request_factory = RequestFactory()
        self.logged_in_user = User.objects.create_user(
                username = "test",
                email = "test@example.com",
                password = "test_password",
            )
        self.TestDeck = Deck.objects.create(
                name = "TestDeck",
                game_format = 'STD',
            )

    def test_new_stash_logged_in( self ):
        request = self.request_factory.get( reverse('new_deck') )

        request.user = self.logged_in_user

        response = new_deck( request )
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

    def test_new_stash_logged_out( self ):
        response = self.client.get( reverse('new_deck'), follow=True)
        redirect_target = '/login/?next='+reverse('new_deck')
        self.logged_out_redirect(response, redirect_target)

    def test_deck_details( self ):
        def test_table_heading( response, heading, value ):
            expected = '<tr><th scope="row">'+heading+'</th>'
            expected += '<td>'+str(value)+'</td></tr>'
            self.assertContains(
                    response,
                    expected,
                    html=True
                )

        request = self.request_factory.get( reverse('deck_details',args=[self.TestDeck.uuid]) )

        response = deck_details( request, self.TestDeck.uuid )

        headings = [
                ( 'Deck format:', self.TestDeck.get_game_format() ),
                ( 'Created:', humanize.naturaltime(self.TestDeck.created) ),
                ( 'Last modified:', humanize.naturaltime(self.TestDeck.modified) ),
                ( 'Number of cards:', self.TestDeck.n_cards() ),
                ( 'Legal?', self.TestDeck.is_legal() )
            ]
        for heading, value in headings:
            test_table_heading( response, heading, value )

    def test_edit_deck_logged_in( self ):
        request = self.request_factory.get( reverse('edit_deck', args=[self.TestDeck.uuid] ))

        request.user = self.logged_in_user

        response = edit_deck( request, self.TestDeck.uuid )
        n_legal_cards = Card.objects.filter( standard_legal = True ).count()

        self.assertContains(response, "<option", count=n_legal_cards)

    def test_edit_deck_logged_out( self ):
        url = reverse( 'edit_deck', args=[self.TestDeck.uuid] )
        response = self.client.get( 
                url,
                follow = True
            )
        redirect_target = '/login/?next='+url
        self.logged_out_redirect(response, redirect_target)

    def test_create_deck_entry_logged_in( self ):
        test_name = 'TestCreateDeckEntry'
        request = self.request_factory.get( reverse('create_deck') )
        request.user = self.logged_in_user
        request.POST = { 
                'name': test_name,
                'game_format': 'STD',
            }

        response = create_deck_entry( request )
        Deck.objects.get( name = test_name )
        self.assertContains( response, 'Stash created!' )

    def test_deck_index( self ):
        request = self.request_factory.get( reverse("deck_index") )
        n_decks = Deck.objects.all().count()
        response = index( request )
        self.assertContains( response,"<tr>", count = n_decks + 1 ) 
