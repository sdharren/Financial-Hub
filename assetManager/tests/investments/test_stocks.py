from django.test import TestCase
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.models import User, AccountType, AccountTypeEnum
from assetManager.API_wrappers.plaid_wrapper import PublicTokenNotExchanged
from assetManager.investments.stocks import StocksGetter, TransactionsNotDefined
from assetManager.investments.transaction import Transaction
from assetManager.investments.investment import Investment
from assetManager.API_wrappers.yfinance_wrapper import TickerNotSupported
import json
import os

class StocksTestCase(TestCase):
    fixtures = [
        'assetManager/tests/fixtures/users.json',
    ]

    def setUp(self):
        self.stock_getter = None
        self.user = User.objects.get(email='johndoe@example.org')

    # def test_institution_name_for_stock_account_type(self):
    #     self.stock_getter = self._create_stock_getter_with_sandbox()
    #     self.stock_getter.query_investments(self.user)
    #     account_type_object = AccountType.objects.get(user = self.user)
    #     self.assertEqual(account_type_object.account_institution_name, 'Vanguard')
    #     self.assertEqual(account_type_object.account_asset_type, AccountTypeEnum.STOCK)

    # def test_can_query_multiple_investment_accounts_from_different_banks(self):
    #     self.stock_getter = self._create_stock_getter_with_sandbox()
    #     self.stock_getter.query_investments(self.user)
    #     public_token = self.wrapper.create_public_token(bank_id='ins_12', products_chosen=['investments']) # public token for Fidelity
    #     self.wrapper.exchange_public_token(public_token)
    #     self.wrapper.save_access_token(self.user, ['investments'])
    #     self.stock_getter.query_investments(self.user)
    #     self.assertEqual(len(self.stock_getter.investments), 36)

    #     accounts = AccountType.objects.filter(user = self.user)
    #     for account in accounts:
    #         self.assertTrue(account.account_institution_name == "Vanguard" or account.account_institution_name , "Fidelity")
    #         self.assertEqual(account.account_asset_type , AccountTypeEnum.STOCK)

    # def test_query_transactions(self):
    #     self.stock_getter = self._create_stock_getter_with_sandbox()
    #     self.stock_getter.query_transactions(self.user, '2023-01-02', '2023-02-09')
    #     transactions = self.stock_getter.transactions
    #     transactions_length = 0
    #     for key in transactions:
    #         transactions_length += len(transactions[key])
    #     self.assertEqual(transactions_length, 4)

    # def test_get_sum_investments_returns_total(self):
    #     self._create_stock_getter_with_fake_data()
    #     total_sum = self.stock_getter.get_total_investment_sum()
    #     self.assertEqual(total_sum, 10580.3)
    
    # def test_get_investment_categories(self):
    #     self._create_stock_getter_with_fake_data()
    #     categories = self.stock_getter.get_investment_categories()
    #     self.assertTrue('derivative' in categories)
    #     self.assertTrue('cash' in categories)
    #     self.assertTrue('mutual fund' in categories)
    #     self.assertTrue('equity' in categories)
    #     self.assertTrue('etf' in categories)

    # def test_get_stocks(self):
    #     self._create_stock_getter_with_fake_data()
    #     stocks = self.stock_getter.get_stocks()
    #     self.assertTrue('ACHN' in stocks)
    #     self.assertTrue('EWZ' in stocks)
    #     self.assertTrue('NHX105509' in stocks)
    #     self.assertTrue('SBSI' in stocks)

    # def test_get_stock_history_raises_exception_when_etf_is_delisted(self):
    #     self.stock_getter = StocksGetter(None)
    #     with self.assertRaises(TickerNotSupported):
    #         history = self.stock_getter.get_stock_history('NHX105509')

    # def test_get_stock_history_works_for_listed_stock(self):
    #     self.stock_getter = StocksGetter(None)
    #     history = self.stock_getter.get_stock_history('NFLX')
    #     self.assertIsNotNone(history)

    # def test_get_return_on_buy_orders_raises_error_if_transactions_are_undefined(self):
    #     self.stock_getter = StocksGetter(None)
    #     with self.assertRaises(TransactionsNotDefined):
    #         self.stock_getter.get_return_on_buy_orders()

    # def test_get_return_on_buy_orders(self):
    #     self._create_stock_getter_with_fake_data()
    #     data = self.stock_getter.get_return_on_buy_orders()
    #     for key in data:
    #         self.assertTrue(data[key] > 0)
    #     self.assertEqual(len(data), 2)

    # def test_get_return_on_buy_orders_works_with_negative_returns(self):
    #     transaction_dict = {
    #         'quantity': 10,
    #         'price': 1000000,
    #         'amount': 10000000,
    #         'security_id': 1,
    #         'type': 'buy'
    #     }
    #     transactions = []
    #     transactions.append(Transaction(transaction_dict, 'GOOG'))
    #     transactions.append(Transaction(transaction_dict, 'NFLX'))
    #     self.stock_getter = StocksGetter(None)
    #     self.stock_getter.transactions = transactions
    #     returns = self.stock_getter.get_return_on_buy_orders()
    #     for key in returns:
    #         self.assertTrue(returns[key] < 0)

    # def test_get_return_on_buy_orders_returns_nothing_for_unsupported_ticker(self):
    #     transaction_dict = {
    #         'quantity': 10,
    #         'price': 1000000,
    #         'amount': 10000000,
    #         'security_id': 1,
    #         'type': 'buy'
    #     }
    #     transactions = [Transaction(transaction_dict, "UNSUPPORTED_TICKER938428u9jiokefnm")]
    #     self.stock_getter = StocksGetter(None)
    #     self.stock_getter.transactions = transactions
    #     data = self.stock_getter.get_return_on_buy_orders()
    #     self.assertEqual(len(data), 0)

    # def test_get_return_on_current_holdings_works(self):
    #     self._create_stock_getter_with_fake_data()
    #     data = self.stock_getter.get_return_on_current_holdings()
    #     self.assertEqual(len(data), 2)
    #     for key in data:
    #         self.assertTrue(data[key] > 0)

    # def test_get_return_on_current_holdings_works_with_negative_returns(self):
    #     self.stock_getter = StocksGetter(None)
    #     security_dict = {
    #         'name': 'Netflix',
    #         'ticker': 'NFLX',
    #         'type': 'equity',
    #     }
    #     holding_dict = {
    #         'quantity': 5,
    #         'total_price': 5000000,
    #         'security_id': '1'
    #     }
    #     self.stock_getter.investments = [Investment(holding_dict, security_dict)]
    #     data = self.stock_getter.get_return_on_current_holdings()
    #     self.assertEqual(len(data), 1)
    #     for key in data:
    #         self.assertTrue(data[key] < 0)

    def test_get_return_on_holding_works(self):
        self._create_stock_getter_with_fake_data()
        data = self.stock_getter.get_return_on_holding('SBSI')
        self.assertTrue(data > 0)

    def test_get_return_on_holding_raises_error_if_ticker_not_supported(self):
        self._create_stock_getter_with_fake_data()
        with self.assertRaises(TickerNotSupported):
            self.stock_getter.get_return_on_holding('NHX105509')

    # def test_temp(self):
    #     self.stock_getter = self._create_stock_getter_with_custom_user()
    #     self.stock_getter.query_investments(self.user)
    #     self.stock_getter.query_transactions(self.user, '2022-06-29', '2022-07-08')
    #     self.assertEqual(2,2)

    def _create_stock_getter_with_fake_data(self):
        self.stock_getter = StocksGetter(None)
        self.stock_getter.investments = self._get_fake_investments()
        self.stock_getter.transactions = self._get_fake_transactions()

    def _get_fake_investments(self):
        current_dir = os.path.dirname(__file__)
        securities_file = open(os.path.join(current_dir, 'fake_securities.json'))
        holdings_file = open(os.path.join(current_dir, 'fake_holdings.json'))
        securities = json.load(securities_file)
        holdings = json.load(holdings_file)
        investments = []
        for i in range (0, len(securities)):
            investments.append(Investment(holdings[i], securities[i]))
        securities_file.close()
        holdings_file.close()
        return investments
    
    def _get_fake_transactions(self):
        current_dir = os.path.dirname(__file__)
        transactions_file = open(os.path.join(current_dir, 'fake_transactions.json'))
        transactions = json.load(transactions_file)
        return_list = []
        for transaction in transactions:
            return_list.append(Transaction(transaction, transaction['ticker']))
        transactions_file.close()
        return return_list

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
