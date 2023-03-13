from django.test import TestCase
from assetManager.API_wrappers.yfinance_wrapper import YFinanceWrapper, TickerNotSupported
from datetime import datetime

class YFinanceWrapperTestCase(TestCase):
    def setUp(self):
        self.ticker = 'MSFT' # ticker name for Microsoft
        self.wrapper = YFinanceWrapper()

    def test_get_ticker_info_returns_prices_for_stock(self):
        data = self.wrapper.get_stock_history(self.ticker)
        self.assertIsNotNone(data)

    def test_get_ticker_info_throws_error_for_unlisted_stock(self):
        with self.assertRaises(TickerNotSupported):
            self.wrapper.get_stock_history('fdjio;aksop89ifaduj903427ukljdasnfiuahf9867239fhq32iuhfjkql3hf897qh')

    def test_get_most_recent_stock_price_returns_price_for_valid_stock(self):
        data = self.wrapper.get_most_recent_stock_price(self.ticker)
        self.assertIsNotNone(data)
        self.assertTrue(type(data) == float)

    def test_get_most_recent_prices_throws_error_for_unlisted_stock(self):
        with self.assertRaises(TickerNotSupported):
            self.wrapper.get_most_recent_stock_price('fdjio;aksop89ifaduj903427ukljdasnfiuahf9867239fhq32iuhfjkql3hf897qh')

    def test_get_stock_price_at_date_works(self):
        date = datetime(2022, 10, 10)
        data = self.wrapper.get_stock_price_at_date(self.ticker, date)
        self.assertEqual(int(data), 228)