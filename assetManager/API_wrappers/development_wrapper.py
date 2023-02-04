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

class DevelopmentWrapper(PlaidWrapper):
    def __init__(self):
        super().__init__()
        
        configuration = plaid.Configuration(
        host=plaid.Environment.Development,
        api_key={
            'clientId': self.CLIENT_ID,
            'secret': self.DEVELOPMENT_KEY,
            }
        )

        api_client = plaid.ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)

    def get_access_token(self):
        return self.ACCESS_TOKEN

    def get_item_id(self):
        return self.ITEM_ID

    def get_link_token(self):
        return self.LINK_TOKEN
        

