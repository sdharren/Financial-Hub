import yfinance as yf
import pandas as pd

class TickerNotSupported(Exception):
    pass

class YFinanceWrapper():
    # Returns a dictionary of the form {date: close price}
    # Retrieves data for the maximum period available
    def get_stock_history(self, ticker_symbol):
        try:
            ticker = yf.Ticker(ticker_symbol)
            history = ticker.history(prepost = False, raise_errors = True)
            close_data = history['Close'].to_dict()
        except Exception:
            raise TickerNotSupported()
        return close_data

    def get_most_recent_stock_price(self, ticker_symbol):
        try:
            ticker = yf.Ticker(ticker_symbol)
            history = ticker.history(prepost = False, raise_errors = True, period='1d')
            close_data = history['Close'].to_dict()
            price = list(close_data.values())[0]
        except Exception:
            raise TickerNotSupported()
        return price

    
    