import re
from django.test import TestCase
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper, IncorrectBankIdOrProduct
from assetManager.API_wrappers.plaid_wrapper import PublicTokenNotExchanged, LinkTokenNotCreated,AccessTokenInvalid
from assetManager.models import User, AccountType, AccountTypeEnum

class SandboxWrapperTestCase(TestCase):
    fixtures = ['assetManager/tests/fixtures/users.json']

    def setUp(self):
        self.wrapper = SandboxWrapper()
        self.user = User.objects.get(email='johndoe@example.org')

    def test_sandbox_initialised_correctly(self):
        self.assertEqual(self.wrapper.CLIENT_ID, '63d288b343e6370012e5be86')
        self.assertEqual(self.wrapper.ACCESS_TOKEN, None)
        self.assertEqual(self.wrapper.ITEM_ID, None)
        self.assertEqual(self.wrapper.LINK_TOKEN, None)
        self.assertTrue(self.wrapper.PUBLIC_TOKEN is None)
        self.assertEqual(self.wrapper.SANDBOX_KEY, '3c1540e977fb113fe9bdbb12bf61fd')
        self.assertTrue(self.wrapper.client is not None)

    def test_create_link_token_with_incorrrect_parameters(self):
        with self.assertRaises(IncorrectBankIdOrProduct):
            self.wrapper.create_public_token(bank_id = 'incorrectid', products_chosen = ['incorrectProduct'])

    def test_create_sandbox_public_token_successfully(self):
        public_token = self.wrapper.create_public_token()
        regex_match = re.match(r"^public-sandbox-[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$", public_token)
        self.assertIsNotNone(regex_match)


"""
    def test_wrapper_saves_correct_access_token(self):
        self.wrapper.products_requested = ['transactions']
        self.wrapper.ACCESS_TOKEN = 'access-sandbox-999f84d1-aa93-4fd9-90f0-6af8867a4f0a'
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

    def test_get_accounts_with_no_access_token(self):
        with self.assertRaises(PublicTokenNotExchanged):
            self.wrapper.get_accounts()

    def test_get_accounts_with_incorrect_access_token(self):
        self.wrapper.ACCESS_TOKEN = 'access-development-999f84d1-aa93-4fd9-90f0-6af8867a4f12'
        with self.assertRaises(AccessTokenInvalid):
            self.wrapper.get_accounts()

    def test_get_accounts_with_correct_access_token(self):
        self.wrapper.ACCESS_TOKEN = 'access-development-999f84d1-aa93-4fd9-90f0-6af8867a4f0a'
        accounts = self.wrapper.get_accounts()
        self.assertEqual(accounts[0]['account_id'],"pw3Z5KxQp4IjJzQjX4qeCOAPO470ZAfypoVbj")
        self.assertEqual(str(accounts[0]['subtype']),"checking")
        self.assertEqual(accounts[0]['balances']['iso_currency_code'],'GBP')

    def test_get_with_no_access_token(self):
        with self.assertRaises(PublicTokenNotExchanged):
            self.wrapper.get_item()

    def test_get_item_with_incorrect_access_token(self):
        self.wrapper.ACCESS_TOKEN = 'access-development-999f84d1-aa93-4fd9-90f0-6af8867a4f12'
        with self.assertRaises(AccessTokenInvalid):
            self.wrapper.get_item()

    def test_get_item_with_correct_access_token(self):
        self.wrapper.ACCESS_TOKEN = 'access-development-999f84d1-aa93-4fd9-90f0-6af8867a4f0a'
        item = self.wrapper.get_item()
        print(o)
"""
