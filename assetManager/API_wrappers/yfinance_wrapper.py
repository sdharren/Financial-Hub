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
    
    def getIndexValues(self, index_ticker, time_period="6mo"):
        # tickers = ^GSPC - sp500, ^ftse - ftse100, ^dji - dow, ^STOXX50E - eurostoxx50, ^GDAXI - dax
        INDICES = ["^GSPC","^FTSE", "^DJI", "^STOXX50E", "^GDAXI"]
        if(index_ticker in INDICES):
            try:
                ticker = yf.ticker(index_ticker)
                history = ticker.history(period=time_period, interval="1d")
                close = history['Close'].to_dict()
            except Exception:
                raise TickerNotSupported()
        else:
            raise TickerNotSupported()
        return close

    
    