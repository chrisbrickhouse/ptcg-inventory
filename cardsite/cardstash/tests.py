from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from .models import CardStash, CardAllocation

class CardStashModelTest( TestCase ):
    fixtures = [
        "pgo",
        "sv3",
        "base1",
        "base4",
        "sv4pt5",
    ]

    def setUp( self ):
        CardStash.objects.create( name="TestStash" )
        self.TestStash = CardStash.objects.get(name="TestStash")

    def test_allocate_and_delete_allocation( self ):
        test_card = 'pgo-1'
        test_quant = 2

        # Test .allocate()
        self.TestStash.allocate( card_id = test_card, quantity = test_quant )
        calloc = CardAllocation.objects.get(
                stash_id = self.TestStash.uuid,
                card_id = test_card
            )
        self.assertEqual( calloc.n_card_in_stash, test_quant )

        # Test .delete_allocation()
        self.TestStash.delete_allocation( test_card )
        self.assertRaises(
                ObjectDoesNotExist,
                CardAllocation.objects.get,
                stash_id = self.TestStash.uuid,
                card_id = test_card,
            )

    def test_allocate_deletes_on_zero( self ):
        test_card = "pgo-1"
        self.TestStash.allocate( card_id = test_card, quantity = 3 )
        self.TestStash.allocate( card_id = test_card, quantity = 0 )
        self.assertRaises(
                ObjectDoesNotExist,
                CardAllocation.objects.get,
                stash_id = self.TestStash.uuid,
                card_id = test_card,
            )

    def test_allocate_raises_ValErr_on_negative( self ):
        test_card = "pgo-1"
        self.assertRaises(
                ValueError,
                self.TestStash.allocate,
                card_id = test_card,
                quantity = -1,
            )

        
    def test_n_cards_is_correct( self ):
        def provide_card_allocations():
            return [
                    ('sv3-164',4),
                    ('sv3-162',4),
                    ('pgo-4',3),
                    ('base1-81',1),
                    ('sv4pt5-196',2),
                    ('base4-128',15),
                ]
        CardStash.objects.create( name = "CleanStash" )
        CleanStash = CardStash.objects.get( name = "CleanStash" )

        for card, quant in provide_card_allocations():
            CleanStash.allocate( card_id = card, quantity = quant )

        expected_quant = sum( [ x[1] for x in provide_card_allocations() ] )
        self.assertEquals( CleanStash.n_cards(), expected_quant )
        CleanStash.delete()
