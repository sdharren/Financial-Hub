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

"""
DebitCard class to represent a Bank Card asset with relevant methods to access transactions and account specific data
"""
class DebitCard():
    def __init__(self,concrete_wrapper,user):
        self.plaid_wrapper = concrete_wrapper
        self.user = user
        self.access_tokens = self.plaid_wrapper.retrieve_access_tokens(self.user,'transactions')

    #Method to refresh the plaid api for any new transactions, must be made before querying transactions directly
    def refresh_api(self,token):
        refresh_request = TransactionsRefreshRequest(access_token=token)
        refresh_response = self.plaid_wrapper.client.transactions_refresh(refresh_request)

    def get_institution_name_from_db(self):
        institution_name = AccountType.objects.get(user = self.user, access_token = self.access_tokens[0], account_asset_type = AccountTypeEnum.DEBIT).account_institution_name
        return institution_name

    #returns a dictionary containing account balances for all DEBIT account types stored in the database for a specific user
    def get_account_balances(self):
        balances = {}

        for token in self.access_tokens:
            request_accounts = AccountsGetRequest(access_token=token)
            response = self.plaid_wrapper.client.accounts_get(request_accounts)
            balances[self.get_institution(response['item']['institution_id'])] =  response['accounts'][0]['balances']['available']

        print(balances)

    def get_transactions(self,start_date_input,end_date_input):
        transaction_dict = {}
        for token in self.access_tokens:
            self.refresh_api(token)

            transaction_request = TransactionsGetRequest(
                access_token=token,
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

        """
        while len(transactions) < transaction_response['total_transactions']:
                print('here')
                self.refresh_api()
                request = TransactionsGetRequest(
                access_token=self.access_tokens,
                start_date=start_date_input,
                end_date=end_date_input,
                options=TransactionsGetRequestOptions(
                    offset=len(transactions)
                    )
                )

                response = self.plaid_wrapper.client.transactions_get(request)
                transactions.extend(response['transactions'])
        """

"""
    def get_item(self):
        pt_request = SandboxPublicTokenCreateRequest(
            institution_id='ins_115642',
            initial_products=[Products('transactions')],
            options = SandboxPublicTokenCreateRequestOptions(
                override_username = 'custom_john_smith',
            )

        )
        pt_response = self.plaid_wrapper.client.sandbox_public_token_create(pt_request)
        # The generated public_token can now be
        # exchanged for an access_token
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=pt_response['public_token']
        )
        exchange_response = self.plaid_wrapper.client.item_public_token_exchange(exchange_request)

        access_token = exchange_response['access_token']

        self.get_transactions(access_token)
        #request = SandboxItemFireWebhookRequest(
        #access_token=access_token,
        #webhook_code='DEFAULT_UPDATE'
        #)
        #response = client.sandbox_item_fire_webhook(request)

    def get_institutions(self):
        request = InstitutionsGetRequest(
            country_codes=[CountryCode('GB')],
            count=10,
            offset=1,
            )
        response = self.plaid_wrapper.client.institutions_get(request)
        institutions = response['institutions']
        print(institutions)

    def create_new_item():
        request = SandboxProcessorTokenCreate(institution_id=INSTITUTION_ID)
        response = client.sandbox_processor_token_create(request)
        processor_token = response['processor_token']
        print(processor_token)

    def get_item():
        request = ItemGetRequest(access_token=self.plaid_wrapper.ACCESS_TOKEN)
        response = self.plaid_wrapper.client.item_get(request)
        item = response['item']
        status = response['status']

    def get_synch_transactions(self):
        cursor = ""
        # New transaction updates since "cursor"
        added = []
        modified = []
        removed = [] # Removed transaction ids
        has_more = True
# Iterate through each page of new transaction updates for item
        while has_more:
            request = TransactionsSyncRequest(
            access_token=self.plaid_wrapper.ACCESS_TOKEN,
            cursor=cursor,
            )
            response = self.plaid_wrapper.client.transactions_sync(request)
            print(response)
            # Add this page of results
            added.extend(response['added'])
            modified.extend(response['modified'])
            removed.extend(response['removed'])
            has_more = response['has_more']



    def fire_webhook(self):
        print(self.plaid_wrapper.get_item_id())
        request = SandboxItemFireWebhookRequest(
            access_token=self.plaid_wrapper.ACCESS_TOKEN,
            webhook_code='DEFAULT_UPDATE',
            )
        response = self.plaid_wrapper.client.sandbox_item_fire_webhook(request)
        print(response)

    def get_recurring_transactions():
        request = TransactionsRecurringGetRequest(
            access_token=self.plaid_wrapper.ACCESS_TOKEN,
            account_ids=account_ids,
        )
        response = client.transactions_recurring_get(request)
"""
