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
from assetManager.api.views import sector_spending, company_spending
from django.contrib.auth import get_user_model
from django.core.cache import cache
from assetManager.transactionInsight.bank_graph_data import BankGraphData
from django.conf import settings
from assetManager.tests.helpers import LogInTester
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper

class BarGraphViewTestCase(TestCase, LogInTester):
    """Tests of the views for transactions bar graph."""
    fixtures = [
        'assetManager/tests/fixtures/users.json',
    ]

    def create_public_token(self):
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token()
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(self.user, ['transactions'])

    def setUp(self):
        settings.PLAID_DEVELOPMENT = False
        self.factory = RequestFactory()
        self.user = User.objects.get(email='johndoe@example.org')

    def tearDown(self):
        cache.clear()

    # tests for sector_spending graph view

    def test_sector_spending_graph_with_param(self):
        self.create_public_token()
        request = self.factory.get('/sector_spending/')
        force_authenticate(request, user=self.user)
        response = sector_spending(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_sector_spending_graph_without_authentication(self):
        request = self.factory.get('/sector_spending/')
        response = sector_spending(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data['detail'],
            ErrorDetail('Authentication credentials were not provided.', code='not_authenticated')
        )

    # tests for company_spending graph view

    def test_company_spending_graph_with_param(self):
        self.create_public_token()
        request = self.factory.get('/company_spending/?param=Transport')
        force_authenticate(request, user=self.user)
        response = company_spending(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_company_spending_graph_without_authentication(self):
        request = self.factory.get('/company_spending/?param=Transport')
        response = company_spending(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data['detail'],
            ErrorDetail('Authentication credentials were not provided.', code='not_authenticated')
        )

    def test_company_spending_graph_without_param(self):
        request = self.factory.get('/company_spending-graph/')
        force_authenticate(request, user=self.user)
        with self.assertRaises(Exception):
            company_spending(request)
