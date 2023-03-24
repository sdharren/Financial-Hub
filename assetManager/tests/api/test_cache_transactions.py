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

class CacheTransactionsViewTestCase(TestCase, LogInTester):
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

    def test_cache_bank_transaction_data_already_cached(self):
        correct_data = {"test_transactions_name":"test_transactions_data"}
        cache.set('transactions'+self.user.email,{"test_institution":[correct_data]})
        cacheBankTransactionData(self.user)
        self.assertEqual(cache.get('transactions'+self.user.email),{"test_institution":[correct_data]})

    def test_cache_bank_transaction_data_not_already_cached(self):
        cacheBankTransactionData(self.user)
        self.assertNotEqual(cache.get('transactions'+self.user.email),None)

    def test_get_cached_data_gets_cached_data(self):
        correct_data = [{"test_transactions_name":"test_transactions_data"}]
        cache.set('transactions'+self.user.email,{"test_institution":correct_data})
        cached_data = getCachedInstitutionData(self.user,"test_institution")
        self.assertEqual(cached_data,correct_data)

    def test_get_no_cached_data(self):
        cached_data = getCachedInstitutionData(self.user,"test_institution")
        self.assertEqual(cached_data,None)

    def test_when_institution_name_and_transaction_data_are_both_cached(self):
        cache.set('access_token'+self.user.email, 'Chase')
        cache.set('transactions'+self.user.email, {'Chase': [{'date': '2022-01-01', 'amount': 100}, {'date': '2022-01-02', 'amount': 200}]})
        result = getCachedInstitutionCachedData(self.user)
        assert result == [{'date': '2022-01-01', 'amount': 100}, {'date': '2022-01-02', 'amount': 200}]

    def test_when_only_institution_name_is_cached(self):
        cache.set('access_token'+self.user.email, 'Chase')
        cache.delete('transactions'+self.user.email)
        result = getCachedInstitutionCachedData(self.user)
        self.assertEqual(result,None)

    def test_both_institution_name_and_transaction_data_are_not_cached(self):
        cache.delete('access_token'+self.user.email)
        cache.delete('transactions'+self.user.email)
        result = getCachedInstitutionCachedData(self.user)
        self.assertNotEqual(result,None)

    def test_transaction_data_getter(self):
        self.assertNotEqual(transaction_data_getter(self.user),None)
    
    def test_recache_transaction_data(self):
        oldCachedData = {"test_transactions_name":"test_transactions_data"}
        correct_data = {"test_institution":[oldCachedData]}
        cache.set('transactions'+self.user.email,correct_data)
        recacheTransactionData(self.user)
        newCachedData = cache.get('transactions'+self.user.email)
        self.assertNotEqual(correct_data, newCachedData)
        self.assertNotEqual(newCachedData,None)