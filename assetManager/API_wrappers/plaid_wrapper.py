from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError
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
from plaid.model.item_get_request import ItemGetRequest
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
import re
import os
from dotenv import dotenv_values
from assetManager.models import AccountType, AccountTypeEnum
from assetManager.helpers import make_aware_date
from datetime import datetime
from plaid.model.identity_get_request import IdentityGetRequest


from plaid.exceptions import ApiException

class PublicTokenNotExchanged(Exception):
    pass

class LinkTokenNotCreated(Exception):
    pass

class AccessTokenInvalid(Exception):
    pass

class InvalidProductSelection(Exception):
    pass

class PlaidWrapperIsAnAbstractClass(Exception):
    pass

class InvalidPublicToken(Exception):
    pass

class PlaidWrapper():
    def __init__(self):
        self.CLIENT_ID = '63d288b343e6370012e5be86'
        self.ACCESS_TOKEN = None
        self.ITEM_ID = None
        self.LINK_TOKEN = None

    def get_access_token(self):
        if self.ACCESS_TOKEN is None:
            raise PublicTokenNotExchanged
        return self.ACCESS_TOKEN

    def get_item_id(self):
        if self.ITEM_ID is None:
            raise PublicTokenNotExchanged
        return self.ITEM_ID

    def get_link_token(self):
        if self.LINK_TOKEN is None:
            raise LinkTokenNotCreated
        return self.LINK_TOKEN

    # Exchanges public token for access token and item id and saves them as class variables
    # Cannot be used with a PlaidWrapper object (only subclasses of it)
    def exchange_public_token(self, public_token):
        if not hasattr(self, 'client'):
            raise PlaidWrapperIsAnAbstractClass()
        if public_token is None:
            raise InvalidPublicToken('Public token cannot be None')
        if re.match(r"^public-development-[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$",public_token) is None and re.match(r"^public-sandbox-[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$", public_token) is None:
            raise InvalidPublicToken("Public token: " + public_token + " has invalid format")

        exchange_request = ItemPublicTokenExchangeRequest(
            public_token = public_token
        )
        try:
            exchange_response = self.client.item_public_token_exchange(exchange_request)
        except ApiException as plaid_exception:
            raise InvalidPublicToken('The public token provided is invalid. See plaid message:\n' + str(plaid_exception))
        self.ACCESS_TOKEN = exchange_response['access_token']
        self.ITEM_ID = exchange_response['item_id']


    def get_identity(self):
        request = IdentityGetRequest(access_token=self.get_access_token())
        try:
            response = self.client.identity_get(request)
        except ApiException:
            raise AccessTokenInvalid

        return response['accounts'][0]['owners'][0]


    def get_accounts(self,token):
        request_accounts = AccountsGetRequest(access_token=token)
        try:
            response = self.client.accounts_get(request_accounts)
        except ApiException:
            raise AccessTokenInvalid
        return response['accounts']


    def get_item(self,token):
        request = ItemGetRequest(access_token=token)
        try:
            response = self.client.item_get(request)
        except ApiException:
            raise AccessTokenInvalid

        item = response['item']
        return item

    #write tests for this method
    def get_institution_id(self,token):
        item = self.get_item(token)
        institution_id = item['institution_id']
        return institution_id

    #Returns the name of an institution given the institution_id passed as a parameter
    #write tests for this method as well
    def get_institution_name(self,token):
        institution_id = self.get_institution_id(token)

        request = InstitutionsGetByIdRequest(
            institution_id=institution_id,
            country_codes=[CountryCode('US'), CountryCode('GB'), CountryCode('ES'), CountryCode('NL'), CountryCode('FR'), CountryCode('IE'), CountryCode('CA'), CountryCode('DE'), CountryCode('IT'), CountryCode('PL'), CountryCode('DK'), CountryCode('NO'), CountryCode('SE'), CountryCode('EE'), CountryCode('LT'), CountryCode('LT')]
        )
        response = self.client.institutions_get_by_id(request)
        return response['institution']['name']

    def save_access_token(self, user, products_chosen):
        if self.ACCESS_TOKEN is None:
            raise PublicTokenNotExchanged

        institution_name = self.get_institution_name(self.ACCESS_TOKEN)
        for product_name in products_chosen:
            try:
                AccountType.objects.create(
                    user = user,
                    account_asset_type = AccountTypeEnum(product_name),
                    account_date_linked = make_aware_date(datetime.now()),
                    access_token = self.ACCESS_TOKEN,
                    account_institution_name = institution_name
                )
            except IntegrityError:
                return

    '''
    Retrieves the access tokens matching specified paramters. If a user has more than one access for the same product
    - the self.access_token attribute is set to a LIST of tokens
    '''
    def retrieve_access_tokens(self, user, product):
        accounts = AccountType.objects.filter(user = user, account_asset_type = product)
        if len(accounts) == 0:
            raise PublicTokenNotExchanged
        else:
            tokens = []
            for account in accounts:
                tokens.append(account.access_token)
            return tokens
