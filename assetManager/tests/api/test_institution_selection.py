import json
from django.test import TestCase, RequestFactory
from django.urls import reverse
from assetManager.tests.helpers import LogInTester
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from assetManager.models import User
from django.test import TestCase, RequestFactory
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.exceptions import ErrorDetail
from assetManager.api.views import set_bank_access_token, select_bank_account
from assetManager.api.views_helpers import *
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.core.cache import cache
from assetManager.transactionInsight.bank_graph_data import BankGraphData

from assetManager.tests.helpers import LogInTester

class InstitutionSelectionViewTestCase(TestCase, LogInTester):
    """Tests of the views for institution selection."""
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

    def test_select_bank_account(self):
        self.create_public_token()
        request = self.factory.get('/select_bank_account/')
        force_authenticate(request, user=self.user)
        response = select_bank_account(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(response.data, [{'id': 0, 'name': 'Royal Bank of Scotland - Current Accounts'}])

    def test_select_bank_account_without_authentication(self):
        request = self.factory.get('/select_bank_account/')
        response = select_bank_account(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})

    def test_set_bank_access_token_with_correct_post_body(self):
        self.create_public_token()
        url = reverse('set_bank_access_token')
        client = APIClient()
        client.force_authenticate(user=self.user)
        data = {'selectedOption': '0'}
        response = client.post(url, json.dumps(data).encode('utf-8'), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        cache_key = 'access_token' + self.user.email
        cached_value = cache.get(cache_key)
        self.assertEqual(cached_value, 'Royal Bank of Scotland - Current Accounts')

    def test_set_bank_access_token_with_incorrect_post_body(self):
        url = reverse('set_bank_access_token')
        client = APIClient()
        client.force_authenticate(user=self.user)
        data = {'selectedOption': '100'}
        response = client.post(url, json.dumps(data).encode('utf-8'), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        cache_key = 'access_token' + self.user.email
        cached_value = cache.get(cache_key)
        self.assertEqual(cached_value, None)
        