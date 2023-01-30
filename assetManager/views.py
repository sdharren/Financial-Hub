from django.shortcuts import render
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

"""https://sandbox.plaid.com (Sandbox)
https://development.plaid.com (Development)
https://production.plaid.com (Production)"""

PUBLIC_TOKEN = "public-development-c619bf87-1395-44ae-ad2c-34d99d53bc60"

PLAID_CLIENT_ID = "63d288b343e6370012e5be86"
PLAID_SECRET_ID = "e28a689e4a829a09af4969900e0e55"#sandbox key"3c1540e977fb113fe9bdbb12bf61fd"
PLAID_REDIRECT_URI = 'http://localhost:8000/'

host = plaid.Environment.Development #Sandbox

configuration = plaid.Configuration(
    host=host,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET_ID,
        'plaidVersion': '2020-09-14'
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

"""
request = LinkTokenCreateRequest(
    products=[Products('auth'), Products('transactions')],
    client_name="Plaid Test App",
    country_codes=[CountryCode('US')],
    redirect_uri='http://localhost:8000',
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
"""

def get_accounts():
    #response = client.link_token_create(request)
    #link_token = response['link_token'] # getting link token form API

    #REVOLUT_ID = 'ins_115642' # using revolut's ID (just for testing)
    #pt_request = SandboxPublicTokenCreateRequest(
#        institution_id=REVOLUT_ID,
#        initial_products=[Products('transactions')]
#    )
    #pt_response = client.sandbox_public_token_create(pt_request)
     #The generated public_token can now be
#     exchanged for an access_token
    exchange_request = ItemPublicTokenExchangeRequest(
        public_token=PUBLIC_TOKEN
    )

    exchange_response = client.item_public_token_exchange(exchange_request)
    ACCESS_TOKEN = exchange_response['access_token'] # this access token needs to be used in places

    request = AccountsGetRequest(access_token=ACCESS_TOKEN)
    response = client.accounts_get(request)
    accounts = response['accounts']
    print(response)
    print(accounts)


def get_transactions():
    response = client.link_token_create(request)
    link_token = response['link_token']
    #print(link_token)

def connect_investments(request):
    investments = Investments()
    link_token = investments.create_link_token()
    return render(request, 'connect_investments.html', {'link_token': link_token})
