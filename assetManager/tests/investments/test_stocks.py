from django.test import TestCase
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.models import User, AccountType, AccountTypeEnum
from assetManager.API_wrappers.plaid_wrapper import PublicTokenNotExchanged
from assetManager.investments.stocks import StocksGetter, CannotGetStockHistoryException, TransactionsNotDefined

class StocksTestCase(TestCase):
    fixtures = [
        'assetManager/tests/fixtures/users.json',
    ]

    def setUp(self):
        self.stock_getter = None
        self.user = User.objects.get(email='johndoe@example.org')

    def test_institution_name_for_stock_account_type(self):
        self.stock_getter = self._create_stock_getter_with_sandbox()
        self.stock_getter.query_investments(self.user)
        account_type_object = AccountType.objects.get(user = self.user)
        self.assertEqual(account_type_object.account_institution_name, 'Vanguard')
        self.assertEqual(account_type_object.account_asset_type, AccountTypeEnum.STOCK)

    def test_can_query_multiple_investment_accounts_from_different_banks(self):
        self.stock_getter = self._create_stock_getter_with_sandbox()
        self.stock_getter.query_investments(self.user)
        public_token = self.wrapper.create_public_token(bank_id='ins_12', products_chosen=['investments']) # public token for Fidelity
        self.wrapper.exchange_public_token(public_token)
        self.wrapper.save_access_token(self.user, ['investments'])
        self.stock_getter.query_investments(self.user)
        self.assertEqual(len(self.stock_getter.investments), 36)

        accounts = AccountType.objects.filter(user = self.user)
        for account in accounts:
            self.assertTrue(account.account_institution_name == "Vanguard" or account.account_institution_name , "Fidelity")
            self.assertEqual(account.account_asset_type , AccountTypeEnum.STOCK)

    def test_get_sum_investments_returns_total(self):
        self.stock_getter = self._create_stock_getter_with_sandbox()
        self.stock_getter.query_investments(self.user)
        total_sum = self.stock_getter.get_total_investment_sum()
        # these tests might fail at some point if plaid's sandbox changes the values
        self.assertEqual(total_sum, 24498.313179999997)

    def test_get_prepared_data(self):
        self.stock_getter = self._create_stock_getter_with_sandbox()
        self.stock_getter.query_investments(self.user)
        prepared_data = self.stock_getter.get_prepared_data()
        self.assertEqual(len(prepared_data), 11)
    
    def test_get_investment_categories(self):
        self.stock_getter = self._create_stock_getter_with_sandbox()
        self.stock_getter.query_investments(self.user)
        categories = self.stock_getter.get_investment_categories()
        self.assertTrue('derivative' in categories)
        self.assertTrue('cash' in categories)
        self.assertTrue('mutual fund' in categories)
        self.assertTrue('equity' in categories)
        self.assertTrue('etf' in categories)

    def test_get_stocks(self):
        self.stock_getter = self._create_stock_getter_with_sandbox()
        self.stock_getter.query_investments(self.user)
        stocks = self.stock_getter.get_stocks()
        self.assertTrue('ACHN' in stocks)
        self.assertTrue('EWZ' in stocks)
        self.assertTrue('NHX105509' in stocks)
        self.assertTrue('SBSI' in stocks)

    def test_get_stock_history_raises_exception_when_etf_is_delisted(self):
        self.stock_getter = self._create_stock_getter_with_sandbox()
        self.stock_getter.query_investments(self.user)
        with self.assertRaises(CannotGetStockHistoryException):
            history = self.stock_getter.get_stock_history('NHX105509')

    def test_get_stock_history_works_for_listed_stock(self):
        self.stock_getter = self._create_stock_getter_with_sandbox()
        self.stock_getter.query_investments(self.user)
        history = self.stock_getter.get_stock_history('NFLX')
        self.assertIsNotNone(history)

    def test_query_transactions(self):
        self.stock_getter = self._create_stock_getter_with_sandbox()
        self.stock_getter.query_transactions(self.user, '2023-01-02', '2023-02-09')
        buy_orders = self.stock_getter.buy_orders
        self.assertEqual(len(buy_orders), 4)

    def test_get_return_on_buy_orders_raises_error_if_transactions_are_undefined(self):
        self.stock_getter = self._create_stock_getter_with_sandbox()
        with self.assertRaises(TransactionsNotDefined):
            self.stock_getter.get_return_on_buy_orders()
        
    def test_get_return_on_buy_orders(self):
        self.stock_getter = self._create_stock_getter_with_sandbox()
        self.stock_getter.query_transactions(self.user, '2023-01-02', '2023-02-09')
        data = self.stock_getter.get_return_on_buy_orders()
        self.assertEqual(len(data), 0)

    def test_get_return_on_buy_orders_with_custom_user(self):
        self.stock_getter = self._create_stock_getter_with_custom_user()
        self.stock_getter.query_transactions(self.user, '2021-03-20', '2023-02-20')
        data = self.stock_getter.get_return_on_buy_orders()
        self.assertEqual(len(data), 2)

    def _create_stock_getter_with_sandbox(self):
        self.wrapper = SandboxWrapper()
        # creating a sandbox public token for vanguard
        public_token = self.wrapper.create_public_token(bank_id='ins_115616', products_chosen=['investments'])
        self.wrapper.exchange_public_token(public_token)
        self.wrapper.save_access_token(self.user, ['investments'])
        return StocksGetter(self.wrapper)

    def _create_stock_getter_with_custom_user(self):
        self.wrapper = SandboxWrapper()
        public_token = self.wrapper.create_public_token_custom_user(bank_id='ins_115616', products_chosen=['investments'], override_username='custom_stocks_user')
        self.wrapper.exchange_public_token(public_token)
        self.wrapper.save_access_token(self.user, ['investments'])
        return StocksGetter(self.wrapper)


