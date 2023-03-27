from assetManager.transactionInsight.bank_transaction_insight import CategoriseTransactions
from assetManager.transactionInsight.bank_graph_data import format_transactions
from dateutil.tz import tzlocal
import datetime
from django.conf import settings
from django.test import TestCase

class CategoriseTransactionsTestCase(TestCase):

    def setUp(self):
        settings.PLAID_DEVELOPMENT = False
        self.transaction_history = format_transactions([{'account_id': 'a9X88M4oEpfBMMjVpOEVUp0m8ykRZ6f3n58M3a', 'account_owner': None, 'amount': 3.3, 'authorized_date': datetime.date(2022, 11, 18), 'authorized_datetime': None, 'category': ['Travel', 'Public Transportation Services'], 'category_id': '22014000', 'check_number': None, 'date': datetime.date(2022, 11, 21), 'datetime': datetime.datetime(2022, 11, 21, 0, 0, tzinfo=tzlocal()), 'iso_currency_code': 'GBP', 'location': {'address': None,              'city': None,              'country': None,              'lat': None,              'lon': None,              'postal_code': None,              'region': None,              'store_number': None}, 'merchant_name': 'Transport for London', 'name': '9114 18NOV22 CD TFL TRAVEL CH TFL.GOV.UK/CP GB', 'payment_channel': 'online', 'payment_meta': {'by_order_of': None,                  'payee': None,                  'payer': None,                  'payment_method': None,                  'payment_processor': None,                  'ppd_id': None,                  'reason': None,                  'reference_number': None}, 'pending': False, 'pending_transaction_id': None, 'personal_finance_category': None, 'transaction_code': 'purchase', 'transaction_id': 'rkKAAqQRMeSMrrEj0PejH694dNqzKzCj3gvMOq', 'transaction_type': 'place', 'unofficial_currency_code': None}, {'account_id': 'a9X88M4oEpfBMMjVpOEVUp0m8ykRZ6f3n58M3a', 'account_owner': None, 'amount': -40.0, 'authorized_date': datetime.date(2022, 11, 19), 'authorized_datetime': None, 'category': ['Shops', 'Supermarkets and Groceries'], 'category_id': '19047000', 'check_number': None, 'date': datetime.date(2022, 11, 21), 'datetime': datetime.datetime(2022, 11, 21, 0, 0, tzinfo=tzlocal()), 'iso_currency_code': 'GBP', 'location': {'address': None,              'city': None,              'country': None,              'lat': None,              'lon': None,              'postal_code': None,              'region': None,              'store_number': None}, 'merchant_name': None, 'name': 'ANDREI AVETOV SERGEI MINAKOV FP 19/11/22 2125 P457SHRSL7HZKUA1EV', 'payment_channel': 'other', 'payment_meta': {'by_order_of': None,                  'payee': None,                  'payer': None,                  'payment_method': None,                  'payment_processor': None,                  'ppd_id': None,                  'reason': None,                  'reference_number': None}, 'pending': False, 'pending_transaction_id': None, 'personal_finance_category': None, 'transaction_code': None, 'transaction_id': '5aexxV0NmKUBZZY8J4w8Uk0dXeOwEwHm0AqaEq', 'transaction_type': 'place', 'unofficial_currency_code': None}, {'account_id': 'a9X88M4oEpfBMMjVpOEVUp0m8ykRZ6f3n58M3a', 'account_owner': None, 'amount': 1.99, 'authorized_date': datetime.date(2022, 11, 20), 'authorized_datetime': None, 'category': ['Food and Drink', 'Restaurants', 'Fast Food'], 'category_id': '13005032', 'check_number': None, 'date': datetime.date(2022, 11, 21), 'datetime': datetime.datetime(2022, 11, 21, 0, 0, tzinfo=tzlocal()), 'iso_currency_code': 'GBP', 'location': {'address': None,              'city': None,              'country': None,              'lat': None,              'lon': None,              'postal_code': None,              'region': None,              'store_number': None}, 'merchant_name': "McDonald's", 'name': "McDonald's", 'payment_channel': 'in store', 'payment_meta': {'by_order_of': None,                  'payee': None,                  'payer': None,                  'payment_method': None,                  'payment_processor': None,                  'ppd_id': None,                  'reason': None,                  'reference_number': None}, 'pending': False, 'pending_transaction_id': None, 'personal_finance_category': None, 'transaction_code': 'purchase', 'transaction_id': '0v5yyomk0PFL44oxNk9xt8Y3A0PwxwfBgjbz1P', 'transaction_type': 'place', 'unofficial_currency_code': None}, {'account_id': 'a9X88M4oEpfBMMjVpOEVUp0m8ykRZ6f3n58M3a', 'account_owner': None, 'amount': 15.99, 'authorized_date': datetime.date(2022, 11, 19), 'authorized_datetime': None, 'category': ['Service', 'Subscription'], 'category_id': '18061000', 'check_number': None, 'date': datetime.date(2022, 11, 21), 'datetime': datetime.datetime(2022, 11, 21, 0, 0, tzinfo=tzlocal()), 'iso_currency_code': 'GBP', 'location': {'address': None,              'city': None,              'country': None,              'lat': None,              'lon': None,              'postal_code': None,              'region': None,              'store_number': None}, 'merchant_name': 'Netflix', 'name': 'Netflix', 'payment_channel': 'online', 'payment_meta': {'by_order_of': None,                  'payee': None,                  'payer': None,                  'payment_method': None,                  'payment_processor': None,                  'ppd_id': None,                  'reason': None,                  'reference_number': None}, 'pending': False, 'pending_transaction_id': None, 'personal_finance_category': None, 'transaction_code': 'purchase', 'transaction_id': 'jD0eeYgjEmfrLLbe8BaeTeEOBxVYmYTk0wLoq0', 'transaction_type': 'place', 'unofficial_currency_code': None}, {'account_id': 'a9X88M4oEpfBMMjVpOEVUp0m8ykRZ6f3n58M3a', 'account_owner': None, 'amount': 20.0, 'authorized_date': datetime.date(2022, 11, 20), 'authorized_datetime': None, 'category': ['Food and Drink', 'Restaurants'], 'category_id': '13005000', 'check_number': None, 'date': datetime.date(2022, 11, 21), 'datetime': datetime.datetime(2022, 11, 21, 0, 0, tzinfo=tzlocal()), 'iso_currency_code': 'GBP', 'location': {'address': None,              'city': None,              'country': None,              'lat': None,              'lon': None,              'postal_code': None,              'region': None,              'store_number': None}, 'merchant_name': None, 'name': 'THAI THAI PLACE VIA MOBILE - LVP FP 20/11/22 10 39142730062162000N', 'payment_channel': 'in store', 'payment_meta': {'by_order_of': None,                  'payee': None,                  'payer': None,                  'payment_method': None,                  'payment_processor': None,                  'ppd_id': None,                  'reason': None,                  'reference_number': None}, 'pending': False, 'pending_transaction_id': None, 'personal_finance_category': None, 'transaction_code': 'transfer', 'transaction_id': 'Z83BBoKQEVtwooLxZ4XxIbe50dQMPMFPKL0dy6', 'transaction_type': 'place', 'unofficial_currency_code': None}])

    def test_get_transactions(self):
        transactions = CategoriseTransactions(self.transaction_history)
        self.assertEqual(transactions.get_transaction_history(), self.transaction_history)

    def test_get_empty_transactions(self):
        transactions = CategoriseTransactions("")
        self.assertEqual(transactions.get_transaction_history(), "")

    def test_get_yearly_spending(self):
        transactions = CategoriseTransactions(self.transaction_history)
        self.assertEqual(transactions.get_total_spending(), 41.28)

    def test_get_no_yearly_spending(self):
        transactions = CategoriseTransactions("")
        self.assertEqual(transactions.get_total_spending(), 0)

    def test_get_november_monthly_spending(self):
        transactions = CategoriseTransactions(self.transaction_history)
        self.assertEqual(transactions.get_monthly_spending(11,2022), 41.28)

    def test_get_december_monthly_spending(self):
        transactions = CategoriseTransactions(self.transaction_history)
        self.assertEqual(transactions.get_monthly_spending(12,2022), 0)

    def test_get_no_monthly_spending(self):
        transactions = CategoriseTransactions("")
        self.assertEqual(transactions.get_monthly_spending(11,2022), 0)

    def test_get_mcdonalds_spending(self):
        transactions = CategoriseTransactions(self.transaction_history)
        self.assertEqual(transactions.get_spending_for_company("McDonald's"), 1.99)

    def test_get_mcdonalds_spending_for_empty_json(self):
        transactions = CategoriseTransactions("")
        self.assertEqual(transactions.get_spending_for_company("McDonald's"), 0)

    def test_get_no_company_spending(self):
        transactions = CategoriseTransactions(self.transaction_history)
        self.assertEqual(transactions.get_spending_for_company(""), 0)

    def test_get_no_company_spending_for_empty_json(self):
        transactions = CategoriseTransactions("")
        self.assertEqual(transactions.get_spending_for_company(""), 0)

    def test_get_november_third_week_spending(self):
        transactions = CategoriseTransactions(self.transaction_history)
        self.assertEqual(transactions.get_weekly_spending(3,11,2022), 41.28)

    def test_get_december_first_week_monthly_spending(self):
        transactions = CategoriseTransactions(self.transaction_history)
        self.assertEqual(transactions.get_weekly_spending(1,12,2022), 0)

    def test_get_no_weekly_spending(self):
        transactions = CategoriseTransactions("")
        self.assertEqual(transactions.get_weekly_spending(1,11,2022), 0)

    def test_get_categories_of_spending(self):
        transactions = CategoriseTransactions(self.transaction_history)
        self.assertEqual(transactions.get_categorised_spending(self.transaction_history), {'Travel': 3.3, 'Food and Drink': 21.99, 'Service': 15.99})

    def test_get_categories_of_spending(self):
        transactions = CategoriseTransactions("")
        self.assertEqual(transactions.get_categorised_spending(""), {})

    def test_get_november_monthly_transactions(self):
        transactions = CategoriseTransactions(self.transaction_history)
        self.assertNotEqual(transactions.get_monthly_transactions(11,2022), [])

    def test_get_yearly_transactions(self):
        transactions = CategoriseTransactions(self.transaction_history)
        self.assertNotEqual(transactions.get_yearly_transactions(2022), [])

    def test_get_no_yearly_transactions(self):
        transactions = CategoriseTransactions("")
        self.assertEqual(transactions.get_yearly_transactions(2022), [])

    def test_get_december_monthly_transactions(self):
        transactions = CategoriseTransactions(self.transaction_history)
        self.assertEqual(transactions.get_monthly_transactions(12,2022), [])

    def test_get_no_monthly_transactions(self):
        transactions = CategoriseTransactions("")
        self.assertEqual(transactions.get_monthly_transactions(11,2022), [])

    def test_get_november_weekly_transactions(self):
        transactions = CategoriseTransactions(self.transaction_history)
        self.assertNotEqual(transactions.get_weekly_transactions(3,11,2022), [])

    def test_get_december_weekly_transactions(self):
        transactions = CategoriseTransactions(self.transaction_history)
        self.assertEqual(transactions.get_weekly_transactions(1,12,2022), [])

    def test_get_no_weekly_transactions(self):
        transactions = CategoriseTransactions("")
        self.assertEqual(transactions.get_weekly_transactions(3,11,2022), [])

    def test_get_ordered_categories_of_transactions(self):
        transactions = CategoriseTransactions(self.transaction_history)
        self.assertEqual(transactions.get_order_categories(self.transaction_history), [{'name': 'Food and Drink', 'value': 21.99},{'name': 'Service', 'value': 15.99},{'name': 'Travel', 'value': 3.3}])

    def test_get_no_ordered_categories_of_transactions(self):
        transactions = CategoriseTransactions("")
        self.assertEqual(transactions.get_order_categories(""), [])
