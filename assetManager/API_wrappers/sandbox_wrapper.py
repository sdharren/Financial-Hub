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
from plaid.model.sandbox_public_token_create_request_options import SandboxPublicTokenCreateRequestOptions
from plaid.model.accounts_get_request import AccountsGetRequest

from .plaid_wrapper import PlaidWrapper

from plaid.exceptions import ApiException

class IncorrectInstitutionId(Exception):
    def __init__(self):
        self.message = 'Non Existing InstituionId Provided'


class IncorrectProduct(Exception):
    def __init__(self):
        self.message = 'Non Valid Products Provided'

class SandboxWrapper(PlaidWrapper):

    def __init__(self):
        super().__init__()
        self.PUBLIC_TOKEN = None
        self.SANDBOX_KEY = '3c1540e977fb113fe9bdbb12bf61fd'

        configuration = plaid.Configuration(
        host=plaid.Environment.Sandbox,
        api_key={
            'clientId': self.CLIENT_ID,
            'secret': self.SANDBOX_KEY,
            }
        )

        api_client = plaid.ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)

    def create_public_token(self, bank_id='ins_115642', products_chosen=['transactions']):
        product_list = []
        for product_name in products_chosen:
            product_list.append(Products(product_name))

        public_token_request = SandboxPublicTokenCreateRequest(
            institution_id = bank_id,
            initial_products = product_list
        )

        try:
            response = self.client.sandbox_public_token_create(public_token_request)
        except ApiException as e:
            if(e.body.split()[6] == '"INVALID_INSTITUTION",'):
                raise IncorrectInstitutionId
            else:
                raise IncorrectProduct

        return response['public_token']

    #write tests for this method
    def create_public_token_custom_user(self, bank_id='ins_115642', products_chosen=['transactions'], override_username="custom_sixth"):
        product_list = []
        for product_name in products_chosen:
            product_list.append(Products(product_name))
        self.products_requested = products_chosen

        public_token_request = SandboxPublicTokenCreateRequest(
            institution_id = bank_id,
            initial_products = product_list,
            options = SandboxPublicTokenCreateRequestOptions(override_username = override_username, override_password = "nonempty", )
        )

        try:
            response = self.client.sandbox_public_token_create(public_token_request)
        except ApiException as e:
            if(e.body.split()[6] == '"INVALID_INSTITUTION",'):
                raise IncorrectInstitutionId
            else:
                raise IncorrectProduct

        return response['public_token']
