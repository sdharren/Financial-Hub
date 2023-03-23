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
from assetManager.api.views import yearlyGraph, monthlyGraph, weeklyGraph, transaction_data_getter
from assetManager.api.views_helpers import *
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

    # tests for yearly graph view

    def test_yearly_graph_with_param(self):
        request = self.factory.get('/yearly-graph/?param=2022')
        force_authenticate(request, user=self.user)
        response = yearlyGraph(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_yearly_graph_without_authentication(self):
        request = self.factory.get('yearly-graph/?param=2022')
        response = yearlyGraph(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data['detail'],
            ErrorDetail('Authentication credentials were not provided.', code='not_authenticated')
        )

    # tests for monthly graph view

    def test_monthly_graph_with_param(self):
        request = self.factory.get('/monthly-graph/?param=2022')
        force_authenticate(request, user=self.user)
        response = monthlyGraph(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_monthly_graph_without_param(self):
        request = self.factory.get('/monthly-graph/')
        force_authenticate(request, user=self.user)
        with self.assertRaises(Exception):
            monthlyGraph(request)

    def test_monthly_graph_without_authentication(self):
        request = self.factory.get('/monthly-graph/?param=2022')
        response = monthlyGraph(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data['detail'],
            ErrorDetail('Authentication credentials were not provided.', code='not_authenticated')
        )

    # tests for weekly graph view

    def test_weekly_graph_with_param(self):
        request = self.factory.get('/weekly-graph/?param=May+2022')
        force_authenticate(request, user=self.user)
        response = weeklyGraph(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_weekly_graph_without_param(self):
        request = self.factory.get('/weekly-graph/')
        force_authenticate(request, user=self.user)
        with self.assertRaises(Exception):
            weeklyGraph(request)

    def test_weekly_graph_without_authentication(self):
        request = self.factory.get('/weekly-graph/?param=2022')
        response = weeklyGraph(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data['detail'],
            ErrorDetail('Authentication credentials were not provided.', code='not_authenticated')
        )

    # tests for cache bank transaction data view

    def test_cache_bank_transaction_data(self):
        bankgraphdata = BankGraphData(getCachedInstitutionCachedData(self.user))
        cache.set('transactions' + self.user.email, bankgraphdata.transactionInsight.transaction_history)
        cached_data = cache.get('transactions' + self.user.email)
        correct_data = bankgraphdata.transactionInsight.transaction_history
        self.assertNotEqual(correct_data,"")
        self.assertNotEqual(cached_data,"")
        self.assertNotEqual(correct_data,None)
        self.assertNotEqual(cached_data,None)
        self.assertEqual(correct_data,cached_data)
        self.assertIsInstance(cached_data, list)
        all(self.assertIsInstance(transaction, dict) for transaction in cached_data)

    # test for transaction data getter view

    def test_transaction_data_getter(self):
        json_data = transaction_data_getter(self.user)
        self.assertNotEqual(json_data,"")
        self.assertIsInstance(json_data, dict)
        all(self.assertIsInstance(transaction, str) for transaction in json_data)
