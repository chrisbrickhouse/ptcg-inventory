from django.contrib.auth.models import AnonymousUser, User
from django.contrib.humanize.templatetags import humanize
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .api import get_n_card_in, index, get_bulk_move_table, update_stash
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

    def test_get_bulk_move_table( self ):
        from_test_card_id = 'sv3-162'
        from_test_card_name = 'Pidgey'
        from_test_card_quant = 5
        to_test_card_id = 'sv3-163'
        to_test_card_name = 'Pidgeotto'
        to_test_card_quant = 2
        both_test_card_id = 'sv3-164'
        both_from_test_card_quant = 3
        both_to_test_card_quant = 2
        both_test_card_name = 'Pidgeot ex'
        expected_json = {
                from_test_card_id: {
                    'from_quantity': from_test_card_quant,
                    'to_quantity': 0,
                    'card_name': from_test_card_name,
                },
                to_test_card_id: {
                    'from_quantity': 0,
                    'to_quantity': to_test_card_quant,
                    'card_name': to_test_card_name,
                },
                both_test_card_id: {
                    'from_quantity': both_from_test_card_quant,
                    'to_quantity': both_to_test_card_quant,
                    'card_name': both_test_card_name,
                }
            }
        from_stash = CardStash.objects.create( name = 'TestFromStash' )
        from_stash.allocate( card_id = from_test_card_id, quantity = from_test_card_quant )
        from_stash.allocate( card_id = both_test_card_id, quantity = both_from_test_card_quant )
        to_stash = CardStash.objects.create( name = 'TestToStash' )
        to_stash.allocate( card_id = to_test_card_id, quantity = to_test_card_quant )
        to_stash.allocate( card_id = both_test_card_id, quantity = both_to_test_card_quant )
        request = self.request_factory.get(
               reverse( "api_get_bulk_move_table", args = [from_stash.uuid, to_stash.uuid] )
            )
        response = get_bulk_move_table( request, from_stash.uuid, to_stash.uuid )
        self.assertJSONEqual(
                str(response.content, encoding='utf-8'),
                expected_json
            )
