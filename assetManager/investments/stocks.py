from assetManager.API_wrappers.plaid_wrapper import PublicTokenNotExchanged
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
from plaid.model.investments_transactions_get_request import InvestmentsTransactionsGetRequest
import json
from collections import defaultdict
from assetManager.investments.investment import Investment

class StocksGetter():
    def __init__(self, concrete_wrapper):
        self.wrapper = concrete_wrapper
        self.investments = []

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

    # Returns security ids categorized by their resprective type - {type: security_id}
    def _categorized_security_ids(self):
        categories = defaultdict(list)
        for security in self.get_securities():
            categories[security['type']].append(security['security_id'])
        return categories

    # Returns the monetary total of investments categorised by their type - {'type: total_sum'}
    def get_investment_categories(self):
        categories = defaultdict(int)
        for investment in self.investments:
            categories[investment.get_category()] += investment.get_total_price()
        return categories


