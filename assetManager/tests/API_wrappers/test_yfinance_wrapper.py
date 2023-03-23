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

    def test_get_stock_history_for_period_works(self):
        data = self.wrapper.get_stock_history_for_period(self.ticker, 1)
        self.assertTrue(len(data) > 10)

    def test_get_indices_last_year_returns_values(self):
        data = self.wrapper.getIndexValues("^GSPC")
        self.assertIsNotNone(data)

    def test_index_in_available_list(self):
        with self.assertRaises(TickerNotSupported):
            self.wrapper.getIndexValues("SPY")

    def test_is_ticker_supported_works(self):
        data = self.wrapper.is_ticker_supported("AAPL")
        self.assertTrue(data)
