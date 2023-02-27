from plaid.model.sandbox_item_fire_webhook_request import SandboxItemFireWebhookRequest
from plaid.model.transactions_refresh_request import TransactionsRefreshRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.institutions_get_request import InstitutionsGetRequest
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
from plaid.model.accounts_get_request import AccountsGetRequest

from plaid.model.sandbox_public_token_create_request_options import SandboxPublicTokenCreateRequestOptions
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions

from plaid.model.item_get_request import ItemGetRequest

from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from datetime import date

from assetManager.models import AccountType, AccountTypeEnum
from plaid.exceptions import ApiException
from assetManager.API_wrappers.plaid_wrapper import AccessTokenInvalid
"""
DebitCard class to represent a Bank Card asset with relevant methods to access transactions and account specific data
"""
class DebitCard():
    def __init__(self,concrete_wrapper,user):
        self.plaid_wrapper = concrete_wrapper
        self.user = user
        self.access_tokens = self.plaid_wrapper.retrieve_access_tokens(self.user,'transactions')

    #Method to refresh the plaid api for any new transactions, must be made before querying transactions directly
    def refresh_api(self):
        refresh_request = TransactionsRefreshRequest(access_token=self.plaid_wrapper.ACCESS_TOKEN)
        try:
            refresh_response = self.plaid_wrapper.client.transactions_refresh(refresh_request)
        except ApiException:
            raise AccessTokenInvalid


    def get_institution_name_from_db(self):
        institution_name = AccountType.objects.get(user = self.user, access_token = self.access_tokens[0], account_asset_type = AccountTypeEnum.DEBIT).account_institution_name
        return institution_name

    #returns a dictionary containing account balances for all DEBIT account types stored in the database for a specific user
    def get_account_balances(self):
        balances = {}
        for token in self.access_tokens:
            self.plaid_wrapper.ACCESS_TOKEN = token

            request_accounts = self.plaid_wrapper.get_accounts()
            accounts = {}
            for account in request_accounts:
                case = {'available_amount':account['balances']['available'], 'current_amount':account['balances']['current'],'type':account['type'],'currency':account['balances']['iso_currency_code']}
                accounts[account['account_id']] = case

            balances[self.plaid_wrapper.get_institution_name()] = accounts

        return balances



    def get_transactions_by_date(self,start_date_input,end_date_input):
        transaction_dict = {}
        for token in self.access_tokens:
            self.plaid_wrapper.ACCESS_TOKEN = token
            
            self.refresh_api(token)

            transaction_request = TransactionsGetRequest(
                access_token=SELF.plaid_wrapper.ACCESS_TOKEN,
                start_date=start_date_input,
                end_date=end_date_input,
            )

            transaction_response = self.plaid_wrapper.client.transactions_get(transaction_request)
            print(transaction_response)

            #institution_id = transaction_response['item']['institution_id']
            #currency = transaction_response['accounts'][0]['balances']['iso_currency_code']
            #transactions = transaction_response['transactions']#

        #    single_transaction_case = {'transactions':transactions, 'currency':currency} # instituion id here

        #    transaction_dict[institution_id] = single_transaction_case

        #print(transaction_dict)
        #return transaction_dict
