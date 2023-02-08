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
from assetManager.models import AccountType, AccountTypeEnum
from assetManager.helpers import make_aware_date
from datetime import datetime
from django.db import IntegrityError

class PublicTokenNotExchanged(Exception):
    pass

class LinkTokenNotCreated(Exception):
    pass

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

    def save_access_token(self, user):
        if self.ACCESS_TOKEN is None:
            raise PublicTokenNotExchanged
        for product_name in self.products_requested:
            try:
                AccountType.objects.create(
                    user = user,
                    account_asset_type = AccountTypeEnum(self._transform_product_to_enum_value(product_name)),
                    account_date_linked = make_aware_date(datetime.now()),
                    access_token = self.ACCESS_TOKEN
                )
            except IntegrityError:
                return


    def _transform_product_to_enum_value(self, product):
        if product == 'investments' or product == 'assets':
            return 'STOCK'
        if product == 'transactions':
            return 'DEBIT'

        
        
        


        

