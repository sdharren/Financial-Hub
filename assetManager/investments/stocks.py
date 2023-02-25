from assetManager.API_wrappers.plaid_wrapper import PublicTokenNotExchanged
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
from plaid.model.investments_transactions_get_request import InvestmentsTransactionsGetRequest
import json
from datetime import date
from collections import defaultdict
from assetManager.investments.investment import Investment
from assetManager.investments.transaction import Transaction
from assetManager.API_wrappers.yfinance_wrapper import YFinanceWrapper, TickerNotSupported

class TransactionsNotDefined(Exception):
    pass

class StocksGetter():
    def __init__(self, concrete_wrapper):
        self.wrapper = concrete_wrapper
        self.investments = []
        self.buy_orders = []
        self.yfinance_wrapper = YFinanceWrapper()

    # Sends API calls to plaid requesting investment info for each access token associated with user
    def query_investments(self, user):
        unformatted_investments = []
        access_tokens = self.wrapper.retrieve_access_tokens(user, 'investments')
        for token in access_tokens:
            request = InvestmentsHoldingsGetRequest(access_token=token)
            response = self.wrapper.client.investments_holdings_get(request)
            unformatted_investments.append(response)
        self.format_investments(unformatted_investments)

    def query_transactions(self, user, start_date, end_date):
        access_tokens = self.wrapper.retrieve_access_tokens(user, 'investments')
        for token in access_tokens:
            request = InvestmentsTransactionsGetRequest(
                access_token=token,
                start_date=date.fromisoformat(start_date),
                end_date=date.fromisoformat(end_date),
            )
            response = self.wrapper.client.investments_transactions_get(request)
            self.make_buy_orders(response)

    def make_buy_orders(self, unformatted_transactions):
        for transaction in unformatted_transactions['investment_transactions']:
            shouldSkip = False
            if str(transaction['type']) == 'buy':
                for security in unformatted_transactions['securities']:
                    if security['security_id'] == transaction['security_id']:
                        ticker = security['ticker_symbol']
                        if security['type'] != 'equity' and security['type'] != 'etf':
                            shouldSkip = True
                        break
                if not shouldSkip:
                    self.buy_orders.append(Transaction(transaction, ticker))

    def format_investments(self, unformatted_investments):
        for current_investment in unformatted_investments:
            for holding in current_investment['holdings']:
                security_id = holding['security_id']
                for security in current_investment['securities']:
                    if security['security_id'] == security_id:
                        self.investments.append(Investment(holding, security))
                        break

    #Returns total investment sum within the account
    def get_total_investment_sum(self):
        total = 0
        for investment in self.investments:
            total += investment.get_total_price()
        return total

    # Returns the monetary total of investments categorised by their type - {type: total_sum}
    def get_investment_categories(self):
        categories = defaultdict(int)
        for investment in self.investments:
            categories[investment.get_category()] += investment.get_total_price()
        return categories

    # Returns a dictionary - {stock_ticker: total_price}
    # The total for all stocks can be calculated by the front-end by summing up all the prices in the returned dict
    def get_stocks(self):
        stocks = defaultdict(int)
        for investment in self.investments:
            category = investment.get_category()
            # only equity and ETFs are considered stocks (i.e. ignoring derivatives)
            if category == 'equity' or category == 'etf':
                stocks[investment.get_ticker()] = investment.get_total_price()
        return stocks

    # Returns a dictionary - {date: close_price} for a specific stock
    def get_stock_history(self, ticker):
        data = self.yfinance_wrapper.get_stock_history(ticker)
        return data

    # Returns a dictionary - {ticker: price_diff} where price_diff is diff * number of stocks
    def get_return_on_buy_orders(self):
        if not bool(self.buy_orders):
            raise TransactionsNotDefined()
        returns = defaultdict(float)
        for order in self.buy_orders:
            if order.ticker is not None:
                try:
                    price_today = self.yfinance_wrapper.get_most_recent_stock_price(order.ticker)
                    returns[order.ticker] = (price_today - order.price) * order.quantity
                except TickerNotSupported:
                    continue
        return returns

    #debuggining function
    def print_buy_orders(self):
        for order in self.buy_orders:
            print("Buy order for " + order.ticker + " at " + str(order.price) + " quantity - " + str(order.quantity))

