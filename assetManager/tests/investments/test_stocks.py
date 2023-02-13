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
        self.wrapper.save_access_token(self.user)
        self.access_token = self.wrapper.get_access_token()
        self.stock_getter = StocksGetter(self.wrapper)

    def test_get_holdings_returns_stocks(self):
        self.stock_getter.query_investments(self.user)
        holdings = self.stock_getter.get_holdings()
        self.assertIsNotNone(holdings[0][0]['account_id'])

    def test_get_securities_returns_securities(self):
        self.stock_getter.query_investments(self.user)
        securities = self.stock_getter.get_securities()
        self.assertIsNotNone(securities[0][0]['close_price'])

    def test_get_accounts_returns_accounts(self):
        self.stock_getter.query_investments(self.user)
        accounts = self.stock_getter.get_accounts()
        self.assertIsNotNone(accounts[0][0]['account_id'])

    def test_can_query_multiple_investment_accounts_from_different_banks(self):
        public_token = self.wrapper.create_public_token(bank_id='ins_12', products_chosen=['investments']) # public token for Fidelity
        self.wrapper.exchange_public_token(public_token)
        self.wrapper.save_access_token(self.user)
        self.stock_getter.query_investments(self.user)
        self.assertEqual(len(self.stock_getter.investments), 2)

    def test_get_sum_investments_returns_total(self):
        self.stock_getter.query_investments(self.user)
        total_sum = self.stock_getter.get_total_investment_sum()
        print(total_sum)
        self.assertEqual(total_sum, 190446.8005)