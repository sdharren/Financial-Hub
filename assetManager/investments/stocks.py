from assetManager.API_wrapper.plaid_wrapper import PublicTokenNotExchanged
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions

class StocksGetter():
    def __init__(self, concrete_wrapper):
        self.wrapper = concrete_wrapper

    def get_stock_positions(self, user):
        try:
            access_token = self.wrapper.get_access_token()
        except PublicTokenNotExchanged:
            self.wrapper.retrieve_access_token(user, 'investments')
            access_token = access_token

        request = InvestmentsHoldingsGetRequest(access_token=access_token)
        response = self.wrapper.client.investments_holdings_get(request)
        return response
