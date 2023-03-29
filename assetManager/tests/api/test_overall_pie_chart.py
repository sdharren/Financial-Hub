import json
from django.test import TestCase, RequestFactory
from django.urls import reverse
from assetManager.tests.helpers import LogInTester
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from assetManager.models import User
from django.test import TestCase, RequestFactory
from rest_framework.test import force_authenticate
from rest_framework.exceptions import ErrorDetail
from assetManager.api.views import total_assets
from assetManager.api.views_helpers import *
from django.contrib.auth import get_user_model
from django.core.cache import cache
from assetManager.transactionInsight.bank_graph_data import BankGraphData
from assetManager.API_wrappers.crypto_wrapper import save_wallet_address
from django.core.cache import cache


from assetManager.tests.helpers import LogInTester

class OverallGraphViewTestCase(TestCase, LogInTester):
    """Tests of the views for overall assets pie graph."""
    fixtures = [
        'assetManager/tests/fixtures/users.json',
    ]

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.get(email='johndoe@example.org')

    def tearDown(self):
        cache.clear()

    def create_public_token(self):
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token()
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(self.user, ['transactions'])

    def test_overall_graph_when_logged_in(self):
        self.create_public_token()
        request = self.factory.get('/dashboard')
        force_authenticate(request, user=self.user)
        response = total_assets(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(response.data,{'Bank Assets': 43500.0, 'Investment Assets': 0, 'Crypto Assets': 0.0})

    def test_overall_graph_when_data_is_cached(self):
        cache.set('total_assets'+self.user.email,{'Bank Assets': 100.0, 'Investment Assets': 1000.0, 'Crypto Assets': 100})
        request = self.factory.get('/dashboard')
        force_authenticate(request, user=self.user)
        response = total_assets(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(response.data,{'Bank Assets': 100.0, 'Investment Assets': 1000.0, 'Crypto Assets': 100})

    def test_overall_graph_when_not_logged_in(self):
        request = self.factory.get('/dashboard')
        response = total_assets(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(response.data,{'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})

    def test_sum_instiution_balances(self):
        self.create_public_token()
        wrapper = get_plaid_wrapper(self.user,'balances')
        balance = sum_instiution_balances(wrapper,self.user)
        self.assertEqual(balance,43500.0)

    def test_sum_investment_balance(self):
        balance = sum_investment_balance(self.user)
        self.assertEqual(balance,0)

    def test_sum_crypto_balances_with_no_wallet(self):
        balance = sum_crypto_balances(self.user)
        self.assertEqual(balance,0)

    def test_sum_crypto_balances_with_wallet(self):
        save_wallet_address(self.user, "34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo")
        balance = sum_crypto_balances(self.user)
        self.assertNotEqual(balance,None)
