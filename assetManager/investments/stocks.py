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
from assetManager.transactionInsight.bank_graph_data import create_forex_rates


class TransactionsNotDefined(Exception):
    pass

class InvestmentsNotDefined(Exception):
    pass

class InvestmentsNotLinked(Exception):
    pass

class StocksGetter():
    def __init__(self, concrete_wrapper):
        self.wrapper = concrete_wrapper # used to query plaid
        self.investments = [] # holds user's investments
        self.transactions = [] # holds user's transactions
        self.yfinance_wrapper = YFinanceWrapper() # used to get stock info

    """
        @params:
            user (assetManager.models.User): The ID of the user whose investments will be queried.

        @description:
            Queries investments for a given user using the Plaid API. This method retrieves the access tokens
            for the user and then uses each token to make a request to retrieve the user's investment holdings.
            The responses are appended to a list and then passed to another method for formatting.

        @return:
            None.

        @raises:
            InvestmentsNotLinked: If the user has not linked their investment accounts, and therefore no access tokens can be retrieved.
    """
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

    """
    @params:
        user (str): The ID of the user whose transactions will be queried.
        start_date (str): The start date of the date range for which transactions will be queried. Must be in YYYY-MM-DD format.
        end_date (str): The end date of the date range for which transactions will be queried. Must be in YYYY-MM-DD format.

    @description:
        Queries transactions for a given user within a specified date range using the Plaid API. This method retrieves the access tokens
        for the user and then uses each token to make a request to retrieve the user's investment transactions. The responses are then
        passed to another method for formatting.

    @return:
        None.
    """
    def query_transactions(self, user, start_date, end_date):
        access_tokens = self.wrapper.retrieve_access_tokens(user, 'investments')
        for token in access_tokens:
            request = InvestmentsTransactionsGetRequest(
                access_token=token,
                start_date=date.fromisoformat(start_date),
                end_date=date.fromisoformat(end_date),
            )
            response = self.wrapper.client.investments_transactions_get(request)
            self.format_transactions(response)

    """
    @params:
        unformatted_transactions (dict): A dictionary containing the unformatted transaction data returned from the Plaid API.

    @description:
        Formats and saves in self.transactions unformatted investment transactions returned from the Plaid API. This method loops through each transaction and
        extracts the ticker symbol for the security involved in each 'buy' transaction. It then creates a new Transaction object
        with the formatted data and appends it to a list of formatted transactions.

    @return:
        None.
    """
    def format_transactions(self, unformatted_transactions):
        for transaction in unformatted_transactions['investment_transactions']:
            if str(transaction['type']) == 'buy':
                for security in unformatted_transactions['securities']:
                    if security['security_id'] == transaction['security_id']:
                        ticker = security['ticker_symbol']
                        break
                self.transactions.append(Transaction(transaction, ticker))

    """
    @params:
        unformatted_investments (list): A list containing unformatted investment data returned from the Plaid API.

    @description:
        Formats unformatted investment data returned from the Plaid API. This method loops through each investment holding and
        retrieves the security information for each holding. If the holding is not in USD, the institution value is converted to
        USD using the latest forex rates. The method then creates a new Investment object with the formatted data and appends it
        to a list of formatted investments.

    @return:
        None.
    """
    def format_investments(self, unformatted_investments):
        rates = create_forex_rates(date.today(), base='USD')
        for current_investment in unformatted_investments:
            for holding in current_investment['holdings']:
                security_id = holding['security_id']
                for security in current_investment['securities']:
                    if security['security_id'] == security_id:
                        if security['iso_currency_code'] != 'USD':
                            holding['institution_value'] = holding['institution_value'] / rates[security['iso_currency_code']]
                        self.investments.append(self.set_investment_returns(Investment(holding, security)))
                        break

    # Returns total sum of all investements the user holds
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

    """
    @params:
        None.

    @description:
        Calculates the return on the user's current holdings. This method loops through each Investment object in the list of
        investments and checks if it has a ticker symbol. If it does, the most recent stock price is retrieved for that ticker
        symbol using the yfinance API. The method then calculates the difference between the current value of the holding and the
        total price paid for the holding, and adds this difference to a running total for each ticker symbol. The method returns
        a dictionary containing the returns for each ticker symbol.

    @return:
        A dictionary containing the returns for each ticker symbol.

    """
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

    def get_index_history(self, ticker, period="6mo"):
        return self.yfinance_wrapper.getIndexValues(ticker, period)

    """
    @params:
        ticker: A string representing the ticker symbol of the index to compare the portfolio against.
        period: An integer representing the number of months of data to retrieve. Default is 6.

    @description:
        Compares the user's portfolio to the given stock market index. This method retrieves historical price data for both the
        user's portfolio and the given index using the yfinance API, and compares the value of the user's portfolio to the
        performance of the index over the specified period of time. The method returns a dictionary containing the value of the
        user's portfolio and the value of the index for each date during the specified period.

    @return:
        A dictionary containing the value of the user's portfolio and the value of the given index for each date during the
        specified period.
    """
    def get_portfolio_comparison(self, ticker, period=6):
        index_history = self.get_index_history(ticker, str(period) + 'mo')
        portfolio_history = self.get_portfolio_history(period)
        comparison = defaultdict(dict)

        n_index_units = list(portfolio_history.values())[0]/list(index_history.values())[0] # Calculate how many units of the index could have been bought at start (To normalise graph)
        
        for date in portfolio_history:
            try:
                current_index = index_history[date]
            except KeyError:
                continue
            else:
                comparison[date] = {
                    'portfolio': round(portfolio_history[date], 1),
                    'index': round(index_history[date] * n_index_units, 1)
                }
        return comparison
    
    # Returns user's investments that are supported by YFinance
    def get_supported_investments(self):
        stocks = set()
        for investment in self.investments:
            if investment.get_ticker() is not None and self.is_ticker_supported(investment.get_ticker()):
                stocks.add(investment.get_name())
        return stocks

    # Returns user's investment categories
    def get_categories(self):
        categories = set()
        for investment in self.investments:
            categories.add(investment.get_category())
        return categories

    def is_ticker_supported(self, ticker):
        return self.yfinance_wrapper.is_ticker_supported(ticker)

    """
    @params:
        investment: An Investment object representing the investment to calculate returns for.
    @description:
        Calculates the returns for a given investment by retrieving the price history of the investment's ticker over the past day
        using the yfinance API. The returns are calculated as the percentage difference between the investment's current price
        and the price on the previous day, 5 days ago, and 30 days ago. The returns are stored in a dictionary and added to the
        Investment object.
    @return:
        The Investment object with the returns dictionary added.
    """
    def set_investment_returns(self, investment):
        ticker = investment.get_ticker()
        returns = {}
        if ticker is not None:
            try:
                history = list(self.yfinance_wrapper.get_stock_history_for_period(ticker, 1).values())
            except TickerNotSupported:
                return investment
            else:
                history.reverse()
                current_price = history[0]
                returns['1'] = _calculate_percentage_diff(history[1], current_price)
                returns['5'] = _calculate_percentage_diff(history[5], current_price)
                returns['30'] = _calculate_percentage_diff(history[len(history)-1], current_price)
        investment.returns = returns
        return investment

    # Gets percentage returns of a given stock for 1, 5 and 30 days
    def get_returns(self, stock_name):
        for investment in self.investments:
            if investment.get_name() == stock_name:
                return investment.get_returns()
        return {}

    # Gets percentage returns of a given stock category for 1, 5 and 30 days
    def get_category_returns(self, category):
        returns = defaultdict(float)
        total = 0.0
        for investment in self.investments:
            if investment.get_category() == category and investment.get_returns() != {}:
                total += investment.get_total_price()
    
        for investment in self.investments:
            if investment.get_category() == category and investment.get_returns() != {}:
                weight = investment.get_total_price() / total
                returns['1'] += investment.get_returns()['1'] * weight
                returns['5'] += investment.get_returns()['5'] * weight
                returns['30'] += investment.get_returns()['30'] * weight
        if len(returns) > 0:
            returns['1'] = round(returns['1'], 1)
            returns['5'] = round(returns['5'], 1)
            returns['30'] = round(returns['30'], 1)
        return returns

    # Gets percentage returns of the whole portfolio for 1, 5 and 30 days
    def get_overall_returns(self):
        returns = defaultdict(float)
        total = 0.0
        for investment in self.investments:
            if investment.get_returns() != {}:
                total += investment.get_total_price()

        for investment in self.investments:
            if investment.get_returns() != {}:
                weight = investment.get_total_price() / total
                returns['1'] += investment.get_returns()['1'] * weight
                returns['5'] += investment.get_returns()['5'] * weight
                returns['30'] += investment.get_returns()['30'] * weight
        if len(returns) > 0:
            returns['1'] = round(returns['1'], 1)
            returns['5'] = round(returns['5'], 1)
            returns['30'] = round(returns['30'], 1)
        return returns

def _calculate_percentage_diff(old, current):
    percentage = ((current - old) / current) * 100
    return round(percentage, 1)