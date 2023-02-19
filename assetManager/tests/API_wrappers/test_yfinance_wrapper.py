from django.test import TestCase
from assetManager.API_wrappers.yfinance_wrapper import YFinanceWrapper

class YFinanceWrapperTestCase(TestCase):
    def setUp(self):
        self.ticker = 'MSFT' # ticker name for Microsoft
        self.wrapper = YFinanceWrapper()

    def test_get_ticker_info_returns_prices_for_stock(self):
        data = self.wrapper.get_stock_history(self.ticker)
        self.assertIsNotNone(data)

    def test_get_ticker_info_throws_error_for_unlisted_stock(self):
        with self.assertRaises(Exception):
            self.wrapper.get_stock_history('fdjio;aksop89ifaduj903427ukljdasnfiuahf9867239fhq32iuhfjkql3hf897qh')