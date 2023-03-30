import yfinance as yf
import pandas as pd
from datetime import datetime

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
            raise TickerNotSupported(ticker_symbol)
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

    def get_stock_history_for_period(self, ticker_symbol, period):
        try:
            ticker = yf.Ticker(ticker_symbol)
            history = ticker.history(prepost = False, raise_errors = True, period=str(period)+'mo')
            close_data = history['Close'].to_dict()
        except Exception:
            raise TickerNotSupported()
        dict_with_datetimes = {}
        for key in close_data.keys():
            dict_with_datetimes[key.to_pydatetime().strftime('%Y-%m-%d')] = close_data[key]
        return dict_with_datetimes
    
    def getIndexValues(self, index_ticker, time_period="6mo"):
        # Tickers = ^GSPC - sp500, ^ftse - ftse100, ^dji - dow, ^STOXX50E - eurostoxx50, ^GDAXI - dax
        INDICES = ["^GSPC","^FTSE", "^DJI", "^STOXX50E", "^GDAXI"]
        if(index_ticker in INDICES):
            try:
                ticker = yf.Ticker(index_ticker)
                history = ticker.history(period=time_period, interval="1d")
                close = history['Close'].to_dict()
            except Exception:
                raise TickerNotSupported()
        else:
            raise TickerNotSupported()

        dict_with_datetimes = {}
        for key in close.keys():
            dict_with_datetimes[key.to_pydatetime().strftime('%Y-%m-%d')] = close[key]
        return dict_with_datetimes

    def getDayDelta(self, initial_amount, data):
        keys = list(data.keys())
        values = list(data.values())
        for i in range(values.len()-1):
            data.update({(keys[i+1]) : (initial_amount * (values[i+1]-values[i])/(values[i]))})
        
        return data

    def is_ticker_supported(self, ticker):
        try:
            history = self.get_stock_history(ticker)
        except TickerNotSupported:
            return False
        
        return len(history) > 0