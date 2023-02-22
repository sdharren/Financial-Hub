from django.test import TestCase
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.models import User, AccountType, AccountTypeEnum
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

    def test_institution_name_for_stock_account_type(self):
        account_type_object = AccountType.objects.get(user = self.user)
        self.assertEqual(account_type_object.account_institution_name, 'Vanguard')
        self.assertEqual(account_type_object.account_asset_type, AccountTypeEnum.STOCK)

    def test_get_holdings_returns_stocks(self):
        holdings = self.stock_getter.get_holdings()
        self.assertIsNotNone(holdings[0]['account_id'])

    def test_get_securities_returns_securities(self):
        securities = self.stock_getter.get_securities()
        self.assertIsNotNone(securities[0]['close_price'])

    def test_get_accounts_returns_accounts(self):
        accounts = self.stock_getter.get_accounts()
        self.assertIsNotNone(accounts[0]['account_id'])

    def test_can_query_multiple_investment_accounts_from_different_banks(self):
        public_token = self.wrapper.create_public_token(bank_id='ins_12', products_chosen=['investments']) # public token for Fidelity
        self.wrapper.exchange_public_token(public_token)
        self.wrapper.save_access_token(self.user, ['investments'])
        self.stock_getter.query_investments(self.user)
        self.assertEqual(len(self.stock_getter.investments), 2)

        accounts = AccountType.objects.filter(user = self.user)
        for account in accounts:
            self.assertTrue(account.account_institution_name == "Vanguard" or account.account_institution_name , "Fidelity")
            self.assertEqual(account.account_asset_type , AccountTypeEnum.STOCK)

    def test_get_sum_investments_returns_total(self):
        total_sum = self.stock_getter.get_total_investment_sum()
        # these tests might fail at some point if plaid's sandbox changes the values
        self.assertEqual(total_sum, 190446.8005)

    def test_get_prepared_data(self):
        prepared_data = self.stock_getter.get_prepared_data()
        self.assertEqual(len(prepared_data), 12)
    
    def test_get_investment_categories(self):
        categories = self.stock_getter.get_investment_categories()
        self.assertTrue('derivative' in categories)
        self.assertTrue('cash' in categories)
        self.assertTrue('mutual fund' in categories)
        self.assertTrue('equity' in categories)
        self.assertTrue('etf' in categories)

    def test_categorize_security_ids(self):
        categorized_ids = self.stock_getter._categorized_security_ids()
        self.assertTrue('8E4L9XLl6MudjEpwPAAgivmdZRdBPJuvMPlPb' in categorized_ids['derivative'])
        self.assertTrue('9EWp9Xpqk1ua6DyXQb89ikMARWA6eyUzAbPMg' in categorized_ids['cash'])
        self.assertTrue('JDdP7XPMklt5vwPmDN45t3KAoWAPmjtpaW7DP' in categorized_ids['mutual fund'])
        self.assertTrue('KDwjlXj1Rqt58dVvmzRguxJybmyQL8FgeWWAy' in categorized_ids['equity'])
        self.assertTrue('nnmo8doZ4lfKNEDe3mPJipLGkaGw3jfPrpxoN' in categorized_ids['etf'])