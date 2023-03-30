from assetManager.transactionInsight.bank_graph_data import BankGraphData,create_forex_rates,get_currency_converter
from dateutil.tz import tzlocal
import datetime
from django.conf import settings
from django.test import TestCase
from datetime import date

class CreateBankGraphDataTestCase(TestCase):
    def setUp(self):
        settings.PLAID_DEVELOPMENT = False
        self.transaction_history = [{'account_id': 'a9X88M4oEpfBMMjVpOEVUp0m8ykRZ6f3n58M3a', 'account_owner': None, 'amount': 3.3, 'authorized_date': datetime.date(2022, 11, 18), 'authorized_datetime': None, 'category': ['Travel', 'Public Transportation Services'], 'category_id': '22014000', 'check_number': None, 'date': datetime.date(2022, 11, 21), 'datetime': datetime.datetime(2022, 11, 21, 0, 0, tzinfo=tzlocal()), 'iso_currency_code': 'GBP', 'location': {'address': None,              'city': None,              'country': None,              'lat': None,              'lon': None,              'postal_code': None,              'region': None,              'store_number': None}, 'merchant_name': 'Transport for London', 'name': '9114 18NOV22 CD TFL TRAVEL CH TFL.GOV.UK/CP GB', 'payment_channel': 'online', 'payment_meta': {'by_order_of': None,                  'payee': None,                  'payer': None,                  'payment_method': None,                  'payment_processor': None,                  'ppd_id': None,                  'reason': None,                  'reference_number': None}, 'pending': False, 'pending_transaction_id': None, 'personal_finance_category': None, 'transaction_code': 'purchase', 'transaction_id': 'rkKAAqQRMeSMrrEj0PejH694dNqzKzCj3gvMOq', 'transaction_type': 'place', 'unofficial_currency_code': None}, {'account_id': 'a9X88M4oEpfBMMjVpOEVUp0m8ykRZ6f3n58M3a', 'account_owner': None, 'amount': -40.0, 'authorized_date': datetime.date(2022, 11, 19), 'authorized_datetime': None, 'category': ['Shops', 'Supermarkets and Groceries'], 'category_id': '19047000', 'check_number': None, 'date': datetime.date(2022, 11, 21), 'datetime': datetime.datetime(2022, 11, 21, 0, 0, tzinfo=tzlocal()), 'iso_currency_code': 'GBP', 'location': {'address': None,              'city': None,              'country': None,              'lat': None,              'lon': None,              'postal_code': None,              'region': None,              'store_number': None}, 'merchant_name': None, 'name': 'ANDREI AVETOV SERGEI MINAKOV FP 19/11/22 2125 P457SHRSL7HZKUA1EV', 'payment_channel': 'other', 'payment_meta': {'by_order_of': None,                  'payee': None,                  'payer': None,                  'payment_method': None,                  'payment_processor': None,                  'ppd_id': None,                  'reason': None,                  'reference_number': None}, 'pending': False, 'pending_transaction_id': None, 'personal_finance_category': None, 'transaction_code': None, 'transaction_id': '5aexxV0NmKUBZZY8J4w8Uk0dXeOwEwHm0AqaEq', 'transaction_type': 'place', 'unofficial_currency_code': None}, {'account_id': 'a9X88M4oEpfBMMjVpOEVUp0m8ykRZ6f3n58M3a', 'account_owner': None, 'amount': 1.99, 'authorized_date': datetime.date(2022, 11, 20), 'authorized_datetime': None, 'category': ['Food and Drink', 'Restaurants', 'Fast Food'], 'category_id': '13005032', 'check_number': None, 'date': datetime.date(2022, 11, 21), 'datetime': datetime.datetime(2022, 11, 21, 0, 0, tzinfo=tzlocal()), 'iso_currency_code': 'GBP', 'location': {'address': None,              'city': None,              'country': None,              'lat': None,              'lon': None,              'postal_code': None,              'region': None,              'store_number': None}, 'merchant_name': "McDonald's", 'name': "McDonald's", 'payment_channel': 'in store', 'payment_meta': {'by_order_of': None,                  'payee': None,                  'payer': None,                  'payment_method': None,                  'payment_processor': None,                  'ppd_id': None,                  'reason': None,                  'reference_number': None}, 'pending': False, 'pending_transaction_id': None, 'personal_finance_category': None, 'transaction_code': 'purchase', 'transaction_id': '0v5yyomk0PFL44oxNk9xt8Y3A0PwxwfBgjbz1P', 'transaction_type': 'place', 'unofficial_currency_code': None}, {'account_id': 'a9X88M4oEpfBMMjVpOEVUp0m8ykRZ6f3n58M3a', 'account_owner': None, 'amount': 15.99, 'authorized_date': datetime.date(2022, 11, 19), 'authorized_datetime': None, 'category': ['Service', 'Subscription'], 'category_id': '18061000', 'check_number': None, 'date': datetime.date(2022, 11, 21), 'datetime': datetime.datetime(2022, 11, 21, 0, 0, tzinfo=tzlocal()), 'iso_currency_code': 'GBP', 'location': {'address': None,              'city': None,              'country': None,              'lat': None,              'lon': None,              'postal_code': None,              'region': None,              'store_number': None}, 'merchant_name': 'Netflix', 'name': 'Netflix', 'payment_channel': 'online', 'payment_meta': {'by_order_of': None,                  'payee': None,                  'payer': None,                  'payment_method': None,                  'payment_processor': None,                  'ppd_id': None,                  'reason': None,                  'reference_number': None}, 'pending': False, 'pending_transaction_id': None, 'personal_finance_category': None, 'transaction_code': 'purchase', 'transaction_id': 'jD0eeYgjEmfrLLbe8BaeTeEOBxVYmYTk0wLoq0', 'transaction_type': 'place', 'unofficial_currency_code': None}, {'account_id': 'a9X88M4oEpfBMMjVpOEVUp0m8ykRZ6f3n58M3a', 'account_owner': None, 'amount': 20.0, 'authorized_date': datetime.date(2022, 11, 20), 'authorized_datetime': None, 'category': ['Food and Drink', 'Restaurants'], 'category_id': '13005000', 'check_number': None, 'date': datetime.date(2022, 11, 21), 'datetime': datetime.datetime(2022, 11, 21, 0, 0, tzinfo=tzlocal()), 'iso_currency_code': 'GBP', 'location': {'address': None,              'city': None,              'country': None,              'lat': None,              'lon': None,              'postal_code': None,              'region': None,              'store_number': None}, 'merchant_name': None, 'name': 'THAI THAI PLACE VIA MOBILE - LVP FP 20/11/22 10 39142730062162000N', 'payment_channel': 'in store', 'payment_meta': {'by_order_of': None,                  'payee': None,                  'payer': None,                  'payment_method': None,                  'payment_processor': None,                  'ppd_id': None,                  'reason': None,                  'reference_number': None}, 'pending': False, 'pending_transaction_id': None, 'personal_finance_category': None, 'transaction_code': 'transfer', 'transaction_id': 'Z83BBoKQEVtwooLxZ4XxIbe50dQMPMFPKL0dy6', 'transaction_type': 'place', 'unofficial_currency_code': None}]

    def test_company_spending_per_sector(self):
        companySpending = BankGraphData(self.transaction_history)
        self.assertEqual(companySpending.companySpendingPerSector('Food and Drink'), [{'name': "McDonald's", 'value': 1.99},{'name': 'THAI THAI PLACE VIA MOBILE - LVP FP 20/11/22 10 39142730062162000N','value': 20.0}])

    def test_company_spending_per_fake_sector(self):
        companySpending = BankGraphData(self.transaction_history)
        self.assertEqual(companySpending.companySpendingPerSector('Fake Sector'), [])

    def test_company_spending_per_no_sector(self):
        companySpending = BankGraphData(self.transaction_history)
        self.assertEqual(companySpending.companySpendingPerSector(''), [])

    def test_no_company_spending_per_no_sector(self):
        companySpending = BankGraphData("")
        self.assertEqual(companySpending.companySpendingPerSector(''), [])

    def test_ordered_categorised_spending(self):
        categorisedSpending = BankGraphData(self.transaction_history)
        self.assertEqual(categorisedSpending.orderedCategorisedSpending(), [{'name': 'Food and Drink', 'value': 21.99},{'name': 'Service', 'value': 15.99},{'name': 'Travel', 'value': 3.3}])

    def test_no_ordered_categorised_spending(self):
        categorisedSpending = BankGraphData("")
        self.assertEqual(categorisedSpending.orderedCategorisedSpending(), [])

    def test_yearly_spending_in_year(self):
        annualSpending = BankGraphData(self.transaction_history)
        self.assertEqual(annualSpending.yearlySpending(), [{'name': '2022', 'value': 41.28}])

    def test_no_yearly_spending_in_year(self):
        annualSpending = BankGraphData("")
        self.assertEqual(annualSpending.yearlySpending(), [])

    def test_monthly_spending_in_year(self):
        annualMonthlySpending = BankGraphData(self.transaction_history)
        self.assertEqual(annualMonthlySpending.monthlySpendingInYear(2022), [{'name': 'Jan 2022', 'value': 0},{'name': 'Feb 2022', 'value': 0},{'name': 'Mar 2022', 'value': 0},{'name': 'Apr 2022', 'value': 0},{'name': 'May 2022', 'value': 0},{'name': 'Jun 2022', 'value': 0},{'name': 'Jul 2022', 'value': 0},{'name': 'Aug 2022', 'value': 0},{'name': 'Sep 2022', 'value': 0},{'name': 'Oct 2022', 'value': 0},{'name': 'Nov 2022', 'value': 41.28},{'name': 'Dec 2022', 'value': 0}])

    def test_no_monthly_spending_in_year(self):
        annualMonthlySpending = BankGraphData("")
        self.assertEqual(annualMonthlySpending.monthlySpendingInYear(2022), [{'name': 'Jan 2022', 'value': 0},{'name': 'Feb 2022', 'value': 0},{'name': 'Mar 2022', 'value': 0},{'name': 'Apr 2022', 'value': 0},{'name': 'May 2022', 'value': 0},{'name': 'Jun 2022', 'value': 0},{'name': 'Jul 2022', 'value': 0},{'name': 'Aug 2022', 'value': 0},{'name': 'Sep 2022', 'value': 0},{'name': 'Oct 2022', 'value': 0},{'name': 'Nov 2022', 'value': 0},{'name': 'Dec 2022', 'value': 0}])

    def test_weekly_spending_in_month(self):
        annualWeeklySpending = BankGraphData(self.transaction_history)
        self.assertEqual(annualWeeklySpending.weeklySpendingInYear("Nov 2022"), [{'name': 'Week 1', 'value': 0},{'name': 'Week 2', 'value': 0},{'name': 'Week 3', 'value': 41.28},{'name': 'Week 4', 'value': 0},{'name': 'Week 5', 'value': 0}])

    def test_no_weekly_spending_in_month(self):
        annualWeeklySpending = BankGraphData("")
        self.assertEqual(annualWeeklySpending.weeklySpendingInYear("Jan 2022"), [{'name': 'Week 1', 'value': 0},{'name': 'Week 2', 'value': 0},{'name': 'Week 3', 'value': 0},{'name': 'Week 4', 'value': 0},{'name': 'Week 5', 'value': 0}])

    def test_ordered_categorised_monthly_spending(self):
        annualMonthlySpending = BankGraphData(self.transaction_history)
        self.assertEqual(annualMonthlySpending.orderedCategorisedMonthlySpending(11,2022), [{'name': 'Food and Drink', 'value': 21.99},{'name': 'Service', 'value': 15.99},{'name': 'Travel', 'value': 3.3}])

    def test_ordered_categorised_weekly_spending(self):
        annualWeeklySpending = BankGraphData(self.transaction_history)
        self.assertEqual(annualWeeklySpending.orderedCategorisedWeeklySpending(3,11,2022), [{'name': 'Food and Drink', 'value': 21.99},{'name': 'Service', 'value': 15.99},{'name': 'Travel', 'value': 3.3}])

    def test_no_ordered_categorised_monthly_spending(self):
        annualMonthlySpending = BankGraphData("")
        self.assertEqual(annualMonthlySpending.orderedCategorisedMonthlySpending(11,2022), [])

    def test_no_ordered_categorised_weekly_spending(self):
        annualWeeklySpending = BankGraphData("")
        self.assertEqual(annualWeeklySpending.orderedCategorisedWeeklySpending(3,11,2022), [])

    def test_ordered_categorised_monthly_spending_for_invalid_month(self):
        annualMonthlySpending = BankGraphData("")
        self.assertEqual(annualMonthlySpending.orderedCategorisedMonthlySpending(13,2022), [])

    def test_no_ordered_categorised_weekly_spending_for_invalid_week(self):
        annualWeeklySpending = BankGraphData("")
        self.assertEqual(annualWeeklySpending.orderedCategorisedWeeklySpending(6,11,2022), [])

    def test_get_month(self):
        testObject = BankGraphData("")
        self.assertEqual(testObject.getMonth("Jan"), 1)

    def test_create_forex_rates_in_sandbox_environment_correctly_without_saved_data_fallback(self):
        input_date = get_currency_converter()
        self.assertEqual(input_date,datetime.date(2014, 5, 23))
        rates = create_forex_rates(input_date)
        self.assertEqual(len(list(rates.keys())),33)
        self.assertTrue('EUR' in list(rates.keys()))
        self.assertTrue('USD' in list(rates.keys()))
        self.assertTrue('JPY' in list(rates.keys()))
        self.assertTrue('GBP' in list(rates.keys()))
        self.assertTrue('CHF' in list(rates.keys()))
        self.assertTrue('NOK' in list(rates.keys()))
        self.assertTrue('AUD' in list(rates.keys()))
        self.assertTrue('CAD' in list(rates.keys()))
        self.assertTrue('INR' in list(rates.keys()))
        self.assertEqual(rates['EUR'],1.2355593995181318)
        self.assertEqual(rates['USD'],1.6840674615432136)
        self.assertEqual(rates['JPY'],171.64391178105885)
        self.assertEqual(rates['GBP'],1)
        self.assertEqual(rates['CHF'],1.5086180268116391)
        self.assertEqual(rates['NOK'],10.045715697782171)
        self.assertEqual(rates['AUD'],1.8264039043677025)
        self.assertEqual(rates['CAD'],1.8357941558040403)
        self.assertEqual(rates['INR'],98.53240254525237)

    def test_create_forex_rates_in_development_environment_correctly_without_saved_data_fallback(self):
        old_input_date = get_currency_converter()
        self.assertEqual(old_input_date,datetime.date(2014, 5, 23))
        old_rates = create_forex_rates(old_input_date)
        self.assertEqual(len(list(old_rates.keys())),33)
        settings.PLAID_DEVELOPMENT = True
        input_date = get_currency_converter()
        self.assertEqual(input_date,date.today())
        rates = create_forex_rates(input_date)
        self.assertEqual(len(list(rates.keys())),30)
        self.assertTrue('EUR' in list(rates.keys()))
        self.assertTrue('USD' in list(rates.keys()))
        self.assertTrue('JPY' in list(rates.keys()))
        self.assertTrue('GBP' in list(rates.keys()))
        self.assertTrue('CHF' in list(rates.keys()))
        self.assertTrue('NOK' in list(rates.keys()))
        self.assertTrue('AUD' in list(rates.keys()))
        self.assertTrue('CAD' in list(rates.keys()))
        self.assertTrue('INR' in list(rates.keys()))

        self.assertNotEqual(rates['INR'],old_rates['INR'])
        self.assertNotEqual(rates['USD'],old_rates['USD'])
        self.assertNotEqual(rates['EUR'],old_rates['EUR'])
        self.assertNotEqual(rates['JPY'],old_rates['JPY'])
        self.assertEqual(rates['GBP'],old_rates['GBP'])
        self.assertNotEqual(rates['CHF'],old_rates['CHF'])
        self.assertNotEqual(rates['NOK'],old_rates['NOK'])
        self.assertNotEqual(rates['AUD'],old_rates['AUD'])
        self.assertNotEqual(rates['CAD'],old_rates['CAD'])

    def test_create_forex_rates_force_exception(self):
        rates = create_forex_rates('incorrect_date')
        self.assertEqual(len(list(rates.keys())),30)
        self.assertEqual(rates,{'EUR': 1.1371648206691076, 'USD': 1.2328003820873799, 'JPY': 161.12488344060586, 'BGN': 2.224066956264641, 'CZK': 26.914416975596442, 'DKK': 8.470968182128317, 'HUF': 435.4772680752348, 'PLN': 5.323637107962427, 'RON': 5.631581341399622, 'SEK': 12.758420705497054, 'CHF': 1.1311378471195614, 'ISK': 168.41410994109484, 'NOK': 12.877254429256975, 'TRY': 23.556710409606765, 'AUD': 1.8443676226432257, 'BRL': 6.377220314312356, 'CAD': 1.68334508403648, 'CNY': 8.478018604016466, 'HKD': 9.677272623894106, 'IDR': 18596.511178330187, 'INR': 101.2804475880734, 'KRW': 1601.0598376128635, 'MXN': 22.56009916077236, 'MYR': 5.426209374786781, 'NZD': 1.976619891287043, 'PHP': 67.03700334326457, 'SGD': 1.6368350428711136, 'THB': 42.24794741749869, 'ZAR': 22.40544474516136, 'GBP': 1})
