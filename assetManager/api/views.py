import json
from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
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
from .views_helpers import reformat_balances_into_currency,calculate_perentage_proportions_of_currency_data,reformatAccountBalancesData,reformatBalancesData,get_balances_wrapper,check_institution_name_selected_exists

from assetManager.models import AccountType, AccountTypeEnum

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

"""
@params: request

@Description: Gets the users transaction data from cache then returns the relevant transactions to be displayed by the graph

@return: Response: returns a response containing a json that contains the data to display on the bar graph
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def company_spending(request):
    transactions = BankGraphData(cacheBankTransactionData(request.user))
    if request.GET.get('param'):
        sector = request.GET.get('param')
    else:
        raise Exception
        # should return bad request
    graphData = transactions.companySpendingPerSector(sector)
    return Response(graphData, content_type='application/json')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sector_spending(request):
    transactions = BankGraphData(cacheBankTransactionData(request.user))
    graphData = transactions.orderedCategorisedSpending()
    return Response(graphData, content_type='application/json')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def yearlyGraph(request):
    transactions = BankGraphData(cacheBankTransactionData(request.user))
    graphData = transactions.yearlySpending()
    return Response(graphData, content_type='application/json')

"""
@params: request

@Description: Gets the users transaction data from cache then receives the date from the GET request parameter and returns the relevant transactions for that date
     to be displayed by the graph

@return: Response: returns a response containing a json that contains the data to display on the bar graph
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthlyGraph(request):
    transactions = BankGraphData(cacheBankTransactionData(request.user))
    if request.GET.get('param'):
        yearName = request.GET.get('param')
    else:
        raise Exception
        # should return bad request
    graphData = transactions.monthlySpendingInYear(int(yearName))
    return Response(graphData, content_type='application/json')

"""
@params: request

@Description: Gets the users transaction data from cache then receives the date from the GET request parameter and returns the relevant transactions for that date
     to be displayed by the graph

@return: Response: returns a response containing a json that contains the data to display on the bar graph
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weeklyGraph(request):
    transactions = BankGraphData(cacheBankTransactionData(request.user))
    if request.GET.get('param'):
        date = request.GET.get('param')
    else:
        raise Exception
        # should return bad request
    graphData = transactions.weeklySpendingInYear(date)
    return Response(graphData, content_type='application/json')

"""
@params: user

@Description: Sets the correct wrapper depending on the PLAID_DEVELOPMENT setting and then if it sets the SandboxWrapper it creates all the necessary tokens.
    Then queries plaid for all the transactions from the access tokens stored, and inserts them into a BankGraphData object and returns the relevant object

@return: BankGraphDataObject with the users transaction history stored inside
"""
def transaction_data_getter(user):
    if settings.PLAID_DEVELOPMENT:
        plaid_wrapper = DevelopmentWrapper()
    else:
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token()
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(user, ['transactions'])

    debitCards = DebitCard(plaid_wrapper,user)
    #debitCards.make_graph_transaction_data_insight(datetime.date(2022,6,13),datetime.date(2022,12,16))
    debitCards.make_graph_transaction_data_insight(datetime.date(2000,12,16),datetime.date(2050,12,17))

    accountData = debitCards.get_insight_data()
    first_key = next(iter(accountData))
    return accountData[first_key]

"""
@params: user

@Description: if the transactions for the user have already been cached then it returns the transaction otherwise it caches the transaction data

@return: json of transaction data for the account
"""
def cacheBankTransactionData(user):
    if False==cache.has_key('transactions' + user.email):
        cache.set('transactions' + user.email, json.dumps(transaction_data_getter(user).transactionInsight.transaction_history))

    return (json.loads(cache.get('transactions' + user.email)))

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
        #if(len(list(account_balances.keys()))) != len(plaid_wrapper.retrieve_access_tokens(user,'transactions')):
        #    delete_balances_cache(user)
        #else:
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recent_transactions(request):
    user = request.user
    if request.GET.get('param'):
        institution_name = request.GET.get('param')
        bank_graph_data_insight = cacheBankTransactionData(user)
        if(check_institution_name_selected_exists(user,institution_name) is False):
            return Response({'error': 'Institution Selected Is Not Linked.'}, content_type='application/json', status=303)
        concrete_wrapper = DevelopmentWrapper()
        debit_card = DebitCard(concrete_wrapper,user)

        recent_transactions = debit_card.get_recent_transactions(bank_graph_data_insight,institution_name)
        return Response(recent_transactions,content_type='application/json',status = 200)
    else:
        return Response({'error': 'Institution Name Not Selected'}, content_type='application/json', status=303)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_linked_assets(request):
    account_type = AccountType.objects.filter(user = request.user, account_asset_type = AccountTypeEnum.DEBIT)
    reformatted = [account_type.account_institution_name]
    return Response(reformatted, content_type='application/json',status = 200)
