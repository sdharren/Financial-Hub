import re
from django.test import TestCase
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.API_wrappers.plaid_wrapper import PublicTokenNotExchanged, LinkTokenNotCreated, AccessTokenInvalid, InvalidProductSelection, InvalidPublicToken
from assetManager.models import User, AccountType

"""Tests of the PLAID DevelopmentWrapper."""

class DevelopmentWrapperTestCase(TestCase):
    fixtures = ['assetManager/tests/fixtures/users.json']

    def setUp(self):
        self.wrapper = DevelopmentWrapper()
        self.user = User.objects.get(email='johndoe@example.org')

    def test_development_wrapper_set_up_correctly(self):
        self.assertEqual(self.wrapper.CLIENT_ID, '63d288b343e6370012e5be86')
        self.assertEqual(self.wrapper.DEVELOPMENT_KEY,'e28a689e4a829a09af4969900e0e55')
        self.assertEqual(self.wrapper.ACCESS_TOKEN, None)
        self.assertEqual(self.wrapper.ITEM_ID, None)
        self.assertEqual(self.wrapper.LINK_TOKEN, None)
        self.assertTrue(self.wrapper.client is not None)

    def test_wrapper_creates_development_link_token(self):
        self.wrapper.create_link_token()
        regex_match = re.match(r"^link-development-[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$", self.wrapper.get_link_token())
        self.assertIsNotNone(regex_match)

    def test_cannot_get_undefined_access_token(self):
        with self.assertRaises(PublicTokenNotExchanged):
            self.wrapper.get_access_token()

    def test_cannot_get_undefined_item_id(self):
        with self.assertRaises(PublicTokenNotExchanged):
            self.wrapper.get_item_id()

    def test_cannot_get_undefined_link_token(self):
        with self.assertRaises(LinkTokenNotCreated):
            self.wrapper.get_link_token()

    def test_cannot_save_undefined_access_token(self):
        with self.assertRaises(PublicTokenNotExchanged):
            self.wrapper.save_access_token(self.user, ['transactions'])

    def test_wrapper_saves_correct_access_token(self):
        self.wrapper.products_requested = ['transactions']
        self.wrapper.ACCESS_TOKEN = 'access-development-999f84d1-aa93-4fd9-90f0-6af8867a4f0a'
        self.wrapper.save_access_token(self.user, ['transactions'])
        account_type = AccountType.objects.get(user=self.user)
        self.assertEqual(account_type.access_token, self.wrapper.ACCESS_TOKEN)
        self.assertEqual(account_type.account_asset_type, 'transactions')
        self.assertEqual(account_type.account_institution_name, "HSBC (UK) - Personal")

    def test_wrapper_saves_correct_access_token_for_several_products(self):
        self.wrapper.products_requested = ['transactions', 'investments']
        account_count_before = AccountType.objects.all().count()
        self.wrapper.ACCESS_TOKEN = 'access-development-999f84d1-aa93-4fd9-90f0-6af8867a4f0a'

        self.wrapper.save_access_token(self.user, ['transactions', 'investments'])
        account_count_after = AccountType.objects.all().count()
        self.assertEqual(account_count_before + 2, account_count_after)

        all_account_types = AccountType.objects.all()
        for account in all_account_types:
            self.assertEqual(account.account_institution_name,"HSBC (UK) - Personal")

    def test_get_accounts_with_incorrect_access_token(self):
        self.wrapper.ACCESS_TOKEN = 'access-development-999f84d1-aa93-4fd9-90f0-6af8867a4f12'
        with self.assertRaises(AccessTokenInvalid):
            self.wrapper.get_accounts(self.wrapper.ACCESS_TOKEN)

    def test_create_link_token_with_invalid_products_throws_error(self):
        with self.assertRaises(LinkTokenNotCreated):
            self.wrapper.create_link_token(products_chosen=['not a product for sure'])

    def test_create_link_token_with_no_products_throws_error(self):
        with self.assertRaises(InvalidProductSelection):
            self.wrapper.create_link_token(products_chosen=None)

    def test_create_link_token_with_empty_products_throws_error(self):
        with self.assertRaises(InvalidProductSelection):
            self.wrapper.create_link_token(products_chosen=[])

    def test_exchange_public_token_throws_error_with_incorrect_format(self):
        with self.assertRaises(InvalidPublicToken):
            self.wrapper.exchange_public_token(public_token='invalid format')

    def test_exchange_public_token_throws_error_if_no_token_provided(self):
        with self.assertRaises(InvalidPublicToken):
            self.wrapper.exchange_public_token(public_token=None)

    def test_exchange_public_token_throws_error_when_plaid_deems_public_token_invalid(self):
        with self.assertRaises(InvalidPublicToken):
            self.wrapper.exchange_public_token(public_token='public-sandbox-ee8278ff-cf33-45df-b495-a8545ed61f6e')
            # this test could fail if the public token somehow matches one provided by plaid but very unlikely
