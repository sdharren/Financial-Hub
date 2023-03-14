from assetManager.API_wrappers.plaid_wrapper import PublicTokenNotExchanged
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
from plaid.model.investments_transactions_get_request import InvestmentsTransactionsGetRequest
import json
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from assetManager.investments.investment import Investment
from assetManager.investments.transaction import Transaction
from assetManager.API_wrappers.yfinance_wrapper import YFinanceWrapper, TickerNotSupported
from operator import attrgetter

class TransactionsNotDefined(Exception):
    pass

class InvestmentsNotDefined(Exception):
    pass

class InvestmentsNotLinked(Exception):
    pass

class StocksGetter():
    def __init__(self, concrete_wrapper):
        self.wrapper = concrete_wrapper
        self.investments = []
        self.transactions = []
        self.yfinance_wrapper = YFinanceWrapper()

    # Sends API calls to plaid requesting investment info for each access token associated with user
    def query_investments(self, user):
        unformatted_investments = []
        try:
            access_tokens = self.wrapper.retrieve_access_tokens(user, 'investments')
        except PublicTokenNotExchanged:
            raise InvestmentsNotLinked()
        for token in access_tokens:
            request = InvestmentsHoldingsGetRequest(access_token=token)
            response = self.wrapper.client.investments_holdings_get(request)
            unformatted_investments.append(response)
        self.format_investments(unformatted_investments)

    def query_transactions(self, user, start_date, end_date):
        #TODO: error handling for no access tokens
        access_tokens = self.wrapper.retrieve_access_tokens(user, 'investments')
        for token in access_tokens:
            request = InvestmentsTransactionsGetRequest(
                access_token=token,
                start_date=date.fromisoformat(start_date),
                end_date=date.fromisoformat(end_date),
            )
            response = self.wrapper.client.investments_transactions_get(request)
            self.format_transactions(response)

    def format_transactions(self, unformatted_transactions):
        for transaction in unformatted_transactions['investment_transactions']:
            if str(transaction['type']) == 'buy':
                for security in unformatted_transactions['securities']:
                    if security['security_id'] == transaction['security_id']:
                        ticker = security['ticker_symbol']
                        break
                self.transactions.append(Transaction(transaction, ticker))

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
        serialized_data = {}
        for key in data:
            serialized_data[key.isoformat()] = data[key]
        return serialized_data

    # Returns a dictionary - {ticker: price_diff} where price_diff is diff * number of stocks
    def get_return_on_buy_orders(self):
        if not bool(self.transactions):
            raise TransactionsNotDefined()
        returns = defaultdict(float)
        for order in self.transactions:
            if order.ticker is not None and order.type == 'buy':
                try:
                    price_today = self.yfinance_wrapper.get_most_recent_stock_price(order.ticker)
                    returns[order.ticker] = (price_today - order.price) * order.quantity
                except TickerNotSupported:
                    continue
        return returns

    # Returns a dictionary - {ticker: total diff} where total diff is current total value - original total value
    # Stocks with the same ticker share a return sum e.g. 2 shares AAPL @ $20 and 3 shares AAPL @ $10
    # with current price $40 will have a shared return of $140
    def get_return_on_current_holdings(self):
        if not bool(self.investments):
            raise InvestmentsNotDefined()
        returns = defaultdict(float)
        for investment in self.investments:
            if investment.get_ticker() is not None:
                try:
                    price_today = self.yfinance_wrapper.get_most_recent_stock_price(investment.ticker)
                    returns[investment.get_ticker()] += price_today * investment.get_quantity() - investment.get_total_price()
                except TickerNotSupported:
                    continue
        return returns

    # Returns a dictionary - {category: total_price}
    def get_investment_category(self, category):
        category_dict = defaultdict(float)
        for investment in self.investments:
            if investment.get_category() == category:
                # maybe get quantity and multiply by current price? need to know if plaid updates data freqeuntly or at all
                category_dict[investment.get_name()] += investment.get_total_price()
        return category_dict
    
    # Returns the stock ticker for associated with a name if one exists
    def get_stock_ticker(self, stock_name):
        for investment in self.investments:
            if investment.get_name() == stock_name:
                return investment.get_ticker()
        return 'Cannot get stock ticker for ' + stock_name
    
    # Returns the day-by-day portfolio history for a specified period in months (only 1, 3, 6 months accepted)
    # The return is a dict of the form {date: portfolio vaue}
    def get_portfolio_history(self, months=6):
        end_date = date.today()
        start_date = end_date - relativedelta(months=months)
        
        portfolio_history = defaultdict(float)
        stock_histories = []

        for investment in self.investments:
            if investment.get_ticker() is not None:
                try:
                    stock_history = self.yfinance_wrapper.get_stock_history_for_period(investment.get_ticker(), months)
                except TickerNotSupported:
                    continue
                stock_histories.append(stock_history)

        for current_date in (start_date + timedelta(days=n) for n in range(months*31)):
            current_sum = 0
            skipDay = False
            for stock_history in stock_histories:
                try:
                    current_sum += stock_history[current_date.strftime('%Y-%m-%d')]
                except KeyError: # key error means it's a weekend so there is no price data
                    skipDay = True
                    break
            if not skipDay:
                portfolio_history[current_date.strftime('%Y-%m-%d')] = current_sum
        return portfolio_history

    def get_first_supported_stock(self):
        for investment in self.investments:
            if investment.get_category() == 'equity' and self.is_ticker_supported(investment.get_ticker()):
                return investment.get_name()

    def get_first_category(self):
        return self.investments[0].get_category()

    def is_ticker_supported(self, ticker):
        return self.yfinance_wrapper.is_ticker_supported(ticker)
