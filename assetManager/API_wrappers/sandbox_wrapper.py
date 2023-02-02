from django.shortcuts import render
from django.http import HttpResponse
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.link_token_account_filters import LinkTokenAccountFilters
from plaid.model.depository_filter import DepositoryFilter
from plaid.model.depository_account_subtypes import DepositoryAccountSubtypes
from plaid.model.depository_account_subtype import DepositoryAccountSubtype
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from .plaid_wrapper import PlaidWrapper

class SandboxWrapper(PlaidWrapper):
    def __init__(self):
        super().__init__()
        self.SANDBOX_KEY = '3c1540e977fb113fe9bdbb12bf61fd'
        self.PUBLIC_TOKEN = None

        configuration = plaid.Configuration(
        host=plaid.Environment.Development,
        api_key={
            'clientId': self.CLIENT_ID,
            'secret': self.SANDBOX_KEY,
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

    def create_public_token(self):
        REVOLUT_ID = 'ins_115642' # revolut's ID
        public_token_request = SandboxPublicTokenCreateRequest(
            institution_id=REVOLUT_ID,
            initial_products=[Products('transactions')]
        )
        return self.client.sandbox_public_token_create(public_token_request)
