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
from assetManager.API_wrappers.plaid_wrapper import InvalidPublicToken, LinkTokenNotCreated
from assetManager.investments.stocks import StocksGetter, InvestmentsNotLinked


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
        #return bad request
    data = stock_getter.get_stock_history(stock_ticker)
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