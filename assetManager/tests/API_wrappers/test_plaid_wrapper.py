from django.test import TestCase
from assetManager.models import User
from assetManager.API_wrappers.plaid_wrapper import PlaidWrapper, PublicTokenNotExchanged, PlaidWrapperIsAnAbstractClass

class PlaidWrapperTestCase(TestCase):
    fixtures = [
        'assetManager/tests/fixtures/users.json',
        'assetManager/tests/fixtures/account_types.json'
        ]

    def setUp(self):
        self.wrapper = PlaidWrapper()

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
