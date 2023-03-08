import json

from django.test import TestCase
from django.core.cache import cache

from assetManager.models import User
from assetManager.tests.investments.test_stocks import _create_stock_getter_with_fake_data
from assetManager.api.views import *

from rest_framework.test import force_authenticate
from rest_framework.test import APIClient


class APIViewsTestCase(TestCase):
    fixtures = [
        'assetManager/tests/fixtures/users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.org')
        self.stock_getter = _create_stock_getter_with_fake_data()

        self.client = APIClient()
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.post('/api/token/', {'email': self.user.email, 'password': 'Password123'}, format='json')
        jwt = str(response.data['access'])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ jwt)

        cache.set('investmentsjohndoe@example.org', self.stock_getter.investments)

    def tearDown(self):
        cache.delete('investmentsjohndoe@example.org')

    def test_investment_categories_returns_categories(self):
        response = self.client.get('/api/investment_categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'equity': 200, 'etf': 152.3, 'derivative': 15, 'cash': 10000, 'mutual fund': 213})

    def test_investment_categories_returns_error_with_no_credentials(self):
        self.client.credentials()
        response = self.client.get('/api/investment_categories/')
        self.assertEqual(response.status_code, 401)

    #TODO: figure out 301 response 
    #NOTE: need OPTIONS preflight request??
    # def test_investment_category_breakdown_returns_breakdown(self):
    #     #self.client.get('/api/investment_category_breakdown?param=etf')
    #     response = self.client.options('/api/investment_category_breakdown?param=etf')
    #     #response = self.client.get('/api/investment_category_breakdown?param=etf')
    #     print(response)
    #     print(response.data)
    #     self.assertEqual(response.status_code, 200)
