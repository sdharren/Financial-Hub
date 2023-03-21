from django.conf import settings
from assetManager.assets.debit_card import DebitCard
from assetManager.transactionInsight.bank_graph_data import BankGraphData,get_currency_converter
import datetime
from assetManager.models import User,AccountType,AccountTypeEnum
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.investments.stocks import StocksGetter, InvestmentsNotLinked
from assetManager.assets.debit_card import DebitCard
from forex_python.converter import CurrencyRates

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

def get_balances_wrapper(user):
    if settings.PLAID_DEVELOPMENT:
        plaid_wrapper = DevelopmentWrapper()
    else:
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token_custom_user()
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(user, ['transactions'])

    return plaid_wrapper

def check_institution_name_selected_exists(user,institution_name):
    instituitions = AccountType.objects.filter(user = user, account_asset_type = AccountTypeEnum.DEBIT)

    for account in instituitions:
        if account.account_institution_name == institution_name:
            return True

    return False
