import json
from django.test import TestCase, RequestFactory
from django.urls import reverse
from assetManager.tests.helpers import LogInTester
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from assetManager.models import User
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from rest_framework.exceptions import ErrorDetail
from assetManager.api.views import sector_spending, company_spending
from django.contrib.auth import get_user_model
from django.core.cache import cache
from assetManager.transactionInsight.bank_graph_data import BankGraphData

from assetManager.tests.helpers import LogInTester

class BarGraphViewTestCase(TestCase, LogInTester):
    """Tests of the views for transactions bar graph."""

    def setUp(self):
        self.factory = RequestFactory()
        User = get_user_model()
        users = User.objects.all()
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.org',
            'password': 'Password123',
            'password_confirmation':
            'Password123'
        }
        self.url = reverse('sign_up')
        self.client.post(self.url, self.form_input, follow=True)
        self.user = User.objects.get(email='janedoe@example.org')

    def tearDown(self):
        cache.clear()

    # tests for sector_spending graph view

    def test_sector_spending_graph_with_param(self):
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