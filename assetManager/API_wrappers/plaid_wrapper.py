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
from assetManager.API_wrappers.investments import Investments

class PlaidWrapper():
    def __init__(self):
        self.CLIENT_ID = '63d288b343e6370012e5be86'
        self.ACCESS_TOKEN = None
        self.ITEM_ID = None

    def get_access_token(self):
        pass

    def get_item_id(self):
        pass

    def create_link_token(self):
        request = LinkTokenCreateRequest(
            products=[Products('auth'), Products('transactions')],
            client_name="Plaid Test App",
            country_codes=[CountryCode('US')],
            redirect_uri='https://google.com',
            language='en',
            webhook='https://sample-webhook-uri.com',
            link_customization_name='default',
            account_filters=LinkTokenAccountFilters(
                depository=DepositoryFilter(
                    account_subtypes=DepositoryAccountSubtypes(
                        [DepositoryAccountSubtype('checking'), DepositoryAccountSubtype('savings')]
                    )
                )
            ),
            user=LinkTokenCreateRequestUser(
                client_user_id='123-test-user-id'
            ),
        )
        response = self.client.link_token_create(request)
        return response['link_token']

    def exchange_public_token(self,public_token):
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=public_token_response['public_token']
        )
        exchange_response = client.item_public_token_exchange(exchange_request)
        self.ACCESS_TOKEN = exchange_response['access_token']
        self.ITEM_ID = exchange_response['item_id']
