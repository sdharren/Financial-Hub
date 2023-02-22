from assetManager.API_wrappers.plaid_wrapper import PublicTokenNotExchanged
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
from plaid.model.investments_transactions_get_request import InvestmentsTransactionsGetRequest
import json
from collections import defaultdict

class StocksGetter():
    def __init__(self, concrete_wrapper):
        self.wrapper = concrete_wrapper
        self.investments = []

    # Sends API calls to plaid requesting investment info for each access token associated with user
    def query_investments(self, user):
        self.investments = []
        access_tokens = self.wrapper.retrieve_access_tokens(user, 'investments')
        for token in access_tokens:
            request = InvestmentsHoldingsGetRequest(access_token=token)
            response = self.wrapper.client.investments_holdings_get(request)
            self.investments.append(response)

    def get_holdings(self):
        holdings = []
        for investment in self.investments:
            holdings.append(investment['holdings'])
        return holdings

    # Returns the users securities
    # These represent specific stocks/bonds/... a user has
    def get_securities(self):
        securities = []
        for investment in self.investments:
            securities.append(investment['securities'])
        return securities

    # Returns the user's investment accounts
    # These only represent how much value a user's account has
    def get_accounts(self):
        accounts = []
        for investment in self.investments:
            accounts.append(investment['accounts'])
        return accounts

    # Returns a list of dictionaries of the form {stock_name: stock_price}
    def get_prepared_data(self):
        stocks = []
        for investment in self.investments:
            for holding in investment['holdings']:
                security_id = holding['security_id']
                stock_dict = {}
                for security in investment['securities']:
                    if security['security_id'] == security_id:
                        name = security['name'] # maybe we can use ticker instead of name?
                        break
                stock_dict[name] = holding['institution_value']
                stocks.append(stock_dict)
        return stocks

    #Returns total investment sum within the account
    def get_total_investment_sum(self):
        accounts = self.get_accounts()
        aggregate_investment = 0
        for account in accounts:
            for idx in range(len(account)):
                aggregate_investment += accounts[0][idx]['balances']['current']
        return aggregate_investment

    def categorized_securities(self):
        categories = defaultdict(list)
        for securities in self.get_securities():
            for security in securities:
                categories[security['type']].append(security['security_id'])
        return categories

    def get_investment_categories(self):
        categories = self.categorized_securities()
        all_holdings = self.get_holdings()
        for category_key in categories:
            sum = 0
            for security_id in categories[category_key]:
                for holdings in all_holdings:
                    for holding in holdings:
                        if holding['security_id'] == security_id:
                            sum += holding['institution_value']
                            break
            categories[category_key] = sum
        return categories


