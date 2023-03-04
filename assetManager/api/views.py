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
    return HttpResponse(json.dumps(categories, default=str), content_type='application/json')

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
    return HttpResponse(json.dumps(data), content_type='application/json')

def retrieve_stock_getter(user):
    stock_getter = StocksGetter(None)
    data = cache.get('investments' + user.email)
    stock_getter.investments = data
    return stock_getter
