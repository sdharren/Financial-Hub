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
import os
from dotenv import dotenv_values
from assetManager.models import AccountType, AccountTypeEnum
from assetManager.helpers import make_aware_date
from datetime import datetime

class PublicTokenNotExchanged(Exception):
    pass

class LinkTokenNotCreated(Exception):
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

    def create_link_token(self, products_chosen=['auth']):
        product_list = []
        for product_name in products_chosen:
            product_list.append(Products(product_name))
        
        request = LinkTokenCreateRequest(
            products=product_list,
            client_name="dash.",
            country_codes=[CountryCode('US'), CountryCode('GB'), CountryCode('ES'), CountryCode('NL'), CountryCode('FR'), CountryCode('IE'), CountryCode('CA'), CountryCode('DE'), CountryCode('IT'), CountryCode('PL'), CountryCode('DK'), CountryCode('NO'), CountryCode('SE'), CountryCode('EE'), CountryCode('LT'), CountryCode('LT')],
            redirect_uri='https://google.com',
            language='en',
            webhook='https://sample-webhook-uri.com',
            link_customization_name='default',
            user=LinkTokenCreateRequestUser(
                client_user_id='123-test-user-id' # FIGURE OUT WHAT TO DO HERE
            ),
        )
        response = self.client.link_token_create(request)
        self.LINK_TOKEN = response['link_token']

    def exchange_public_token(self, public_token):
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token = public_token
        )
        exchange_response = self.client.item_public_token_exchange(exchange_request)
        self.ACCESS_TOKEN = exchange_response['access_token']
        self.ITEM_ID = exchange_response['item_id']

    def save_access_token(self, user, products_chosen):
        if self.ACCESS_TOKEN is None:
            raise PublicTokenNotExchanged
        for product_name in products_chosen:
            try:
                AccountType.objects.create(
                    user = user,
                    account_asset_type = AccountTypeEnum(product_name),
                    account_date_linked = make_aware_date(datetime.now()),
                    access_token = self.ACCESS_TOKEN
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
    
        
            
        

        

    
