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
from assetManager.transactionInsight.bank_graph_data import BankGraphData
from dateutil.tz import tzlocal
import datetime
from django.http import JsonResponse
from .serializers import UserSerializer
from assetManager.models import User
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.API_wrappers.plaid_wrapper import InvalidPublicToken
from assetManager.investments.stocks import StocksGetter


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
        stock_name = request.GET.get('param')
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

@api_view(['GET'])
def yearlyGraph(request):
    transactions = make_fake_transaction_getter()
    graphData = transactions.yearlySpending()
    return Response(graphData, content_type='application/json')

@api_view(['GET'])
def monthlyGraph(request):
    transactions = make_fake_transaction_getter()
    if request.GET.get('param'):
        yearName = request.GET.get('param')
    else:
        raise Exception
        # should return bad request
    graphData = transactions.monthlySpendingInYear(int(yearName))
    return Response(graphData, content_type='application/json')

@api_view(['GET'])
def weeklyGraph(request):
    transactions = make_fake_transaction_getter()
    if request.GET.get('param'):
        date = request.GET.get('param')
    else:
        raise Exception
        # should return bad request
    graphData = transactions.weeklySpendingInYear(date)
    return Response(graphData, content_type='application/json')

def make_fake_transaction_getter():
     return BankGraphData([{'account_id': 'a9X88M4oEpfBMMjVpOEVUp0m8ykRZ6f3n58M3a',
     'account_owner': None,
     'amount': 3.3,
     'authorized_date': datetime.date(2022, 11, 18),
     'authorized_datetime': None,
     'category': ['Travel', 'Public Transportation Services'],
     'category_id': '22014000',
     'check_number': None,
     'date': datetime.date(2022, 11, 21),
     'datetime': datetime.datetime(2022, 11, 21, 0, 0, tzinfo=tzlocal()),
     'iso_currency_code': 'GBP',
     'location': {'address': None,
                  'city': None,
                  'country': None,
                  'lat': None,
                  'lon': None,
                  'postal_code': None,
                  'region': None,
                  'store_number': None},
     'merchant_name': 'Transport for London',
     'name': '9114 18NOV22 CD TFL TRAVEL CH TFL.GOV.UK/CP GB',
     'payment_channel': 'online',
     'payment_meta': {'by_order_of': None,
                      'payee': None,
                      'payer': None,
                      'payment_method': None,
                      'payment_processor': None,
                      'ppd_id': None,
                      'reason': None,
                      'reference_number': None},
     'pending': False,
     'pending_transaction_id': None,
     'personal_finance_category': None,
     'transaction_code': 'purchase',
     'transaction_id': 'rkKAAqQRMeSMrrEj0PejH694dNqzKzCj3gvMOq',
     'transaction_type': 'place',
     'unofficial_currency_code': None}, {'account_id': 'a9X88M4oEpfBMMjVpOEVUp0m8ykRZ6f3n58M3a',
     'account_owner': None,
     'amount': -40.0,
     'authorized_date': datetime.date(2022, 11, 19),
     'authorized_datetime': None,
     'category': ['Shops', 'Supermarkets and Groceries'],
     'category_id': '19047000',
     'check_number': None,
     'date': datetime.date(2022, 11, 21),
     'datetime': datetime.datetime(2022, 11, 21, 0, 0, tzinfo=tzlocal()),
     'iso_currency_code': 'GBP',
     'location': {'address': None,
                  'city': None,
                  'country': None,
                  'lat': None,
                  'lon': None,
                  'postal_code': None,
                  'region': None,
                  'store_number': None},
     'merchant_name': None,
     'name': 'ANDREI AVETOV SERGEI MINAKOV FP 19/11/22 2125 P457SHRSL7HZKUA1EV',
     'payment_channel': 'other',
     'payment_meta': {'by_order_of': None,
                      'payee': None,
                      'payer': None,
                      'payment_method': None,
                      'payment_processor': None,
                      'ppd_id': None,
                      'reason': None,
                      'reference_number': None},
     'pending': False,
     'pending_transaction_id': None,
     'personal_finance_category': None,
     'transaction_code': None,
     'transaction_id': '5aexxV0NmKUBZZY8J4w8Uk0dXeOwEwHm0AqaEq',
     'transaction_type': 'place',
     'unofficial_currency_code': None}, {'account_id': 'a9X88M4oEpfBMMjVpOEVUp0m8ykRZ6f3n58M3a',
     'account_owner': None,
     'amount': 1.99,
     'authorized_date': datetime.date(2022, 11, 20),
     'authorized_datetime': None,
     'category': ['Food and Drink', 'Restaurants', 'Fast Food'],
     'category_id': '13005032',
     'check_number': None,
     'date': datetime.date(2022, 11, 21),
     'datetime': datetime.datetime(2022, 11, 21, 0, 0, tzinfo=tzlocal()),
     'iso_currency_code': 'GBP',
     'location': {'address': None,
                  'city': None,
                  'country': None,
                  'lat': None,
                  'lon': None,
                  'postal_code': None,
                  'region': None,
                  'store_number': None},
     'merchant_name': "McDonald's",
     'name': "McDonald's",
     'payment_channel': 'in store',
     'payment_meta': {'by_order_of': None,
                      'payee': None,
                      'payer': None,
                      'payment_method': None,
                      'payment_processor': None,
                      'ppd_id': None,
                      'reason': None,
                      'reference_number': None},
     'pending': False,
     'pending_transaction_id': None,
     'personal_finance_category': None,
     'transaction_code': 'purchase',
     'transaction_id': '0v5yyomk0PFL44oxNk9xt8Y3A0PwxwfBgjbz1P',
     'transaction_type': 'place',
     'unofficial_currency_code': None}])