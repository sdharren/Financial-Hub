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
from .plaid_wrapper import PlaidWrapper, InvalidProductSelection, LinkTokenNotCreated
from plaid.exceptions import ApiException

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

    # Returns a token which can be used to link a user's assets to the app via plaid
    def create_link_token(self, products_chosen=['auth']):
        if products_chosen is None or len(products_chosen) == 0:
            raise InvalidProductSelection('Cannot create link token for the following products: ' + str(products_chosen))
        product_list = []
        for product_name in products_chosen:
            product_list.append(Products(product_name))

        request = LinkTokenCreateRequest(
            products=product_list,
            client_name="dash.",
            country_codes=[CountryCode('US'), CountryCode('GB'), CountryCode('ES'), CountryCode('NL'), CountryCode('FR'), CountryCode('IE'), CountryCode('CA'), CountryCode('DE'), CountryCode('IT'), CountryCode('PL'), CountryCode('DK'), CountryCode('NO'), CountryCode('SE'), CountryCode('EE'), CountryCode('LT')],
            redirect_uri='https://google.com',
            language='en',
            webhook='https://sample-webhook-uri.com',
            link_customization_name='default',
            user=LinkTokenCreateRequestUser(
                client_user_id='123-test-user-id' # FIGURE OUT WHAT TO DO HERE
            ),
        )
        try:
            response = self.client.link_token_create(request)
        except ApiException as plaid_exception:
            raise LinkTokenNotCreated("Something went wrong while creating the link token. See plaid message:\n" + str(plaid_exception))
        self.LINK_TOKEN = response['link_token']