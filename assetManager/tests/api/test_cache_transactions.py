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
from assetManager.api.views import yearlyGraph, monthlyGraph, weeklyGraph, transaction_data_getter
from assetManager.api.views_helpers import *
from django.contrib.auth import get_user_model
from django.core.cache import cache
from assetManager.transactionInsight.bank_graph_data import BankGraphData
from django.conf import settings

from assetManager.tests.helpers import LogInTester

class CacheTransactionsViewTestCase(TestCase, LogInTester):
    fixtures = [
        'assetManager/tests/fixtures/users.json',
    ]
    """Tests of the views for transactions bar graph."""
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

    def test_cache_bank_transaction_data_already_cached(self):
        correct_data = {"test_transactions_name":"test_transactions_data"}
        cache.set('transactions'+self.user.email,{"test_institution":[correct_data]})
        cacheBankTransactionData(self.user)
        self.assertEqual(cache.get('transactions'+self.user.email),{"test_institution":[correct_data]})

    def test_cache_bank_transaction_data_not_already_cached(self):
        self.create_public_token()
        cacheBankTransactionData(self.user)
        self.assertNotEqual(cache.get('transactions'+self.user.email),None)

    def test_get_cached_data_gets_cached_data(self):
        correct_data = [{"test_transactions_name":"test_transactions_data"}]
        cache.set('transactions'+self.user.email,{"test_institution":correct_data})
        cached_data = getCachedInstitutionData(self.user,"test_institution")
        self.assertEqual(cached_data,correct_data)

    def test_get_no_cached_data(self):
        self.create_public_token()
        cached_data = getCachedInstitutionData(self.user,"test_institution")
        self.assertEqual(cached_data,None)

    def test_when_institution_name_and_transaction_data_are_both_cached(self):
        cache.set('access_token'+self.user.email, 'Chase')
        cache.set('transactions'+self.user.email, {'Chase': [{'date': '2022-01-01', 'amount': 100}, {'date': '2022-01-02', 'amount': 200}]})
        result = getCachedInstitutionCachedData(self.user)
        assert result == [{'date': '2022-01-01', 'amount': 100}, {'date': '2022-01-02', 'amount': 200}]

    def test_when_only_institution_name_is_cached(self):
        self.create_public_token()
        cache.set('access_token'+self.user.email, 'Chase')
        cache.delete('transactions'+self.user.email)
        result = getCachedInstitutionCachedData(self.user)
        self.assertEqual(result,None)

    def test_both_institution_name_and_transaction_data_are_not_cached(self):
        self.create_public_token()
        cache.delete('access_token'+self.user.email)
        cache.delete('transactions'+self.user.email)
        result = getCachedInstitutionCachedData(self.user)
        self.assertNotEqual(result,None)

    def test_transaction_data_getter(self):
        self.create_public_token()
        self.assertNotEqual(transaction_data_getter(self.user),None)

    def test_recache_transaction_data(self):
        self.create_public_token()
        oldCachedData = {"test_transactions_name":"test_transactions_data"}
        correct_data = {"test_institution":[oldCachedData]}
        cache.set('transactions'+self.user.email,correct_data)
        recacheTransactionData(self.user)
        newCachedData = cache.get('transactions'+self.user.email)
        self.assertNotEqual(correct_data, newCachedData)
        self.assertNotEqual(newCachedData,None)
