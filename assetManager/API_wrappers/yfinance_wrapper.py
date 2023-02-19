import yfinance as yf
import pandas as pd

class InvalidTickerName(Exception):
    pass

class YFinanceWrapper():
    # Returns a dictionary of the form {date: close price}
    # Retrieves data for the maximum period available
    def get_stock_history(self, ticker_name):
        ticker = yf.Ticker(ticker_name)
        history = ticker.history(prepost = False)
        close_data = history['Close'].to_dict()
        if not close_data:
            raise InvalidTickerName()
        return close_data

    
    