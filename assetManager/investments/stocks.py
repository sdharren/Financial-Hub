from assetManager.API_wrappers.plaid_wrapper import PublicTokenNotExchanged
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
import json

class StocksGetter():
    def __init__(self, concrete_wrapper):
        self.wrapper = concrete_wrapper
        self.investments = []

    def query_investments(self, user):
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

    def get_securities(self):
        holdings = []
        for investment in self.investments:
            holdings.append(investment['securities'])
        return holdings

    def get_accounts(self):
        holdings = []
        for investment in self.investments:
            holdings.append(investment['accounts'])
        return holdings


    #Returns total investment sum within the account
    def get_total_investment_sum(self):
        accounts = self.get_accounts()
        aggregate_investment = 0
        for account in accounts:
            for idx in range(len(account)):
                aggregate_investment += accounts[idx][0]['balances']['current']
        return aggregate_investment
