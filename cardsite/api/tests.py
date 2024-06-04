from django.contrib.auth.models import AnonymousUser, User
from django.contrib.humanize.templatetags import humanize
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .api import get_n_card_in, index
from cardstash.models import CardStash

class ApiInterfaceTests( TestCase ):
    fixtures = [
            'sv3',
        ]

    def setUp( self ):
        self.request_factory = RequestFactory()
        self.logged_in_user = User.objects.create_user(
                username = "api_test",
                email = "api@example.com",
                password = "api_password",
            )
        self.TestStash = CardStash.objects.create(
                name = 'ApiTestStash',
            )

    def test_no_action_returns_400( self ):
        request = self.request_factory.get( reverse("api_index") )
        response = index( request )
        self.assertContains(response,'Malformed request',status_code=400)

    def test_useless_action_returns_418( self ):
        request = self.request_factory.get( reverse("api_index") )
        request.GET = {
                'action': 'Foo',
            }
        response = index( request )
        self.assertContains(response,'',status_code=418)

    def test_get_n_card_in( self ):
        test_card = 'sv3-5'
        test_quant = 4
        self.TestStash.allocate(test_card,test_quant)
        request = self.request_factory.get( 
                reverse( 'api_get_n_card_in_stash', args=[self.TestStash.uuid] )
            )
        request.GET = {
                'card_id': test_card,
            }
        response = get_n_card_in( request, self.TestStash.uuid )
        self.assertContains( response, test_quant )

    def test_bulk_update( self ):
