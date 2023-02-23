from assetManager.API_wrappers.plaid_wrapper import PublicTokenNotExchanged
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
from plaid.model.investments_transactions_get_request import InvestmentsTransactionsGetRequest
import json
from collections import defaultdict
from assetManager.investments.investment import Investment
from assetManager.API_wrappers.yfinance_wrapper import YFinanceWrapper

class CannotGetStockHistoryException(Exception):
    pass

class StocksGetter():
    def __init__(self, concrete_wrapper):
        self.wrapper = concrete_wrapper
        self.investments = []
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

    def format_investments(self, unformatted_investments):
        for current_investment in unformatted_investments:
            for holding in current_investment['holdings']:
                security_id = holding['security_id']
                for security in current_investment['securities']:
                    if security['security_id'] == security_id:
                        self.investments.append(Investment(holding, security))
                        break

    # Returns a list of dictionaries of the form {stock_name: stock_price}
    def get_prepared_data(self):
        stock_dict = defaultdict(int)
        for investment in self.investments:
            stock_dict[investment.get_name()]+=investment.get_total_price()
        return stock_dict

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
    def get_stocks(self):
        stocks = defaultdict(int)
        for investment in self.investments:
            category = investment.get_category()
            # only equity and ETFs are considered stocks (i.e. ignoring derivatives)
            if category == 'equity' or category == 'etf':
                stocks[investment.get_ticker()] = investment.get_total_price()
        return stocks

    # Returns a dictionary - {date: close_price}
    def get_stock_history(self, ticker):
        try:
            data = self.yfinance_wrapper.get_stock_history(ticker)
        except Exception:
            raise CannotGetStockHistoryException('YFinance API could not provide information for: ' + ticker)
        return data

