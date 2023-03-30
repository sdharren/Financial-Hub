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
from assetManager.investments.stocks import StocksGetter, InvestmentsNotLinked
from assetManager.API_wrappers.crypto_wrapper import getAllCryptoData, getAlternateCryptoData, save_wallet_address, get_wallets
from assetManager.API_wrappers.plaid_wrapper import InvalidPublicToken, LinkTokenNotCreated
from .views_helpers import *
from django.http import HttpResponseBadRequest, HttpResponse
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

"""
@params: an HTTP request object containing user authentication information

@description:
This function checks cache to see if the total assets data has already been cached, if it has it returns it.
if not this function retrives the total assets of Bank, Stocks and Crypto and adds them into a dictionary and then caches that

@return:
A dictionary with the sum of all assets for each of the three categories
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def total_assets(request):
    user = request.user
    if False == cache.has_key('total_assets'+user.email):
        wrapper = get_plaid_wrapper(user,'balances')
        try:
            bank_assets = sum_instiution_balances(wrapper, request.user)
        except Exception:
            bank_assets = 0
        investment_assets = sum_investment_balance(user)
        crypto_assets = sum_crypto_balances(user)
        data = {"Bank Assets": bank_assets, "Investment Assets": investment_assets, "Crypto Assets": crypto_assets}
        cache.set('total_assets'+user.email, data, 86400)
    else:
        data = cache.get('total_assets'+user.email)
    return Response(data, content_type='application/json', status=200)

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

"""
@params:
request: An HTTP request object.

@description:
This function is a view function that returns a list of investment categories for the authenticated user. It first retrieves
a stock_getter object, which is responsible for retrieving the user's investment data, using the retrieve_stock_getter()
method. If the user's investments are not linked, an error message is returned. Otherwise, the get_investment_categories()
method of the stock_getter object is called to retrieve the list of investment categories, which is returned in the
HTTP response.

@return:
An HTTP response containing a list of investment categories for the authenticated user, or an error message if the user's
investments are not linked.
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def investment_categories(request):
    try:
        stock_getter = retrieve_stock_getter(request.user)
    except InvestmentsNotLinked:
        return Response({'error': 'Investments not linked.'}, content_type='application/json', status=303)
    categories = stock_getter.get_investment_categories()
    return Response(categories, content_type='application/json', status=200)

"""
@params:
request: Django request object

@description:
This API view method is used to retrieve investment category breakdown for the authenticated user. The category is passed in as a request parameter.

@return:
A Django Response object containing the investment category breakdown data for the specified category.
"""
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

"""
@params:
    request: Django request object
@description:
    This API view returns a list of all available investment categories.
@returns:
    Returns a JSON object with the list of categories under the 'categories' key and a status code of 200.
    If the user's investments are not linked, returns an error JSON object with the 'error' key and a status code of 303.
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def investment_category_names(request):
    try:
        stock_getter = retrieve_stock_getter(request.user)
    except InvestmentsNotLinked:
        return Response({'error': 'Investments not linked.'}, content_type='application/json', status=303)
    categories = stock_getter.get_categories()
    data = {'categories': categories}
    return Response(data, content_type='application/json', status=200)

"""
@params:
    request: the HTTP request object containing the user session information
@description:
    Given an authenticated user session, retrieves the stock history data for a particular stock by name and returns it in JSON format.
@returns:
    A Response object containing the stock history data in JSON format, or an error message if there was an issue with the request.
"""
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

"""
@params:
    request (HttpRequest): The request object containing information about the current request.
@description:
    View function that handles GET requests for comparing the user's portfolio with a given stock ticker over a given period.
@returns:
    A JSON response containing the portfolio comparison data and an HTTP status code.
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def portfolio_comparison(request):
    try:
        stock_getter = retrieve_stock_getter(request.user)
    except InvestmentsNotLinked:
        return Response({'error': 'Investments not linked.'}, content_type='application/json', status=303)

    if request.GET.get('param'):
        ticker = request.GET.get('param')
    else:
        return Response({'error': 'Bad request. Param not specified.'}, status=400)

    comparison = stock_getter.get_portfolio_comparison(ticker, period=6)

    return Response(comparison, content_type='application/json', status=200)

"""
@params:
    request: HttpRequest object
@description:
    This view returns a list of all supported investments (e.g. stocks, mutual funds) that can be queried in the API.
@returns:
    Returns a JSON response containing a list of supported investments.
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def supported_investments(request):
    try:
        stock_getter = retrieve_stock_getter(request.user)
    except InvestmentsNotLinked:
        return Response({'error': 'Investments not linked.'}, content_type='application/json', status=303)
    stocks = stock_getter.get_supported_investments()
    data = {'investments': stocks}
    return Response(data, content_type='application/json', status=200)

"""
@params:
    request: HttpRequest object
@description:
    Returns the returns data for a given stock investment.
@returns:
    A Response object containing the returns data in JSON format.
"""
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

"""
@params:
    request: HttpRequest object representing the incoming request
@description:
    This method fetches the returns of a specified investment category from the stock getter for a user.
@returns:
    Returns a HTTP Response object with the investment category returns in JSON format with a success status code of 200. If the investments are not linked for the user, returns a HTTP Response object with an error message in JSON format with a status code of 303. If the parameter is not specified in the request, returns a HTTP Response object with an error message in JSON format with a status code of 400.
"""
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

"""
@params:
    request: Request object
@description:
    Retrieves the overall returns of all investments of the user.
@returns:
    Returns a Response object with the returns data in JSON format, with a 200 status code if successful, or an error message with a 303 status code if the user's investments are not linked.
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def overall_returns(request):
    try:
        stock_getter = retrieve_stock_getter(request.user)
    except InvestmentsNotLinked:
        return Response({'error': 'Investments not linked.'}, content_type='application/json', status=303)

    returns = stock_getter.get_overall_returns()
    return Response(returns, status=200, content_type='application/json')

"""
@params:
    request: The HTTP request object
@description:
    Links an investment account by creating a link token for the user's desired product and storing it in the cache for a day.
@returns:
    A JSON response containing a link token.
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def link_token(request):
    if request.GET.get('product'):
        product = request.GET.get('product')
        cache.set('product_link' + request.user.email, [product], 86400)
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

"""
@params: request: HTTP request object containing information about the user and the GET parameters.

@Description: This function is responsible for linking a user's cryptocurrency wallet address to their account.
It retrieves the user object from the request, checks if the 'param' parameter is present in the GET request,
and saves the wallet address to the user's account using the save_wallet_address() function.
It then retrieves all of the user's cryptocurrency data using getAllCryptoData(), caches it using the cache.set() function, and returns a HTTP 200 response.

@return: Response object: A HTTP response object with a status code of 200 if the wallet address is successfully linked,
or a status code of 400 with an error message if the 'param' parameter is not present in the GET request.
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def link_crypto_wallet(request):
    user = request.user
    if request.GET.get('param'):
        address = request.GET.get('param')
    else:
        return Response({'error': 'Bad request. Product not specified.'}, status=400)

    save_wallet_address(user, address)

    data = getAllCryptoData(user)
    cache.set("crypto" + user.email, data)
    delete_cached('total_assets', request.user)

    return Response(status=200)

"""
@params: request: an HTTP request object

@Description: This function takes an HTTP request object and returns a JSON response containing all the crypto wallets associated with the user making the request.
It calls the "get_wallets" function with the user object extracted from the request to retrieve all the wallets. The JSON response is returned with a status code of 200.

@return: Response: a JSON response containing all the crypto wallets associated with the user making the request.
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_crypto_wallets(request):
    user = request.user
    allWallets = get_wallets(user)

    if (not allWallets):
        return Response({'error': 'Crypto not linked.'}, status=303, content_type='application/json')

    return Response(allWallets, content_type='application/json', status=200)

"""
@params:
    request: request object

@description:
    This method is responsible for exchanging a public token obtained from Plaid with an access token. It saves the access token and the selected products to the database. If 'transactions' are among the selected products, this method calls two other methods - set_single_institution_balances_and_currency and set_single_institution_transactions, to cache the balances and transactions for the user's accounts. If 'investments' is among the selected products, this method calls the cache_investments function.

@returns:
    A Response object with status 200 if the public token is exchanged successfully. Otherwise, it returns a Response object with an error message and status code indicating the cause of the failure.
"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def exchange_public_token(request):
    if cache.has_key('product_link' + request.user.email):
        products_selected = cache.get('product_link' + request.user.email)
    else:
        return Response({'error': 'Link was not initialised correctly.'}, status=303) # redirect to plaid link on front end
    cache.delete('product_link' + request.user.email)

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

    wrapper.save_access_token(request.user, products_selected)
    token = wrapper.get_access_token()

    delete_cached('total_assets', request.user)

    if('transactions' in products_selected):
        #update balances cache if it exists
        set_single_institution_balances_and_currency(token,wrapper,request.user)
        set_single_institution_transactions(token,wrapper,request.user)

    if 'investments' in products_selected:
        cache_investments(request.user)

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
def cache_assets(request):
    if request.method == 'PUT':
        user = request.user
        if settings.PLAID_DEVELOPMENT: # TODO: remove wrapper from here later they should be created within each methods
            wrapper = DevelopmentWrapper()
        else:
            wrapper = SandboxWrapper()

        cache_investments(user)

        #caching of bank related investements
        try:
            cryptoData = getAllCryptoData(user)
            cache.set("crypto" + user.email, cryptoData)
            account_balances = get_institutions_balances(wrapper,request.user)
            cache.set('balances' + user.email, account_balances, 86400)
            cache.set('currency' + user.email,calculate_perentage_proportions_of_currency_data(reformat_balances_into_currency(account_balances)), 86400)
            cache.set('transactions'+user.email,transaction_data_getter(request.user), 86400) #test this
        except TransactionsNotLinkedException:
            pass


    elif request.method == 'DELETE':
        user = request.user
        delete_cached("crypto", user)
        delete_cached('investments', user)
        delete_cached('transactions', user)
        delete_cached('currency', user)
        delete_cached('balances', user)
        delete_cached('total_assets',user) #test this

    return Response(status=200)

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
        return Response(status=400)
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
@params: request: HTTP request object

@Description: This function retrieves cryptocurrency data for a user. It first checks if the data is already cached for the user, and if so, retrieves it from the cache.
Otherwise, it calls the getAllCryptoData function to fetch the data and stores it in the cache for future use. The function returns the cryptocurrency data as a JSON response.

@return: Response object containing the cryptocurrency data in JSON format
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def crypto_all_data(request):    #test
    if(cache.has_key("crypto" + request.user.email)):
        data = cache.get("crypto" + request.user.email)
    else:
        data = getAllCryptoData(request.user)
        if not data:
            return Response({'error': 'Crypto not linked.'}, status=303, content_type='application/json')
        cache.set("crypto" + request.user.email, data)
    return Response(data, content_type='application/json')


"""
@params: request - Django HttpRequest object containing the request parameters.

@Description: This function is used to fetch cryptocurrency data based on the user's input. The function takes a GET request from the user and checks for a 'param' parameter.
If it exists, the function first checks if the requested data is already stored in the cache. If not, it fetches the data by calling the getAllCryptoData() function and stores
it in the cache. It then calls the getAlternateCryptoData() function to fetch the requested data. If the data is already present in the cache,
it directly fetches the data using cache.get(). If the 'param' parameter is not present, it raises an exception.

@return: The function returns a Django Response object containing the requested cryptocurrency data in JSON format.
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def crypto_select_data(request):
    if request.GET.get('param'):
        if(cache.has_key("crypto" + request.user.email) is False):
            storedData = getAllCryptoData(user=request.user)
            if not storedData:
                return Response({'error': 'Crypto not linked.'}, status=303, content_type='application/json')
            cache.set("crypto" + request.user.email, storedData)
            data = getAlternateCryptoData(user=request.user, command=(request.GET.get('param')), data = storedData)
        else:
            storedData = cache.get("crypto" + request.user.email)
            data = getAlternateCryptoData(user=request.user, command=(request.GET.get('param')), data=storedData)
    else:
        raise Response({'Bad request. Param not specified.'}, status=400, content_type='application/json')
    return Response(data, content_type='application/json')


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
        return Response(status=400)
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
        return Response(status=400)

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
    try:
        data = request.body
        decoded_data = data.decode('utf-8')
        parsed_data = json.loads(decoded_data)
        access_token_id = int(parsed_data['selectedOption'])
        plaid_wrapper = get_plaid_wrapper(request.user,'transactions')
        debitCards = DebitCard(plaid_wrapper,request.user)
        access_token = debitCards.access_tokens[access_token_id]
        cache.delete('access_token'+request.user.email)
        cache.set('access_token'+request.user.email,debitCards.get_institution_name_from_db(access_token), 86400)
        return Response(status=200)
    except Exception:
        return Response(status=400)

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
    cache.set('currency' + user.email, proportion_currencies, 86400)

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
    cache.set('balances' + user.email, account_balances, 86400)
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

    institutions = AccountType.objects.filter(user = user, account_asset_type = AccountTypeEnum.DEBIT)

    if(len(institutions) == 0):
        return Response({'error': 'Transactions Not Linked.'}, content_type='application/json', status=303)

    concrete_wrapper = get_plaid_wrapper(user,'transactions')
    debit_card = make_debit_card(concrete_wrapper,user)
    transactions = {}

    for institution in institutions:
        bank_graph_data_insight = getCachedInstitutionData(user,institution.account_institution_name)
        try:
            recent_transactions = debit_card.get_recent_transactions(bank_graph_data_insight,institution.account_institution_name)
        except Exception:
            return Response({'error': 'Something went wrong querying PLAID.'}, content_type='application/json', status=303)

        transactions[institution.account_institution_name] = recent_transactions

    return Response(transactions,content_type='application/json',status = 200)

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
        return HttpResponseBadRequest('Transactions Not Linked.')

    account_type.delete()

    if(cache.has_key('transactions' + request.user.email)):
        transactions = cache.get('transactions' + request.user.email)
        delete_cached('transactions', request.user)

        if institution in transactions.keys():
            del transactions[institution]

        if len(transactions) != 0:
            cache.set('transactions' + request.user.email, transactions)

    if(cache.has_key('balances' + request.user.email)):
        balances = cache.get('balances' + request.user.email)
        delete_cached('currency', request.user)
        delete_cached('balances', request.user)

        if institution in balances.keys():
            del balances[institution]

        if(len(balances) != 0):
            cache.set('balances' + request.user.email,balances)
            cache.set('currency' + request.user.email,calculate_perentage_proportions_of_currency_data(reformat_balances_into_currency(balances)))

    delete_cached('total_assets', request.user)

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
     return HttpResponseBadRequest('Investments not linked.')

    account_type.delete()

    delete_cached('investments', request.user)
    delete_cached('total_assets', request.user)

    return HttpResponse(status=204)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def linked_crypto(request):
    account_types = AccountType.objects.filter(user = request.user, account_asset_type = AccountTypeEnum.CRYPTO)
    cryptos = []
    for crypto in account_types:
        cryptos.append(crypto.access_token)
    return Response(cryptos, content_type='application/json',status = 200)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_linked_crypto(request, crypto):

    account_type = AccountType.objects.filter(user=request.user, access_token = crypto).first()

    if not account_type:
     return HttpResponseBadRequest('Crypto not linked.')

    account_type.delete()

    if(cache.has_key("crypto" + request.user.email)):
        delete_cached('crypto', request.user)
        cryptoData = getAllCryptoData(request.user)
        cache.set("crypto" + request.user.email, cryptoData)


    delete_cached('total_assets', request.user)
    return HttpResponse(status=204)
