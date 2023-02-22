from django.test import TestCase
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.models import User, AccountType
from assetManager.API_wrappers.plaid_wrapper import PublicTokenNotExchanged
from assetManager.investments.stocks import StocksGetter

class StocksTestCase(TestCase):
    fixtures = [
        'assetManager/tests/fixtures/users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.org')
        self.wrapper = SandboxWrapper()
        # creating a sandbox public token for vanguard
        public_token = self.wrapper.create_public_token(bank_id='ins_115616', products_chosen=['investments'])
        self.wrapper.exchange_public_token(public_token)
        self.wrapper.save_access_token(self.user, ['investments'])
        self.stock_getter = StocksGetter(self.wrapper)
        self.stock_getter.query_investments(self.user)

    def test_can_query_multiple_investment_accounts_from_different_banks(self):
        public_token = self.wrapper.create_public_token(bank_id='ins_12', products_chosen=['investments']) # public token for Fidelity
        self.wrapper.exchange_public_token(public_token)
        self.wrapper.save_access_token(self.user, ['investments'])
        self.stock_getter.query_investments(self.user)
        self.assertEqual(len(self.stock_getter.investments), 36)

    def test_get_sum_investments_returns_total(self):
        total_sum = self.stock_getter.get_total_investment_sum()
        # these tests might fail at some point if plaid's sandbox changes the values
        self.assertEqual(total_sum, 24498.313179999997)

    def test_get_prepared_data(self):
        prepared_data = self.stock_getter.get_prepared_data()
        self.assertEqual(len(prepared_data), 11)
    
    def test_get_investment_categories(self):
        categories = self.stock_getter.get_investment_categories()
        self.assertTrue('derivative' in categories)
        self.assertTrue('cash' in categories)
        self.assertTrue('mutual fund' in categories)
        self.assertTrue('equity' in categories)
        self.assertTrue('etf' in categories)