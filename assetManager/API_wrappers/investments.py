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


class Investments:
    def __init__(self):
        self.SANDBOX_KEY = '3c1540e977fb113fe9bdbb12bf61fd' # THESE SHOULD BE IN .env
        self.DEVELOPMENT_KEY = 'e28a689e4a829a09af4969900e0e55'
        self.CLIENT_ID = '63d288b343e6370012e5be86'


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
            products=[Products('auth'), Products('transactions')],
            client_name="Plaid Test App",
            country_codes=[CountryCode('GB')],
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


    def get_access_token(self, public_token):
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=PUBLIC_TOKEN
        )

        exchange_response = client.item_public_token_exchange(exchange_request)
        return exchange_response['access_token']

