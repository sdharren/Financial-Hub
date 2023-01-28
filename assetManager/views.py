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

"""https://sandbox.plaid.com (Sandbox)
https://development.plaid.com (Development)
https://production.plaid.com (Production)"""

PLAID_CLIENT_ID = "63d288b343e6370012e5be86"
PLAID_SECRET_ID = "3c1540e977fb113fe9bdbb12bf61fd"
PLAID_REDIRECT_URI = 'http://localhost:3000/'

host = plaid.Environment.Sandbox

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

request = LinkTokenCreateRequest(
    products=[Products('auth'), Products('transactions')],
    client_name="KCL",
    country_codes=[CountryCode('US')],
    redirect_uri='http://localhost:3000/',
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
        client_user_id=PLAID_CLIENT_ID
    ),
)

def get_transactions():
    response = client.link_token_create(request)
    link_token = response['link_token']
    #print(link_token)
