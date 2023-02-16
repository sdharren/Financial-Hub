from plaid.model.sandbox_item_fire_webhook_request import SandboxItemFireWebhookRequest
from plaid.model.transactions_refresh_request import TransactionsRefreshRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.institutions_get_request import InstitutionsGetRequest

from plaid.model.sandbox_public_token_create_request_options import SandboxPublicTokenCreateRequestOptions
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions

from plaid.model.item_get_request import ItemGetRequest

from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from datetime import date

from pprint import pprint

#response = client.sandbox_item_fire_webhook(request)
#GqQalvm5JrCAaQ8lPjq7tdjXVK7wpyt1jexyg

class DebitCard():
    def __init__(self,concrete_wrapper):
        self.plaid_wrapper = concrete_wrapper
        public_token = self.plaid_wrapper.create_public_token()
        self.plaid_wrapper.products_requested = 'transactions'
        self.plaid_wrapper.exchange_public_token(public_token)



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

    def print_class(self):
        obj = TransactionsGetRequestOptions()
        print(dir(obj))

    def get_transactions(self):
        request1 = TransactionsRefreshRequest(access_token=self.plaid_wrapper.ACCESS_TOKEN)
        response1 = self.plaid_wrapper.client.transactions_refresh(request1)

        request = TransactionsGetRequest(
            access_token=self.plaid_wrapper.ACCESS_TOKEN,
            start_date=date.fromisoformat('2023-01-02'),
            end_date=date.fromisoformat('2023-02-09'),
            #options =TransactionsGetRequestOptions(
            #username = "John Smith",
            #)
            )
        response = self.plaid_wrapper.client.transactions_get(request)
        transactions = response['transactions']
        print(transactions)
        print(len(transactions))
        """
        while len(transactions) < response['total_transactions']:
            request = TransactionsGetRequest(
            access_token=self.plaid_wrapper.ACCESS_TOKEN,
            start_date=datetime.date('2018-01-01'),
            end_date=datetime.date('2018-02-01'),
            options=TransactionsGetRequestOptions(
                offset=len(transactions)
                )
            )

        response = self.plaid_wrapper.client.transactions_get(request)
        transactions.extend(response['transactions'])
        print(transactions)
        """
