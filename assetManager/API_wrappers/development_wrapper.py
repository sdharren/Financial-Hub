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
from plaid_wrapper import PlaidWrapper

class DevelopmentWrapper(PlaidWrapper):
    def __init__(self):
        self.DEVELOPMENT_KEY = 'e28a689e4a829a09af4969900e0e55'
        self.ACCESS_TOKEN = ''
        self.ITEM_ID = ''


        configuration = plaid.Configuration(
        host=plaid.Environment.Development,
        api_key={
            'clientId': self.CLIENT_ID,
            'secret': self.DEVELOPMENT_KEY,
            }
        )

        api_client = plaid.ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)


    def create_link_token(self):
        request = LinkTokenCreateRequest(
            products=[Products('auth'), Products('investments'), Products('transactions'), Products('balance')],
            client_name="dash.",
            country_codes=[CountryCode('US'), CountryCode('GB'), CountryCode('ES'), CountryCode('NL'), CountryCode('FR'), CountryCode('IE'), CountryCode('CA'), CountryCode('DE'), CountryCode('IT'), CountryCode('PL'), CountryCode('DK'), CountryCode('NO'), CountryCode('SE'), CountryCode('EE'), CountryCode('LT'), CountryCode('LT')],
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

    def exchange_public_token(self, public_token):
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=PUBLIC_TOKEN
        )
        exchange_response = client.item_public_token_exchange(exchange_request)
        self.ACCESS_TOKEN = exchange_response['access_token']
        self.ITEM_ID = exchange_response['item_id']

    def get_access_token(self):
        return self.ACCESS_TOKEN

    def get_item_id(self):
        return self.ITEM_ID
        

