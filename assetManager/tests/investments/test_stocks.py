from django.test import TestCase
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.models import User, AccountType, AccountTypeEnum
from assetManager.API_wrappers.plaid_wrapper import PublicTokenNotExchanged
from assetManager.investments.stocks import StocksGetter, TransactionsNotDefined, InvestmentsNotDefined
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

    def test_query_transactions(self):
        self.stock_getter = self._create_stock_getter_with_sandbox()
        self.stock_getter.query_transactions(self.user, '2023-01-02', '2023-02-09')
        transactions = self.stock_getter.transactions
        transactions_length = len(transactions)
        self.assertEqual(transactions_length, 9)

    def test_get_sum_investments_returns_total(self):
        self.stock_getter = _create_stock_getter_with_fake_data()
        total_sum = self.stock_getter.get_total_investment_sum()
        self.assertEqual(total_sum, 10580.3)
    
    def test_get_investment_categories(self):
        self.stock_getter = _create_stock_getter_with_fake_data()
        categories = self.stock_getter.get_investment_categories()
        self.assertTrue('derivative' in categories)
        self.assertTrue('cash' in categories)
        self.assertTrue('mutual fund' in categories)
        self.assertTrue('equity' in categories)
        self.assertTrue('etf' in categories)

    def test_get_stocks(self):
        self.stock_getter = _create_stock_getter_with_fake_data()
        stocks = self.stock_getter.get_stocks()
        self.assertTrue('ACHN' in stocks)
        self.assertTrue('EWZ' in stocks)
        self.assertTrue('NHX105509' in stocks)
        self.assertTrue('SBSI' in stocks)

    def test_get_stock_history_raises_exception_when_etf_is_delisted(self):
        self.stock_getter = StocksGetter(None)
        with self.assertRaises(TickerNotSupported):
            history = self.stock_getter.get_stock_history('NHX105509')

    def test_get_stock_history_works_for_listed_stock(self):
        self.stock_getter = StocksGetter(None)
        history = self.stock_getter.get_stock_history('NFLX')
        self.assertIsNotNone(history)

    def test_get_return_on_buy_orders_raises_error_if_transactions_are_undefined(self):
        self.stock_getter = StocksGetter(None)
        with self.assertRaises(TransactionsNotDefined):
            self.stock_getter.get_return_on_buy_orders()

    def test_get_return_on_buy_orders(self):
        self.stock_getter = _create_stock_getter_with_fake_data()
        data = self.stock_getter.get_return_on_buy_orders()
        for key in data:
            self.assertTrue(data[key] > 0)
        self.assertEqual(len(data), 2)

    def test_get_return_on_buy_orders_works_with_negative_returns(self):
        transaction_dict = {
            'quantity': 10,
            'price': 1000000,
            'amount': 10000000,
            'security_id': 1,
            'type': 'buy',
            'date': '2022-01-01'
        }
        transactions = []
        transactions.append(Transaction(transaction_dict, 'GOOG'))
        transactions.append(Transaction(transaction_dict, 'NFLX'))
        self.stock_getter = StocksGetter(None)
        self.stock_getter.transactions = transactions
        returns = self.stock_getter.get_return_on_buy_orders()
        for key in returns:
            self.assertTrue(returns[key] < 0)

    def test_get_return_on_buy_orders_returns_nothing_for_unsupported_ticker(self):
        transaction_dict = {
            'quantity': 10,
            'price': 1000000,
            'amount': 10000000,
            'security_id': 1,
            'type': 'buy',
            'date': '2022-01-01'
        }
        transactions = [Transaction(transaction_dict, "UNSUPPORTED_TICKER938428u9jiokefnm")]
        self.stock_getter = StocksGetter(None)
        self.stock_getter.transactions = transactions
        data = self.stock_getter.get_return_on_buy_orders()
        self.assertEqual(len(data), 0)

    def test_get_return_on_current_holdings_raises_error_if_investments_are_undefined(self):
        self.stock_getter = StocksGetter(None)
        with self.assertRaises(InvestmentsNotDefined):
            self.stock_getter.get_return_on_current_holdings()

    def test_get_return_on_current_holdings(self):
        self.stock_getter = _create_stock_getter_with_fake_data()
        data = self.stock_getter.get_return_on_current_holdings()
        self.assertTrue(len(data) > 0)

    def test_get_investment_category_returns_category(self):
        self.stock_getter = _create_stock_getter_with_fake_data()
        data = self.stock_getter.get_investment_category('equity')
        self.assertEqual(data, {'Achillion Pharmaceuticals Inc.': 100.0, 'Southside Bancshares Inc.': 100.0})

    def test_get_stock_ticker_works_for_existing_stock(self):
        self.stock_getter = _create_stock_getter_with_fake_data()
        data = self.stock_getter.get_stock_ticker('Achillion Pharmaceuticals Inc.')
        self.assertEqual(data, 'ACHN')

    def test_get_stock_ticker_returns_error_string_for_undefined_stock(self):
        self.stock_getter = _create_stock_getter_with_fake_data()
        data = self.stock_getter.get_stock_ticker('Netflix but not real')
        self.assertEqual(data, 'Cannot get stock ticker for Netflix but not real')

    def test_get_portfolio_history_works(self):
        self.stock_getter = _create_stock_getter_with_fake_data()
        data = self.stock_getter.get_portfolio_history(months=6)
        self.assertTrue(len(data) > 100)
        for key in data:
            self.assertTrue(data[key] > 0)
        

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

def _create_stock_getter_with_fake_data():
    stock_getter = StocksGetter(None)
    stock_getter.investments = _get_fake_investments()
    stock_getter.transactions = _get_fake_transactions()
    return stock_getter

def _get_fake_investments():
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

def _get_fake_transactions():
    current_dir = os.path.dirname(__file__)
    transactions_file = open(os.path.join(current_dir, 'fake_transactions.json'))
    transactions = json.load(transactions_file)
    return_list = []
    for transaction in transactions:
        return_list.append(Transaction(transaction, transaction['ticker']))
    transactions_file.close()
    return return_list