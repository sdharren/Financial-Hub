import json
from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from assetManager.transactionInsight.bank_graph_data import BankGraphData
from .serializers import UserSerializer
from assetManager.API_wrappers.plaid_wrapper import InvalidPublicToken, LinkTokenNotCreated
from assetManager.API_wrappers.plaid_wrapper import PublicTokenNotExchanged
from assetManager.API_wrappers.crypto_wrapper import save_wallet_address, get_wallets
from .views_helpers import *
from django.http import HttpResponseBadRequest, HttpResponse,HttpRequest
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
def returns(request):
    try:
        stock_getter = retrieve_stock_getter(request.user)
    except InvestmentsNotLinked:
        return Response({'error': 'Investments not linked.'}, content_type='application/json', status=303)

    if request.GET.get('param'):
        stock_name = request.GET.get('param')
    else:
        return Response({'error': 'Bad request. Param not specified.'}, status=400)
    returns = stock_getter.get_returns(stock_name)
    return Response(returns, status=200, content_type='application/json')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_returns(request):
    try:
        stock_getter = retrieve_stock_getter(request.user)
    except InvestmentsNotLinked:
        return Response({'error': 'Investments not linked.'}, content_type='application/json', status=303)

    if request.GET.get('param'):
        category = request.GET.get('param')
    else:
        return Response({'error': 'Bad request. Param not specified.'}, status=400)
    returns = stock_getter.get_category_returns(category)
    return Response(returns, status=200, content_type='application/json')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def overall_returns(request):
    try:
        stock_getter = retrieve_stock_getter(request.user)
    except InvestmentsNotLinked:
        return Response({'error': 'Investments not linked.'}, content_type='application/json', status=303)

    returns = stock_getter.get_overall_returns()
    return Response(returns, status=200, content_type='application/json')

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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def link_crypto_wallet(request):
    user = request.user
    if request.GET.get('param'):
        address = request.GET.get('param')
    else:
        return Response({'error': 'Bad request. Product not specified.'}, status=400)

    save_wallet_address(user, address)

    return Response(status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_crypto_wallets(request):
    user = request.user
    allWallets = get_wallets(user)

    return Response(allWallets, content_type='application/json', status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def exchange_public_token(request):
    if cache.has_key('product_link' + request.user.email):
        products_selected = cache.get('product_link' + request.user.email)
    else:
        return Response({'error': 'Link was not initialised correctly.'}, status=303) # redirect to plaid link on front end
    cache.delete('product_link' + request.user.email)

    #wrapper = DevelopmentWrapper()
    if settings.PLAID_DEVELOPMENT:
        wrapper = DevelopmentWrapper()
    else:
        wrapper = SandboxWrapper()

    public_token = request.data.get('public_token')
    if public_token is None:
        return Response({'error': 'Bad request. Public token not specified.'}, status=400)

    try:
        wrapper.exchange_public_token(public_token)
    except InvalidPublicToken as e:
        return Response({'error': 'Bad request. Invalid public token.'}, status=400)

    #if statement that checks whether the new access token is for transactions
    wrapper.save_access_token(request.user, products_selected)
    token = wrapper.get_access_token()

    if('transactions' in products_selected):
        #update balances cache if it exists
        token = wrapper.get_access_token()
        set_single_institution_balances_and_currency(token,wrapper,request.user)

    #write a function in helpers it takes an access token, queries plaid for that access token and if
    #single institution thingy
    #check duplicate for institution should be done in save access_token
    return Response(status=200)

"""
@params:
request: Django request object
@api_view(['PUT', 'DELETE']): decorator to indicate that the view only accepts PUT and DELETE HTTP requests.
@permission_classes([IsAuthenticated]): decorator that verifies whether the user is authenticated.
handle_plaid_errors: decorator that handles Plaid API errors.
@Description:

This function is a Django view that either caches or deletes investment, bank balance, and currency data for an authenticated user.
If the request is a PUT, the function first verifies that the user has linked investments, then proceeds to cache the user's investment data, bank balance data, and currency data.
If the request is a DELETE, the function deletes all cached data related to the user's investments, transactions, currency, and balances.

@return: A Response object with a status code of 200.
"""
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@handle_plaid_errors
def cache_assets(request):
    if request.method == 'PUT':
        user = request.user
        if settings.PLAID_DEVELOPMENT: # TODO: remove wrapper from here later they should be created within each methods
            wrapper = DevelopmentWrapper()
        else:
            wrapper = SandboxWrapper()

        if not cache_investments(user): #try to cache investments
            return Response({'error': 'Investments not linked.'}, content_type='application/json', status=303)

        #caching of bank related investements
        #Balances ##SERGY THESE ARE THE ONES TO MOVE
        account_balances = get_institutions_balances(wrapper,request.user)
        cache.set('balances' + user.email, account_balances)
        cache.set('currency' + user.email,calculate_perentage_proportions_of_currency_data(reformat_balances_into_currency(account_balances)))
        #cacheBankTransactionData(request.user) #transactions

    elif request.method == 'DELETE':
        user = request.user
        delete_cached('investments', user)
        delete_cached('transactions', user)
        delete_cached('currency', user)
        delete_cached('balances', user)

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
@params: an HTTP request object containing user authentication information

@Description: Gets the users transaction data from cache then inputs it into BankGraphData.
Then gets the sector as a parameter from the GET request and then gets the spending per company in that sector

@return: Response: returns a response containing a json that contains the data to display on the bar graph
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def company_spending(request):
    transactions = BankGraphData(getCachedInstitutionCachedData(request.user))
    if request.GET.get('param'):
        sector = request.GET.get('param')
    else:
        raise Exception
        # should return bad request
    graphData = transactions.companySpendingPerSector(sector)
    return Response(graphData, content_type='application/json')

"""
@params: an HTTP request object containing user authentication information

@Description: Gets the users transaction data from cache then inputs it into BankGraphData that then gets the spending per sector

@return: Response: returns a response containing a json that contains the data to display on the bar graph
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sector_spending(request):
    transactions = BankGraphData(getCachedInstitutionCachedData(request.user))
    graphData = transactions.orderedCategorisedSpending()
    return Response(graphData, content_type='application/json')

"""
@params: an HTTP request object containing user authentication information

@Description: Gets the users transaction data from cache then returns the relevant transactions to be displayed by the graph

@return: Response: returns a response containing a json that contains the data to display on the bar graph
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def yearlyGraph(request):
    transactions = BankGraphData(getCachedInstitutionCachedData(request.user))
    graphData = transactions.yearlySpending()
    return Response(graphData, content_type='application/json')

"""
@params: an HTTP request object containing user authentication information

@Description: Gets the users transaction data from cache then receives the date from the GET request parameter and returns the relevant transactions for that date
     to be displayed by the graph

@return: Response: returns a response containing a json that contains the data to display on the bar graph
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthlyGraph(request):
    transactions = BankGraphData(getCachedInstitutionCachedData(request.user))
    if request.GET.get('param'):
        yearName = request.GET.get('param')
    else:
        raise Exception
        # should return bad request
    graphData = transactions.monthlySpendingInYear(int(yearName))
    return Response(graphData, content_type='application/json')

"""
@params: an HTTP request object containing user authentication information

@Description: Gets the users transaction data from cache then receives the date from the GET request parameter and returns the relevant transactions for that date
     to be displayed by the graph

@return: Response: returns a response containing a json that contains the data to display on the bar graph
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weeklyGraph(request):
    transactions = BankGraphData(getCachedInstitutionCachedData(request.user))
    if request.GET.get('param'):
        date = request.GET.get('param')
    else:
        raise Exception
        # should return bad request
    graphData = transactions.weeklySpendingInYear(date)
    return Response(graphData, content_type='application/json')


"""
@params:
request: an HTTP request object containing user authentication information

@Description: This function retrives the data from the request body and decodes it.
Then indexes the user's access tokens to find the corresponding token to the one selected by the user.
It then deletes the previous cached instiution name and caches a new one to correlate to the change in institution selected

@return:
A Response object returning that the status is 200
"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_bank_access_token(request):
    data = request.body
    decoded_data = data.decode('utf-8')
    parsed_data = json.loads(decoded_data)
    access_token_id = int(parsed_data['selectedOption'])
    plaid_wrapper = get_plaid_wrapper(request.user,'balances')
    debitCards = DebitCard(plaid_wrapper,request.user)
    access_token = debitCards.access_tokens[access_token_id]
    cache.delete('access_token'+request.user.email)
    cache.set('access_token'+request.user.email,debitCards.get_institution_name_from_db(access_token))
    return Response(status=200)

"""
@params:
request: Django request object
@api_view(['GET]): decorator to indicate that the view only accepts GET HTTP requests.
@permission_classes([IsAuthenticated]): decorator that verifies whether the user is authenticated.
handle_plaid_errors: decorator that handles Plaid API errors.

@Description: This function retrieves and formats currency data associated with a given user.
The function uses a Plaid API wrapper object and a user object to access the data through the Plaid API.
If the currency data has already been retrieved and cached, the function returns the cached data.
Otherwise, the function retrieves the data and formats it into percentage proportions before caching it for future use.

@return:
A Response object containing the cached currency data if it exists
A Response object containing the formatted currency data if it does not exist in the cache
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@handle_plaid_errors
def get_currency_data(request):
    user = request.user

    plaid_wrapper = get_plaid_wrapper(user,'balances')

    if cache.has_key('currency' + user.email):
        return Response(cache.get('currency' + user.email), content_type='application/json', status = 200)

    account_balances = get_institutions_balances(plaid_wrapper,user)

    currency = reformat_balances_into_currency(account_balances)
    proportion_currencies = calculate_perentage_proportions_of_currency_data(currency)
    cache.set('currency' + user.email, proportion_currencies)

    return Response(proportion_currencies, content_type='application/json', status = 200)

"""
@params:
request: Django request object
@api_view(['GET]): decorator to indicate that the view only accepts GET HTTP requests.
@permission_classes([IsAuthenticated]): decorator that verifies whether the user is authenticated.
handle_plaid_errors: decorator that handles Plaid API errors.

@Description: This function retrieves and formats balance data associated with a given user.
The function uses a Plaid API wrapper object and a user object to access the data through the Plaid API.
If the balance data has already been retrieved and cached, the function returns the cached data.
Otherwise, the function retrieves the data and formats it before caching it for future use.

@return:
A Response object containing the cached balance data if it exists
A Response object containing the formatted balance data if it does not exist in the cache
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@handle_plaid_errors
def get_balances_data(request):
    user = request.user

    plaid_wrapper = get_plaid_wrapper(user,'balances')
    if cache.has_key('balances' + user.email):
        account_balances = cache.get('balances' + user.email)
        return Response(reformatBalancesData(account_balances), content_type='application/json', status = 200)

    account_balances = get_institutions_balances(plaid_wrapper,user)

    balances = reformatBalancesData(account_balances)
    cache.set('balances' + user.email, account_balances)
    return Response(balances, content_type='application/json', status = 200)

"""
@param:
request: Django request object
@api_view(['GET]): decorator to indicate that the view only accepts GET HTTP requests.
@permission_classes([IsAuthenticated]): decorator that verifies whether the user is authenticated.
handle_plaid_errors: decorator that handles Plaid API errors.

@Description: This function retrieves account balance data for a specific institution associated with a given user.
The function uses a user object to access the data through a caching system.
If the balance data has not been retrieved and cached, an error response is returned.
If the institution name is not valid, another error response is returned. Otherwise, the function formats the data and returns it.

@Return:
A Response object containing the formatted account balance data for a specific institution if the institution name is valid
An error Response object if the institution name is not valid or if the balance data has not been retrieved and cached
"""
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

"""
@param:
request: Django request object
@api_view(['GET]): decorator to indicate that the view only accepts GET HTTP requests.
@permission_classes([IsAuthenticated]): decorator that verifies whether the user is authenticated.
handle_plaid_errors: decorator that handles Plaid API errors.

@Description: This function retrieves institution names associated with a given user's access tokens.
The function then gives each institution its own id

@Return:
A Response object containing an array of dictionaries each containg an id and name
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def select_bank_account(request):
    user = request.user
    plaid_wrapper = get_plaid_wrapper(user,'transactions')
    debitCards = DebitCard(plaid_wrapper,user)
    institutions = []
    institution_id = 0
    for tokens in debitCards.access_tokens:
        account ={"id":institution_id, "name": debitCards.get_institution_name_from_db(tokens)}
        institutions.append(account)
        institution_id = institution_id + 1
    return Response(institutions,status=200)

"""
@params:
request: Django request object
@api_view(['GET]): decorator to indicate that the view only accepts GET HTTP requests.
@permission_classes([IsAuthenticated]): decorator that verifies whether the user is authenticated.
handle_plaid_errors: decorator that handles Plaid API errors.

@Description:
    This function retrieves recent transactions of a user's bank account from the Plaid API.
    At most five of the most recent transactions as a list of dictionaries containing the name, amount, category and merchant as keys

@returns:
    If the institution name is provided in the request, the function returns the recent transactions of that institution in JSON format with a status code of 200.

    If the institution name is not provided in the request, the function returns an error message indicating that the institution name is not selected with a status code of 303.

    If an exception occurs while querying the Plaid API, the function raises a custom exception named PlaidQueryException.
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@handle_plaid_errors
def recent_transactions(request):
    user = request.user
    if request.GET.get('param'):
        institution_name = request.GET.get('param')

        try:
            bank_graph_data_insight = getCachedInstitutionData(user,institution_name)
        except TransactionsNotLinkedException:
            raise TransactionsNotLinkedException('Transactions Not Linked.')
        except Exception:
            raise PlaidQueryException('Something went wrong querying PLAID.')

        concrete_wrapper = DevelopmentWrapper()

        debit_card = make_debit_card(concrete_wrapper,user)

        try:
            recent_transactions = debit_card.get_recent_transactions(bank_graph_data_insight,institution_name)
        except Exception:
            raise PlaidQueryException('Something went wrong querying PLAID.')


        return Response(recent_transactions,content_type='application/json',status = 200)
    else:
        return Response({'error': 'Institution Name Not Selected'}, content_type='application/json', status=303)


"""
    @params:
        request (HttpRequest): the HTTP request object.

    @Description:
        Retrieve the linked banks for the authenticated user.

    @return:
        Response: the HTTP response object containing a list of institution names in JSON format.
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_linked_banks(request):

    account_types = AccountType.objects.filter(user = request.user, account_asset_type = AccountTypeEnum.DEBIT)
    institutions = []
    for account in account_types:
        institutions.append(account.account_institution_name)
    return Response(institutions, content_type='application/json',status = 200)

"""
    @params:
        request (HttpRequest): the HTTP request object.

    @Description:
        Retrieve the linked brokerages for the authenticated user.

    @return:
        Response: the HTTP response object containing a list of brokerage names in JSON format.

"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def linked_brokerage(request):
    account_types = AccountType.objects.filter(user = request.user, account_asset_type = AccountTypeEnum.STOCK)
    brokerages = []
    for brokerage in account_types:
        brokerages.append(brokerage.account_institution_name)
    return Response(brokerages, content_type='application/json',status = 200)


"""
    @params:
        request: The HTTP request object that contains information about the current request.
        institution: The name of the linked institution account to be deleted.

    @Description:
        This function deletes a linked institution account associated with the authenticated user and the given institution name, and returns a 204 (No Content) response.

    @return:
        A HttpResponse object with status code 204 (No Content) if the account was successfully deleted.
        A HttpResponseBadRequest object with an error message if the account was not found.

"""
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_linked_banks(request, institution):

    account_type = AccountType.objects.filter(user=request.user, account_asset_type=AccountTypeEnum.DEBIT, account_institution_name=institution).first()

    if not account_type:
     return HttpResponseBadRequest('Linked bank account not found')

    account_type.delete()
    return HttpResponse(status=204)


"""
    @params:
        request: The HTTP request object that contains information about the current request.
        brokerage: The name of the linked brokerage account to be deleted.

    @Description:
        This function deletes a linked brokerage account associated with the authenticated user and the given brokerage name, and returns a 204 (No Content) response.

    @return:
        A HttpResponse object with status code 204 (No Content) if the account was successfully deleted.
        A HttpResponseBadRequest object with an error message if the account was not found.

"""
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_linked_brokerage(request, brokerage):

    account_type = AccountType.objects.filter(user=request.user, account_asset_type=AccountTypeEnum.STOCK, account_institution_name=brokerage).first()

    if not account_type:
     return HttpResponseBadRequest('Linked brokerage account not found')

    account_type.delete()
    return HttpResponse(status=204)
