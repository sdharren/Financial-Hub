from django.test import TestCase
from assetManager.models import User
from assetManager.API_wrappers.plaid_wrapper import PlaidWrapper, PublicTokenNotExchanged, PlaidWrapperIsAnAbstractClass

"""Tests of the PLAID general wrapper class."""

class PlaidWrapperTestCase(TestCase):
    fixtures = [
        'assetManager/tests/fixtures/users.json',
        'assetManager/tests/fixtures/account_types.json'
        ]

    def setUp(self):
        self.wrapper = PlaidWrapper()

    def test_plaid_wrapper_correctly_initialised(self):
        self.assertEqual(self.wrapper.CLIENT_ID, '63d288b343e6370012e5be86')
        self.assertEqual(self.wrapper.ACCESS_TOKEN, None)
        self.assertEqual(self.wrapper.ITEM_ID, None)
        self.assertEqual(self.wrapper.LINK_TOKEN, None)

    def test_cannot_retrieve_non_existent_access_token(self):
        user = User.objects.get(email='johndoe@example.org')
        product = 'investments'
        with self.assertRaises(PublicTokenNotExchanged):
            self.wrapper.retrieve_access_tokens(user, product)

    def test_can_retrieve_existent_access_token(self):
        user = User.objects.get(email='johndoe@example.org')
        product = 'transactions'
        tokens = self.wrapper.retrieve_access_tokens(user, product)
        self.assertEqual(tokens[0], 'access-development-8ab976e6-64bc-4b38-98f7-731e7a349970')

    # Plaid wrapper is an abstract class so this should never be allowed
    def test_cannot_exchange_public_token_with_plaid_wrapper(self):
        with self.assertRaises(PlaidWrapperIsAnAbstractClass):
            self.wrapper.exchange_public_token('access-development-8ab976e6-64bc-4b38-98f7-731e7a349970')
