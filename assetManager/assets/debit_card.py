from plaid.model.transactions_refresh_request import TransactionsRefreshRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.products import Products
import datetime
from datetime import date,timedelta
from assetManager.models import AccountType, AccountTypeEnum
from plaid.exceptions import ApiException
from assetManager.API_wrappers.plaid_wrapper import AccessTokenInvalid
from assetManager.transactionInsight.bank_graph_data import BankGraphData
from django.core.exceptions import ObjectDoesNotExist
from assetManager.transactionInsight.bank_graph_data import create_forex_rates,get_currency_converter

"""
Custom Exception Thrown In the case that the passed list of transactions is empty
"""
class bankDataEmpty(Exception):
    def __init__(self):
        self.message = 'Provided transaction data is empty'

"""
@params: request_accounts, PLAID dictionary containing all information regarding accounts of a single linked institution

@Description:-Iterates through un-formatted requested accounts and extracting relevant values for graohs
             -Data is checked for being None and changed to more appropriate value

@return: accounts, custom dictionary keys:(name,available_amount,current_amount,type,currency), values: all strings except for available and current amount which are floats
"""

def filter_non_supported_account_currencies(accounts):
    filtered_accounts = []
    input_date = get_currency_converter()
    rates = create_forex_rates(input_date)

    for account in accounts:
        if account['balances']['iso_currency_code'] in rates.keys():
            filtered_accounts.append(account)

    return filtered_accounts

def filter_non_supported_transaction_currencies(transaction_response):
    input_date = get_currency_converter()
    rates = create_forex_rates(input_date)

    new_transactions = []
    for transaction in transaction_response:
        if(transaction['iso_currency_code'] in rates.keys()):
            new_transactions.append(transaction)

    return new_transactions


def format_accounts_data(request_accounts):
    accounts = {}
    for account in request_accounts:
        available = 0.0
        current = 0.0
        name = 'Not Provided'
        type = 'Not Provided'

        if(account['balances']['available'] is not None):
            available = account['balances']['available']

        if(account['balances']['current'] is not None):
            current = account['balances']['current']

        if(account['name'] is not None):
            name = account['name']

        if(account['type'] is not None):
            type = str(account['type'])

        case = {'name':name,'available_amount':available, 'current_amount':current,'type':type,'currency':account['balances']['iso_currency_code']}
        accounts[account['account_id']] = case

    return accounts

"""
Class DebitCard represents a universal handler to use functionalities related to all bank related assets

-Allows functionalities to retrieve all account balances for all institution linked by the User
-Allows functionalities to retrieve all transactions made within a 2 year time span by the user
-Allows to get the most recent transactions made by the user depending

Constructor:
    @params: concrete_wrapper, an instance of Plaid_wrapper which can be both DEVELOPMENT for deployed application use and SANDBOX for testing purposes
             user, an instance of User from models to gather all access tokens saved with related 'transactions' inferring bank related assets

    @instance_variables:
        -plaid_wrapper: object of instance Plaid_wrapper to make call to plaid
        -user : corresponding user for their bank related assets
        -access_tokens: list of linked access tokens for bank related assets
        -bank_graph_data: key: institution name, value : BankGraphData of transaction data
"""
class DebitCard():
    def __init__(self,concrete_wrapper,user):
        self.plaid_wrapper = concrete_wrapper
        self.user = user
        self.access_tokens = self.plaid_wrapper.retrieve_access_tokens(self.user,'transactions')
        self.bank_graph_data = {}

    """
    @params: token for plaid_wrapper

    @Description: -Refreshes the plaid api to retrieve most updated data

    @return:
    """
    def refresh_api(self,token):
        refresh_request = TransactionsRefreshRequest(access_token=token)
        try:
            refresh_response = self.plaid_wrapper.client.transactions_refresh(refresh_request)
        except ApiException:
            raise AccessTokenInvalid

    """
    @params: token for plaid_wrapper

    @Description: -Finds and returns linked institution name using the user and token

    @return: institution name as string
    """
    def get_institution_name_from_db(self,token):
        try:
            institution_name = AccountType.objects.get(user = self.user, access_token = token, account_asset_type = AccountTypeEnum.DEBIT).account_institution_name
        except ObjectDoesNotExist:
            return None

        return institution_name


    def get_single_account_balances(self,token):
        request_accounts = self.plaid_wrapper.get_accounts(token)
        accounts = filter_non_supported_account_currencies(request_accounts)
        formatted_accounts = format_accounts_data(accounts)
        return formatted_accounts

    def get_single_transaction(self,start_date_input,end_date_input,token):
        self.refresh_api(token)
        transaction_request = TransactionsGetRequest(
            access_token=token,
            start_date=start_date_input,
            end_date=end_date_input,
        )

        transaction_response = self.plaid_wrapper.client.transactions_get(transaction_request)
        return transaction_response['transactions']

    """
    @params:

    @Description: Retrieves all account dictionaries for all linked instituitions by the user, reformatting them by extracting required data

    @return: balances, custom dictionary keys:(name,available_amount,current_amount,type,currency), values: all strings except for available and current amount which are floats
    """
    def get_account_balances(self):
        balances = {}
        for token in self.access_tokens:
            accounts = self.get_single_account_balances(token)
            balances[self.plaid_wrapper.get_institution_name(token)] = accounts

        return balances

    """
    @params: start_date_input,end_date_input datetime.date objects representing the start and end date range for transaction retrieval

    @Description: Retrieves all transactions for all institutions linked by the user within the selected date range

    @return: transactions, list containing TransactionsGetRequest return objects composed of list of transactions linked to corresponding account_id
    """
    def get_transactions_by_date(self,start_date_input,end_date_input):
        transactions = []
        for token in self.access_tokens:
            transaction_response = self.get_single_transaction(start_date_input,end_date_input,token)
            new_transactions = filter_non_supported_transaction_currencies(transaction_response)
            transactions.append(new_transactions)

        return transactions

    """
    @params: token: PlaidApi Token for a linked institution, transactions: list of containing TransactionsGetRequest return objects for all linked institutions requested
             transaction_count: int, index for corresponding transactions list

    @Description: Creates a new entry in bank_graph_data by intialising a new key being the corresponding institution name retrieved using the access token
                  The value being an object of BankGraphData, passed a section of transactions corresponding to the transactions made under the institution retrieved by the access token

    @return:
    """
    def make_bank_graph_data_dict(self,token,transactions,transaction_count):
        self.bank_graph_data[self.get_institution_name_from_db(token)] = BankGraphData(transactions[transaction_count]).transactionInsight.transaction_history

    """
    @params: start_date_input,end_date_input datetime.date objects representing the start and end date range for transaction retrieval

    @Description: Retrieves all transactions for all institutions linked by the user within the selected date range and for all linked institutions creates the bank graph data dictionary for each institutiton

    @return: transactions, list containing TransactionsGetRequest return objects composed of list of transactions linked to corresponding account_id
    """
    def make_graph_transaction_data_insight(self,start_date_input,end_date_input):
        transaction_count = 0
        transactions = self.get_transactions_by_date(start_date_input,end_date_input)
        for token in self.access_tokens:
            self.make_bank_graph_data_dict(token,transactions,transaction_count)
            transaction_count = transaction_count + 1

    """
    @params:

    @Description: Retrieves the bank_graph_data dictionary if it is already set

    @return: bank_graph_data, custom dictionary, key: institution name, value: BankGraphData object of corresponding transactions
    """
    def get_insight_data(self):
        if(not self.bank_graph_data):
            return None
        else:
            return self.bank_graph_data


    def format_category(self,category):
        if(category == 'Not Provided'):
            return category

        result = ', '.join(category)
        last_comma_index = result.rfind(',')
        if last_comma_index != -1:
            result = f"{result[:last_comma_index]},{result[last_comma_index+1:]}"
        return result

    """
    @params: bank_graph_data, dictionary , institution_name: string of the corresponding institution name of the dictionary

    @Description: Within the bank_graph_data dictionary of transactions it retrieves only the transactions whose data correspond to today

    @return: recent_transactions, dictionary, key: passed insitution name, values: list of all transactions made recently (today)
    """
    def get_recent_transactions(self,bank_graph_data,institution):
        if(not bank_graph_data):
            raise bankDataEmpty()

        first_five_transactions = bank_graph_data[:10]
        all_transactions = []
        for account in first_five_transactions:
            if(account['date'] != 'Not Provided'):
                date = datetime.date(account['date'][0],account['date'][1],account['date'][2])
            else:
                date = account['date']

            case = {'amount': '£' + str(account['amount']), 'date':date, 'category':self.format_category(account['category']), 'merchant':account['merchant_name']}

            all_transactions.append(case)

        return all_transactions
