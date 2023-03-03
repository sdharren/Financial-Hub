# from assetManager.transactionInsight.bank_transaction_insight import CategoriseTransactions
from assetManager.transactionInsight.bank_graph_data import BankGraphData
from dateutil.tz import tzlocal
import datetime

from django.test import TestCase

class CreateBankGraphDataTestCase(TestCase):
    def setUp(self):
        self.transaction_history = [{'account_id': 'a9X88M4oEpfBMMjVpOEVUp0m8ykRZ6f3n58M3a', 'account_owner': None, 'amount': 3.3, 'authorized_date': datetime.date(2022, 11, 18), 'authorized_datetime': None, 'category': ['Travel', 'Public Transportation Services'], 'category_id': '22014000', 'check_number': None, 'date': datetime.date(2022, 11, 21), 'datetime': datetime.datetime(2022, 11, 21, 0, 0, tzinfo=tzlocal()), 'iso_currency_code': 'GBP', 'location': {'address': None,              'city': None,              'country': None,              'lat': None,              'lon': None,              'postal_code': None,              'region': None,              'store_number': None}, 'merchant_name': 'Transport for London', 'name': '9114 18NOV22 CD TFL TRAVEL CH TFL.GOV.UK/CP GB', 'payment_channel': 'online', 'payment_meta': {'by_order_of': None,                  'payee': None,                  'payer': None,                  'payment_method': None,                  'payment_processor': None,                  'ppd_id': None,                  'reason': None,                  'reference_number': None}, 'pending': False, 'pending_transaction_id': None, 'personal_finance_category': None, 'transaction_code': 'purchase', 'transaction_id': 'rkKAAqQRMeSMrrEj0PejH694dNqzKzCj3gvMOq', 'transaction_type': 'place', 'unofficial_currency_code': None}, {'account_id': 'a9X88M4oEpfBMMjVpOEVUp0m8ykRZ6f3n58M3a', 'account_owner': None, 'amount': -40.0, 'authorized_date': datetime.date(2022, 11, 19), 'authorized_datetime': None, 'category': ['Shops', 'Supermarkets and Groceries'], 'category_id': '19047000', 'check_number': None, 'date': datetime.date(2022, 11, 21), 'datetime': datetime.datetime(2022, 11, 21, 0, 0, tzinfo=tzlocal()), 'iso_currency_code': 'GBP', 'location': {'address': None,              'city': None,              'country': None,              'lat': None,              'lon': None,              'postal_code': None,              'region': None,              'store_number': None}, 'merchant_name': None, 'name': 'ANDREI AVETOV SERGEI MINAKOV FP 19/11/22 2125 P457SHRSL7HZKUA1EV', 'payment_channel': 'other', 'payment_meta': {'by_order_of': None,                  'payee': None,                  'payer': None,                  'payment_method': None,                  'payment_processor': None,                  'ppd_id': None,                  'reason': None,                  'reference_number': None}, 'pending': False, 'pending_transaction_id': None, 'personal_finance_category': None, 'transaction_code': None, 'transaction_id': '5aexxV0NmKUBZZY8J4w8Uk0dXeOwEwHm0AqaEq', 'transaction_type': 'place', 'unofficial_currency_code': None}, {'account_id': 'a9X88M4oEpfBMMjVpOEVUp0m8ykRZ6f3n58M3a', 'account_owner': None, 'amount': 1.99, 'authorized_date': datetime.date(2022, 11, 20), 'authorized_datetime': None, 'category': ['Food and Drink', 'Restaurants', 'Fast Food'], 'category_id': '13005032', 'check_number': None, 'date': datetime.date(2022, 11, 21), 'datetime': datetime.datetime(2022, 11, 21, 0, 0, tzinfo=tzlocal()), 'iso_currency_code': 'GBP', 'location': {'address': None,              'city': None,              'country': None,              'lat': None,              'lon': None,              'postal_code': None,              'region': None,              'store_number': None}, 'merchant_name': "McDonald's", 'name': "McDonald's", 'payment_channel': 'in store', 'payment_meta': {'by_order_of': None,                  'payee': None,                  'payer': None,                  'payment_method': None,                  'payment_processor': None,                  'ppd_id': None,                  'reason': None,                  'reference_number': None}, 'pending': False, 'pending_transaction_id': None, 'personal_finance_category': None, 'transaction_code': 'purchase', 'transaction_id': '0v5yyomk0PFL44oxNk9xt8Y3A0PwxwfBgjbz1P', 'transaction_type': 'place', 'unofficial_currency_code': None}, {'account_id': 'a9X88M4oEpfBMMjVpOEVUp0m8ykRZ6f3n58M3a', 'account_owner': None, 'amount': 15.99, 'authorized_date': datetime.date(2022, 11, 19), 'authorized_datetime': None, 'category': ['Service', 'Subscription'], 'category_id': '18061000', 'check_number': None, 'date': datetime.date(2022, 11, 21), 'datetime': datetime.datetime(2022, 11, 21, 0, 0, tzinfo=tzlocal()), 'iso_currency_code': 'GBP', 'location': {'address': None,              'city': None,              'country': None,              'lat': None,              'lon': None,              'postal_code': None,              'region': None,              'store_number': None}, 'merchant_name': 'Netflix', 'name': 'Netflix', 'payment_channel': 'online', 'payment_meta': {'by_order_of': None,                  'payee': None,                  'payer': None,                  'payment_method': None,                  'payment_processor': None,                  'ppd_id': None,                  'reason': None,                  'reference_number': None}, 'pending': False, 'pending_transaction_id': None, 'personal_finance_category': None, 'transaction_code': 'purchase', 'transaction_id': 'jD0eeYgjEmfrLLbe8BaeTeEOBxVYmYTk0wLoq0', 'transaction_type': 'place', 'unofficial_currency_code': None}, {'account_id': 'a9X88M4oEpfBMMjVpOEVUp0m8ykRZ6f3n58M3a', 'account_owner': None, 'amount': 20.0, 'authorized_date': datetime.date(2022, 11, 20), 'authorized_datetime': None, 'category': ['Food and Drink', 'Restaurants'], 'category_id': '13005000', 'check_number': None, 'date': datetime.date(2022, 11, 21), 'datetime': datetime.datetime(2022, 11, 21, 0, 0, tzinfo=tzlocal()), 'iso_currency_code': 'GBP', 'location': {'address': None,              'city': None,              'country': None,              'lat': None,              'lon': None,              'postal_code': None,              'region': None,              'store_number': None}, 'merchant_name': None, 'name': 'THAI THAI PLACE VIA MOBILE - LVP FP 20/11/22 10 39142730062162000N', 'payment_channel': 'in store', 'payment_meta': {'by_order_of': None,                  'payee': None,                  'payer': None,                  'payment_method': None,                  'payment_processor': None,                  'ppd_id': None,                  'reason': None,                  'reference_number': None}, 'pending': False, 'pending_transaction_id': None, 'personal_finance_category': None, 'transaction_code': 'transfer', 'transaction_id': 'Z83BBoKQEVtwooLxZ4XxIbe50dQMPMFPKL0dy6', 'transaction_type': 'place', 'unofficial_currency_code': None}]

    def test_monthly_spending_in_year(self):
        annualMonthlySpending = BankGraphData(self.transaction_history)
        self.assertEqual(annualMonthlySpending.monthlySpendingInYear(2022), [{'Jan': 0},{'Feb': 0},{'Mar': 0},{'Apr': 0},{'May': 0},{'Jun': 0},{'Jul': 0},{'Aug': 0},{'Sep': 0},{'Oct': 0},{'Nov': 41.28},{'Dec': 0}])

    def test_no_monthly_spending_in_year(self):
        annualMonthlySpending = BankGraphData("")
        self.assertEqual(annualMonthlySpending.monthlySpendingInYear(2022), [{'Jan': 0},{'Feb': 0},{'Mar': 0},{'Apr': 0},{'May': 0},{'Jun': 0},{'Jul': 0},{'Aug': 0},{'Sep': 0},{'Oct': 0},{'Nov': 0},{'Dec': 0}])

    def test_weekly_spending_in_month(self):
        annualMonthlySpending = BankGraphData(self.transaction_history)
        self.assertEqual(annualMonthlySpending.weeklySpendingInYear(11,2022), [{'Week 1': 0}, {'Week 2': 0}, {'Week 3': 41.28}, {'Week 4': 0}, {'Week 5': 0}])

    def test_no_weekly_spending_in_month(self):
        annualMonthlySpending = BankGraphData("")
        self.assertEqual(annualMonthlySpending.weeklySpendingInYear(11,2022), [{'Week 1': 0}, {'Week 2': 0}, {'Week 3': 0}, {'Week 4': 0}, {'Week 5': 0}])

    def test_weekly_spending_in_invalid_month(self):
        annualMonthlySpending = BankGraphData("")
        self.assertEqual(annualMonthlySpending.weeklySpendingInYear(13,2022), [{'Week 1': 0}, {'Week 2': 0}, {'Week 3': 0}, {'Week 4': 0}, {'Week 5': 0}])

    def test_ordered_categorised_monthly_spending(self):
        annualMonthlySpending = BankGraphData(self.transaction_history)
        self.assertEqual(annualMonthlySpending.orderedCategorisedMonthlySpending(11,2022), [('Food and Drink', 21.99), ('Service', 15.99), ('Travel', 3.3)])

    def test_ordered_categorised_weekly_spending(self):
        annualMonthlySpending = BankGraphData(self.transaction_history)
        self.assertEqual(annualMonthlySpending.orderedCategorisedWeeklySpending(3,11,2022), [('Food and Drink', 21.99), ('Service', 15.99), ('Travel', 3.3)])

    def test_no_ordered_categorised_monthly_spending(self):
        annualMonthlySpending = BankGraphData("")
        self.assertEqual(annualMonthlySpending.orderedCategorisedMonthlySpending(11,2022), [])

    def test_no_ordered_categorised_weekly_spending(self):
        annualMonthlySpending = BankGraphData("")
        self.assertEqual(annualMonthlySpending.orderedCategorisedWeeklySpending(3,11,2022), [])

    def test_ordered_categorised_monthly_spending_for_invalid_month(self):
        annualMonthlySpending = BankGraphData("")
        self.assertEqual(annualMonthlySpending.orderedCategorisedMonthlySpending(13,2022), [])

    def test_no_ordered_categorised_weekly_spending_for_invalid_week(self):
        annualMonthlySpending = BankGraphData("")
        self.assertEqual(annualMonthlySpending.orderedCategorisedWeeklySpending(6,11,2022), [])
