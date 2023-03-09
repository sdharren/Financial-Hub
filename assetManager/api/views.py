import json
from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from assetManager.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer
from assetManager.models import User
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.API_wrappers.plaid_wrapper import InvalidPublicToken
from assetManager.investments.stocks import StocksGetter
from assetManager.assets.debit_card import DebitCard

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def investment_categories(request):
    stock_getter = retrieve_stock_getter(request.user)
    categories = stock_getter.get_investment_categories()
    return Response(categories, content_type='application/json', status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def investment_category_breakdown(request):
    stock_getter = retrieve_stock_getter(request.user)
    if request.GET.get('param'):
        category = request.GET.get('param')
    else:
        return Response({'error': 'Bad request. Param not specified.'})
    data = stock_getter.get_investment_category(category)
    return Response(data, content_type='application/json', status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stock_history(request):
    stock_getter = retrieve_stock_getter(request.user)
    if request.GET.get('param'):
        stock_name = request.GET.get('stock_name')
        stock_ticker = stock_getter.get_stock_ticker(stock_name)
    else:
        return Response({'error': 'Bad request. Param not specified.'}, status=500)
        #return bad request
    data = stock_getter.get_stock_history(stock_ticker)
    return Response(data, content_type='application/json', status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def create_link_token(request):
    if request.GET.get('product'):
        product = request.GET.get('product')
        cache.set('product_link' + request.user.email, [product])
    else:
        return Response({'error': 'Bad request. Product not specified.'}, status=500)
    wrapper = DevelopmentWrapper()
    wrapper.create_link_token([product])
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
    try:
        wrapper.exchange_public_token(request.data['public_token'])
    except InvalidPublicToken as e:
        print(str(e)) # for debugging
        return Response({'error': 'Bad request. Invalid public token.'}, status=500)
    wrapper.save_access_token(request.user, products_selected)
    return Response(status=200)

@api_view(['GET']) #NOTE: Is GET appropriate for this type of request?
@permission_classes([IsAuthenticated])
def cache_assets(request):
    user = request.user
    if settings.PLAID_DEVELOPMENT:
        wrapper = DevelopmentWrapper()
    else:
        wrapper = SandboxWrapper()
    #TODO: same thing for bank stuff
    #NOTE: do we need this for crypto?
    stock_getter = StocksGetter(wrapper)
    stock_getter.query_investments(user)
    cache.set('investments' + user.email, stock_getter.investments)
    return Response(status=200)


#TODO: handle error if investments aren't cached
def retrieve_stock_getter(user):
    stock_getter = StocksGetter(None)
    data = cache.get('investments' + user.email)
    stock_getter.investments = data
    return stock_getter


def reformatAccountBalancesData(account_balances,institution_name):
    accounts = {}
    for account in account_balances[institution_name].keys():
        total = 0
        total += account_balances[institution_name][account]['available_amount']
        accounts[account] = total

    return accounts

def reformatBalancesData(account_balances):
    if type(account_balances) is not dict:
        raise TypeError("account balances must be of type dict")

    balances = {}

    for institution_name in account_balances.keys():
        total = 0
        for account_id in account_balances[institution_name].keys():
            total += account_balances[institution_name][account_id]['available_amount']


        balances[institution_name] = total

    return balances

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_balances_data(request):
    if settings.PLAID_DEVELOPMENT:
        plaid_wrapper = DevelopmentWrapper()
    else:
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token_custom_user()
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(request.user, ['transactions'])


    debit_card = DebitCard(plaid_wrapper,request.user)

    account_balances = debit_card.get_account_balances()
    balances = reformatBalancesData(account_balances)

    return Response(balances, content_type='application/json', status = 200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def select_account(request):
        if request.GET.get('param'):
            institution_name = request.GET.get('param')

            if settings.PLAID_DEVELOPMENT:
                plaid_wrapper = DevelopmentWrapper()
            else:
                plaid_wrapper = SandboxWrapper()
                public_token = plaid_wrapper.create_public_token_custom_user()
                plaid_wrapper.exchange_public_token(public_token)
                plaid_wrapper.save_access_token(request.user, ['transactions'])

            debit_card = DebitCard(plaid_wrapper,request.user)

            account_balances = debit_card.get_account_balances()

            if institution_name not in list(account_balances.keys()):
                raise Exception("Provided institution name does not exist in the requested accounts")

            accounts = reformatAccountBalancesData(account_balances,institution_name)

            return Response(accounts, content_type='application/json',status = 200)

        else:
            raise Exception("No param field supplied to select_account url")
