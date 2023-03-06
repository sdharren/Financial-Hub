from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from assetManager.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer
from assetManager.models import User

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

# the following imports are needed for the below view - leaving them here for now
from assetManager.investments.stocks import StocksGetter
from django.core.cache import cache
from django.http import HttpResponse
import json

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
        raise Exception
        # should return bad request
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

from django.conf import settings
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.API_wrappers.plaid_wrapper import InvalidPublicToken
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
    products_selected = ['transactions'] # for now this is here uncomment for prod!!!
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

# handle error if investments aren't cached
def retrieve_stock_getter(user):
    stock_getter = StocksGetter(None)
    data = cache.get('investments' + user.email)
    stock_getter.investments = data
    return stock_getter
