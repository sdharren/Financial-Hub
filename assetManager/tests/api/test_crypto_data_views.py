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
from assetManager.api.views import crypto_all_data, crypto_select_data
from assetManager.api.views_helpers import *
from django.core.cache import cache
from assetManager.transactionInsight.bank_graph_data import BankGraphData
from django.conf import settings
from assetManager.API_wrappers.crypto_wrapper import save_wallet_address

from assetManager.tests.helpers import LogInTester


class CryptoDataViewsTestCase(TestCase, LogInTester):
    fixtures = [
        'assetManager/tests/fixtures/users.json',
    ]

    """Tests of the views for transactions bar graph."""
    def create_public_token(self):
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token()
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(self.user, ['transactions'])

    fixtures = [
        'assetManager/tests/fixtures/users.json'
    ]

    def setUp(self):
        settings.PLAID_DEVELOPMENT = False
        self.factory = RequestFactory()
        self.user = User.objects.get(email='johndoe@example.org')

    def tearDown(self):
        cache.clear()

    def generate_then_cache_crypto(self):
        save_wallet_address(self.user, "34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo")
        request = self.factory.get('')
        force_authenticate(request, user=self.user)
        crypto_data = crypto_all_data(request).data
        cache.set('crypto'+self.user.email,crypto_data)

    def test_crypto_all_data_with_cached_data(self):
        self.create_public_token()
        self.generate_then_cache_crypto()
        request = self.factory.get('/dashboard')
        force_authenticate(request, user=self.user)
        response = crypto_all_data(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(cache.get('crypto'+self.user.email),response.data)

    def test_crypto_all_data_without_cached_data(self):
        save_wallet_address(self.user, "34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo")
        request = self.factory.get('/dashboard')
        force_authenticate(request, user=self.user)
        response = crypto_all_data(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(cache.get('crypto'+self.user.email),response.data)

    def test_crypto_all_data_redirects_with_no_crypto_linked(self):
        request = self.factory.get('/crypto_all_data')
        force_authenticate(request, user=self.user)
        response = crypto_all_data(request)
        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.data,{'error': 'Crypto not linked.'})

    def test_crypto_select_data_with_cached_data(self):
        self.create_public_token()
        self.generate_then_cache_crypto()
        request = self.factory.get('/dashboard?param="address"')
        force_authenticate(request, user=self.user)
        response = crypto_select_data(request)
        self.assertEqual(response.data,cache.get('crypto'+self.user.email))

    def test_crypto_select_data_without_cached_data(self):
        save_wallet_address(self.user, "34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo")
        self.create_public_token()
        request = self.factory.get('/dashboard?param="address"')
        force_authenticate(request, user=self.user)
        response = crypto_select_data(request)
        self.assertEqual(response.data,cache.get('crypto'+self.user.email))

    def test_crypto_select_data_with_incorrect_param(self):
        self.create_public_token()
        request = self.factory.get('/dashboard/')
        force_authenticate(request, user=self.user)
        with self.assertRaises(Exception) as e:
            crypto_select_data(request)
