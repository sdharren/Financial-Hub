from django.conf import settings
from django.core.cache import cache
from assetManager.assets.debit_card import DebitCard
from assetManager.transactionInsight.bank_graph_data import BankGraphData,get_currency_converter
import datetime
from assetManager.models import User,AccountType,AccountTypeEnum
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.investments.stocks import StocksGetter, InvestmentsNotLinked
from assetManager.assets.debit_card import DebitCard
from forex_python.converter import CurrencyRates
from functools import wraps
from assetManager.API_wrappers.plaid_wrapper import PublicTokenNotExchanged
from rest_framework.response import Response

class TransactionsNotLinkedException(Exception):
    pass

class PlaidQueryException(Exception):
    pass


"""
@params: account_balances custom dictionary combining returned accounts request from PLAID API with the institution linked as the key

@Description: -Iterates through account_balances extracting every account and total amount of liquid assets in that account for a specific currency
              -Calculates percentage totals for all unique currencies for total overall amounts in all accounts

@return: Reformatted dictionary containing the percentage amount of liquidity overall categorised by currency for all accounts in all linked institutions
"""
def reformat_balances_into_currency(account_balances):
    if type(account_balances) is not dict:
        raise TypeError("account balances must be of type dict")

    currency_total = {}
    currency_rates =  CurrencyRates()

    input_date = get_currency_converter()

    for institution in account_balances.keys():
        for account in account_balances[institution].keys():
            currency_type = account_balances[institution][account]['currency']
            amount = account_balances[institution][account]['available_amount']
            if currency_type not in currency_total.keys():
                currency_total[currency_type] = 0

            result = currency_rates.convert(currency_type, 'GBP', amount,input_date)
            currency_total[currency_type] +=  result

    return currency_total

"""
@params: No params

@Description: -Depending on the settings.PLAID_DEVELOPMENT variable, either DEVELOPMENT for today's exhange rates or the SANDBOX for the fixed 2014 exchange rates for testing

@return: input_date, datetime object for returning corresponding exchange rate
"""
def calculate_perentage_proportions_of_currency_data(currency_total):
    proportions = {}
    total_money = sum(currency_total.values())

    for currency, amount in currency_total.items():
        proportion = amount / total_money
        proportions[currency] = round((proportion * 100),2)

    return proportions

"""
@params: account_balances custom dictionary combining returned accounts request from PLAID API with the institution linked as the key, institution_name string representing the name of the institution name

@Description: -Iterates through all account_balances extracting every account and total amount of liquid assets in that account for a specific the passed insitution
              -Creates a dictionary (key: name of the account, value: amount in that account)
              -Uses GBP as unique currency for quantifying amounts

@return: Reformatted dictionary containing all accounts and corresponding amount in that account
"""
def reformatAccountBalancesData(account_balances,institution_name):
    if type(account_balances) is not dict:
        raise TypeError("account balances must be of type dict")

    if institution_name not in account_balances.keys():
        raise Exception("passed institution_name is not account balances dictionary")

    currency_rates =  CurrencyRates()
    input_date = get_currency_converter()
    accounts = {}
    duplicates = 0
    for account in account_balances[institution_name].keys():
        total = 0
        total += currency_rates.convert(account_balances[institution_name][account]['currency'], 'GBP',account_balances[institution_name][account]['available_amount'],input_date)

        if account_balances[institution_name][account]['name'] in accounts.keys():
            duplicates += 1
            accounts[account_balances[institution_name][account]['name'] + '_' + str(duplicates)] = total
        else:
            accounts[account_balances[institution_name][account]['name']] = total

    return accounts

"""
@params: account_balances custom dictionary combining returned accounts request from PLAID API with the institution linked as the key

@Description: -Iterates through all accounts for all linked institutions summing the total available amount in each account
              -Creates a dictionary (key: name of the institution, value: amount in that all the accounts in that institution)
              -Uses GBP as unique currency for quantifying amounts

@return: Reformatted dictionary containing the institution name as the key and the sum of all account's available balance as the value
"""
def reformatBalancesData(account_balances):
    if type(account_balances) is not dict:
        raise TypeError("account balances must be of type dict")

    balances = {}

    currency_rates =  CurrencyRates()
    input_date = get_currency_converter()

    for institution_name in account_balances.keys():
        total = 0
        for account_id in account_balances[institution_name].keys():
            total += currency_rates.convert(account_balances[institution_name][account_id]['currency'], 'GBP', account_balances[institution_name][account_id]['available_amount'],input_date)

        balances[institution_name] = total

    return balances


"""
@params:
-user:models.User
user making the query

@Description: -Depending on the settings.PLAID_DEVELOPMENT either a development wrapper or sandbox wrapper for PLAID is returned

@return: plaid_wrapper: [DevelopmentWrapper, SandboxWrapper]
"""
def get_balances_wrapper(user):
    if settings.PLAID_DEVELOPMENT:
        plaid_wrapper = DevelopmentWrapper()
    else:
        #user is required to make a dummy access token for testing purposes
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token_custom_user()
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(user, ['transactions'])

    return plaid_wrapper

"""
@params:
-user:models.User
user making the query

-institution_name: String
name of the institution being checked in the database

@Description: -Checks whether the queried institution name is linked for the passed user

@return: Boolean - whether or not the institution_name requested is linked for the passed user
"""
def check_institution_name_selected_exists(user,institution_name):
    instituitions = AccountType.objects.filter(user = user, account_asset_type = AccountTypeEnum.DEBIT)

    for account in instituitions:
        if account.account_institution_name == institution_name:
            return True

    return False


"""
@params:
- user: models.User
  The user making the query
- plaid_wrapper: [DevelopmentWrapper, SandboxWrapper]
  The concrete types of PlaidWrapper used for the query

@Description:
This function creates a `DebitCard` object for making transactions using the provided `plaid_wrapper` and `user`.
If there are no access tokens in the database for the user or no institutions linked by the user, the `DebitCard` object creation will fail and the function raises a custom `TransactionsNotLinkedException`.
If the `DebitCard` object is successfully created, the function returns the `DebitCard` object.

@return:
A `DebitCard` object created using the provided `plaid_wrapper` and `user`.
"""
def make_debit_card(plaid_wrapper,user):
    try:
        debit_card = DebitCard(plaid_wrapper,user)
    except PublicTokenNotExchanged:
        raise TransactionsNotLinkedException('Transactions Not Linked.')

    return debit_card

"""
@params:
- user: models.User
  The user making the query
- plaid_wrapper: Union[DevelopmentWrapper, SandboxWrapper]
  The concrete types of PlaidWrapper used for the query

@description:
This function retrieves the account balances for all the linked institutions of the given `user` using the provided `plaid_wrapper`.
It first calls the `make_debit_card` function to create a `DebitCard` object for the given `user` and `plaid_wrapper`. Then it calls the `get_account_balances` method of the `DebitCard` object to retrieve the account balances.
If the account balances are successfully retrieved, the function returns them. If there is any error while querying the Plaid API, the function raises a custom `PlaidQueryException`.

@return:
A dictionary containing the account balances of all the linked institutions for the given `user`.
"""
def get_institutions_balances(plaid_wrapper,user):
    debit_card = make_debit_card(plaid_wrapper,user)

    try:
        account_balances = debit_card.get_account_balances()
    except Exception:
        raise PlaidQueryException('Something went wrong querying PLAID.')

    return account_balances

"""
@params:

token: a Plaid token used to access the Plaid API
wrapper: a Plaid API wrapper object
user: a user object containing the user's email address

@Description: This function retrieves the account balances for a single institution associated with a given user.
It uses a Plaid token and a user object to access the data through the Plaid API.
The account balances are stored in a cache for future use.

Returns:
Raises a PlaidQueryException if an error occurs while querying the Plaid API
None if the function executes successfully and stores the account balances in the cache
"""
def get_single_institution_balances(token,wrapper,user):
    #try catch this
    debit_card = make_debit_card(wrapper,user)

    try:
        account_balances = debit_card.get_single_account_balances(token)
    except Exception:
        raise PlaidQueryException('Something went wrong querying PLAID.')

    institution_name = wrapper.get_institution_name(token)

    if(cache.has_key('balances' + user.email) is False):
        cache.set('balances' + user.email, {institution_name:account_balances})
    else:
        balances = cache.get('balances' + user.email)
        cache.delete('balances' + user.email)

        balances[institution_name] = account_balances


"""
@params:
- view_func: function
  The view function to wrap

@description:
This function is a decorator that wraps a view function and catches two custom exceptions: TransactionsNotLinkedException and PlaidQueryException.
If either exception is raised, it returns a JSON response object with the corresponding error message and status code. Otherwise, it calls the original view function.

@return:
The wrapped view function that catches and handles the custom exceptions.
"""
def handle_plaid_errors(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except TransactionsNotLinkedException:
            return Response({'error': 'Transactions Not Linked.'}, content_type='application/json', status=303)
        except PlaidQueryException:
            return Response({'error': 'Something went wrong querying PLAID.'}, content_type='application/json', status=303)

    return wrapped_view

"""
@params:
-user: a user object containing the user's email address and Plaid account information

@Description:
This function retrieves a user's investment data from Plaid and stores it in a cache for future use.
It uses a Plaid API wrapper object and a user object to access the data through the Plaid API.
The function returns a boolean value indicating whether the data retrieval and caching process was successful.


@return:
True if the function executes successfully and stores the user's investment data in the cache
False if the function encounters an error while querying the Plaid API for investment data
"""
def cache_investments(user):
    if settings.PLAID_DEVELOPMENT:
        wrapper = DevelopmentWrapper()
    else:
        wrapper = SandboxWrapper()
    stock_getter = StocksGetter(wrapper)
    try:
        stock_getter.query_investments(user)
    except InvestmentsNotLinked:
        return False
    cache.set('investments' + user.email, stock_getter.investments)
    return True

"""
@params:
cache_type_string: a string representing the type of cached data to be deleted
user: a user object containing the user's email address

@Description: This function deletes cached data associated with a specified cache type string and user.
If the specified cache data exists in the cache, it is deleted.

@returns: None
"""
def delete_cached(cache_type_string, user):
    if cache.has_key(cache_type_string + user.email):
        cache.delete(cache_type_string + user.email)
