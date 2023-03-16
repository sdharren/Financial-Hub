import json
from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from assetManager.models import User
from assetManager.assets.debit_card import DebitCard
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from assetManager.transactionInsight.bank_graph_data import BankGraphData
from dateutil.tz import tzlocal
import datetime
from django.http import JsonResponse
from .serializers import UserSerializer
from assetManager.models import User
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.API_wrappers.plaid_wrapper import InvalidPublicToken, LinkTokenNotCreated
from assetManager.investments.stocks import StocksGetter, InvestmentsNotLinked
from assetManager.assets.debit_card import DebitCard
from assetManager.API_wrappers.plaid_wrapper import PublicTokenNotExchanged
from forex_python.converter import CurrencyRates
from decimal import Decimal

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh'
    ]
    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFirstName(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def investment_categories(request):
    try:
        stock_getter = retrieve_stock_getter(request.user)
    except InvestmentsNotLinked:
        return Response({'error': 'Investments not linked.'}, content_type='application/json', status=303)
    categories = stock_getter.get_investment_categories()
    return Response(categories, content_type='application/json', status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def investment_category_breakdown(request):
    try:
        stock_getter = retrieve_stock_getter(request.user)
    except InvestmentsNotLinked:
        return Response({'error': 'Investments not linked.'}, content_type='application/json', status=303)
    if request.GET.get('param'):
        category = request.GET.get('param')
    else:
        return Response({'error': 'Bad request. Param not specified.'}, 400)
    data = stock_getter.get_investment_category(category)
    return Response(data, content_type='application/json', status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def investment_category_names(request):
    try:
        stock_getter = retrieve_stock_getter(request.user)
    except InvestmentsNotLinked:
        return Response({'error': 'Investments not linked.'}, content_type='application/json', status=303)
    categories = stock_getter.get_categories()
    # TODO: handle no categories
    data = {'categories': categories}
    return Response(data, content_type='application/json', status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stock_history(request):
    try:
        stock_getter = retrieve_stock_getter(request.user)
    except InvestmentsNotLinked:
        return Response({'error': 'Investments not linked.'}, content_type='application/json', status=303)
    if request.GET.get('param'):
        stock_name = request.GET.get('param')
        stock_ticker = stock_getter.get_stock_ticker(stock_name)
    else:
        return Response({'error': 'Bad request. Param not specified.'}, status=400)
    data = stock_getter.get_stock_history(stock_ticker)
    return Response(data, content_type='application/json', status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def supported_investments(request):
    try:
        stock_getter = retrieve_stock_getter(request.user)
    except InvestmentsNotLinked:
        return Response({'error': 'Investments not linked.'}, content_type='application/json', status=303)
    stocks = stock_getter.get_supported_investments()
    #TODO: handle no stocks
    data = {'investments': stocks}
    return Response(data, content_type='application/json', status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def link_token(request):
    if request.GET.get('product'):
        product = request.GET.get('product')
        cache.set('product_link' + request.user.email, [product])
    else:
        return Response({'error': 'Bad request. Product not specified.'}, status=400)
    wrapper = DevelopmentWrapper()

    try:
        wrapper.create_link_token([product])
    except LinkTokenNotCreated:
        return Response({'error': 'Bad request.'}, status=400)

    link_token = wrapper.get_link_token()
    response_data = {'link_token': link_token}
    return Response(response_data, content_type='application/json', status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def exchange_public_token(request):
    products_selected = ['transactions'] #NOTE: hardcoded for now
    #TODO: uncomment line below for prod
    #products_selected = cache.get('product_link' + request.user.email)
    cache.delete('product_link' + request.user.email)
    wrapper = DevelopmentWrapper()
    public_token = request.POST.get('public_token')
    if public_token is None:
        return Response({'error': 'Bad request. Public token not specified.'}, status=400)
    try:
        wrapper.exchange_public_token(public_token)
    except InvalidPublicToken as e:
        return Response({'error': 'Bad request. Invalid public token.'}, status=400)
    wrapper.save_access_token(request.user, products_selected)
    return Response(status=200)

@api_view(['PUT', 'DELETE']) #NOTE: Is GET appropriate for this type of request?
@permission_classes([IsAuthenticated])
def cache_assets(request):
    if request.method == 'PUT':
        user = request.user
        if settings.PLAID_DEVELOPMENT:
            wrapper = DevelopmentWrapper()
        else:
            wrapper = SandboxWrapper()
        #TODO: same thing for bank stuff
        #NOTE: do we need this for crypto?
        stock_getter = StocksGetter(wrapper)
        try:
            stock_getter.query_investments(user)
        except InvestmentsNotLinked:
            return Response({'error': 'Investments not linked.'}, content_type='application/json', status=303)
        cache.set('investments' + user.email, stock_getter.investments)
    elif request.method == 'DELETE':
        user = request.user
        if cache.has_key('investments' + user.email):
            cache.delete('investments' + user.email)
    return Response(status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sandbox_investments(request):
    user = request.user
    if cache.has_key('investments' + user.email):
        return Response(status=201)
    wrapper = SandboxWrapper()
    public_token = wrapper.create_public_token(bank_id='ins_115616', products_chosen=['investments'])
    wrapper.exchange_public_token(public_token)
    wrapper.save_access_token(user, products_chosen=['investments'])
    stock_getter = StocksGetter(wrapper)
    stock_getter.query_investments(user)
    cache.set('investments' + user.email, stock_getter.investments)
    return Response(status=200)

def retrieve_stock_getter(user):
    if cache.has_key('investments' + user.email):
        stock_getter = StocksGetter(None)
        data = cache.get('investments' + user.email)
        stock_getter.investments = data
    else:
        if settings.PLAID_DEVELOPMENT:
            wrapper = DevelopmentWrapper()
        else:
            wrapper = SandboxWrapper()
        stock_getter = StocksGetter(wrapper)
        stock_getter.query_investments(user) #NOTE: can raise InvestmentsNotLinked
        cache.set('investments' + user.email, stock_getter.investments)
    return stock_getter

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def yearlyGraph(request):
    transactions = cacheBankTransactionData(request.user)
    graphData = transactions.yearlySpending()
    return Response(graphData, content_type='application/json')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthlyGraph(request):
    transactions = cacheBankTransactionData(request.user)
    if request.GET.get('param'):
        yearName = request.GET.get('param')
    else:
        raise Exception
        # should return bad request
    graphData = transactions.monthlySpendingInYear(int(yearName))
    return Response(graphData, content_type='application/json')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weeklyGraph(request):
    transactions = cacheBankTransactionData(request.user)
    if request.GET.get('param'):
        date = request.GET.get('param')
    else:
        raise Exception
        # should return bad request
    graphData = transactions.weeklySpendingInYear(date)
    return Response(graphData, content_type='application/json')

def transaction_data_getter(user):
    if settings.PLAID_DEVELOPMENT:
        plaid_wrapper = DevelopmentWrapper()
    else:
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token()
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(user, ['transactions'])

    debitCards = DebitCard(plaid_wrapper,user)
    debitCards.make_graph_transaction_data_insight(datetime.date(2022,6,13),datetime.date(2022,12,16))
    accountData = debitCards.get_insight_data()
    first_key = next(iter(accountData))
    return accountData[first_key]
    # return accountData[0]

def cacheBankTransactionData(user):
    if False==cache.has_key('transactions' + user.email):
        cache.set('transactions' + user.email, json.dumps(transaction_data_getter(user).transactionInsight.transaction_history))
    return BankGraphData(json.loads(cache.get('transactions' + user.email)))


def get_currency_converter():
    if settings.PLAID_DEVELOPMENT is False:
        input_date = datetime.datetime(2014, 5, 23, 18, 36, 28, 151012)
    else:
        input_date = datetime.datetime.today()

    return input_date
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_currency_data(request):
    user = request.user

    plaid_wrapper = get_balances_wrapper(user)

    if cache.has_key('currency' + user.email):
        return Response(cache.get('currency' + user.email), content_type='application/json', status = 200)

    debit_card = DebitCard(plaid_wrapper,user)
    #try catch to ensure data is returned
    account_balances = debit_card.get_account_balances()
    currency = reformat_balances_into_currency(account_balances)
    proportion_currencies = calculate_perentage_proportions_of_currency_data(currency)
    cache.set('currency' + user.email, proportion_currencies)
    return Response(proportion_currencies, content_type='application/json', status = 200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_balances_data(request):
    user = request.user

    plaid_wrapper = get_balances_wrapper(user)

    if cache.has_key('balances' + user.email):
        account_balances = cache.get('balances' + user.email)
        if(len(list(account_balances.keys()))) != len(plaid_wrapper.retrieve_access_tokens(user,'transactions')):
            delete_balances_cache(user)
        else:
            return Response(reformatBalancesData(account_balances), content_type='application/json', status = 200)

    try:
        debit_card = DebitCard(plaid_wrapper,user)
    except PublicTokenNotExchanged:
        return Response({'error': 'Transactions Not Linked.'}, content_type='application/json', status=303)

    account_balances = debit_card.get_account_balances()
    balances = reformatBalancesData(account_balances)
    cache.set('balances' + user.email, account_balances)

    return Response(balances, content_type='application/json', status = 200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def select_account(request):
    if request.GET.get('param'):
        institution_name = request.GET.get('param')
        if cache.has_key('balances' + request.user.email) is False:
            return Response({'error': 'Balances not queried.'}, content_type='application/json', status=303)
        else:
            account_balances = cache.get('balances' + request.user.email)

        if institution_name not in list(account_balances.keys()):
            return Response({'error': 'Invalid Insitution ID.'}, content_type='application/json', status=303)

        accounts = reformatAccountBalancesData(account_balances,institution_name)

        return Response(accounts, content_type='application/json',status = 200)

    else:
        return Response({'error': 'No param field supplied.'}, content_type='application/json', status=303)


def delete_balances_cache(user):
    cache.delete('balances' + user.email)
