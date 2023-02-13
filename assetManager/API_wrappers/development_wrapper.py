import plaid
from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.depository_filter import DepositoryFilter
from plaid.model.depository_account_subtypes import DepositoryAccountSubtypes
from plaid.model.depository_account_subtype import DepositoryAccountSubtype
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.link_token_account_filters import LinkTokenAccountFilters
from .plaid_wrapper import PlaidWrapper



from datetime import date
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions


class DevelopmentWrapper(PlaidWrapper):
    def __init__(self):
        super().__init__()
        self.DEVELOPMENT_KEY = 'e28a689e4a829a09af4969900e0e55'

        configuration = plaid.Configuration(
        host=plaid.Environment.Development,
        api_key={
            'clientId': self.CLIENT_ID,
            'secret': self.DEVELOPMENT_KEY,
            }
        )

        api_client = plaid.ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)

    
    def get_transactions(self):
        request = TransactionsGetRequest(
            access_token=self.ACCESS_TOKEN,
            start_date=date.fromisoformat("2022-01-01"),
            end_date=date.fromisoformat("2023-01-01"),
            options=TransactionsGetRequestOptions()
        )
        response = self.client.transactions_get(request)
        transactions = response['transactions']
        return transactions

    
