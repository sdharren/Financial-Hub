import re
from django.test import TestCase
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.API_wrappers.plaid_wrapper import PublicTokenNotExchanged, LinkTokenNotCreated
from assetManager.models import User, AccountType, AccountTypeEnum

class DevelopmentWrapperTestCase(TestCase):
    fixtures = ['assetManager/tests/fixtures/users.json']

    def setUp(self):
        self.wrapper = DevelopmentWrapper()
        self.user = User.objects.get(email='johndoe@example.org')

    def test_wrapper_creates_link_token(self):
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
        self.wrapper.ACCESS_TOKEN = 'access-development-c619bf87-1395-44ae-ad2c-34d99d53bc60'
        self.wrapper.save_access_token(self.user, ['transactions'])
        account_type = AccountType.objects.get(user=self.user)
        self.assertEqual(account_type.access_token, self.wrapper.ACCESS_TOKEN)
        self.assertEqual(account_type.account_asset_type, 'transactions')

    def test_wrapper_saves_correct_access_token_for_several_products(self):
        self.wrapper.products_requested = ['transactions', 'investments']
        account_count_before = AccountType.objects.all().count()
        self.wrapper.ACCESS_TOKEN = 'access-development-c619bf87-1395-44ae-ad2c-34d99d53bc60'
        self.wrapper.save_access_token(self.user, ['transactions', 'investments'])
        account_count_after = AccountType.objects.all().count()
        self.assertEqual(account_count_before + 2, account_count_after)