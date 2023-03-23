import json
import re

from django.test import TestCase
from django.core.cache import cache
from django.conf import settings

from assetManager.models import User
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.investments.stocks import InvestmentsNotLinked
from assetManager.tests.investments.test_stocks import _create_stock_getter_with_fake_data
from assetManager.api.views import *
from assetManager.api.views import reformat_balances_into_currency
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from assetManager.tests.bankcard_asset.single_transaction import single_transaction_dict

class APIViewsTestCase(TestCase):
    fixtures = [
        'assetManager/tests/fixtures/users.json',
    ]

    def setUp(self):
        settings.PLAID_DEVELOPMENT = False
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
        cache.delete('balancesjohndoe@example.org')
        cache.delete('transactionsjohndoe@example.org')
        cache.delete('currencyjohndoe@example.org')


    def test_investment_categories_returns_categories(self):
        response = self.client.get('/api/investment_categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'equity': 200, 'etf': 152.3, 'derivative': 15, 'cash': 10000, 'mutual fund': 213})

    def test_investment_categories_returns_unauthorized_with_no_credentials(self):
        self.client.credentials()
        response = self.client.get('/api/investment_categories/')
        self.assertEqual(response.status_code, 401)

    def test_investment_categories_returns_see_other_with_no_investments_linked(self):
        client = APIClient()
        user = User.objects.get(email='lillydoe@example.org')
        client.login(email=user.email, password='Password123')
        response = client.post('/api/token/', {'email': user.email, 'password': 'Password123'}, format='json')
        jwt = str(response.data['access'])
        client.credentials(HTTP_AUTHORIZATION='Bearer '+ jwt)
        response = client.get('/api/investment_categories/')
        self.assertEqual(response.status_code, 303)

    def test_investment_category_breakdown_returns_breakdown(self):
        response = self.client.get('/api/investment_category_breakdown/?param=equity')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'Achillion Pharmaceuticals Inc.': 100.0, 'Southside Bancshares Inc.': 100.0})

    def test_investment_category_breakdown_returns_see_other_with_no_investments_linked(self):
        client = APIClient()
        user = User.objects.get(email='lillydoe@example.org')
        client.login(email=user.email, password='Password123')
        response = client.post('/api/token/', {'email': user.email, 'password': 'Password123'}, format='json')
        jwt = str(response.data['access'])
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt)
        response = client.get('/api/investment_category_breakdown/?param=equity')
        self.assertEqual(response.status_code, 303)

    def test_investment_category_breakdown_returns_bad_request_with_no_params(self):
        response = self.client.get('/api/investment_category_breakdown/')
        self.assertEqual(response.status_code, 400)

    def test_cache_assets_returns_method_not_allowed_wrong_request(self):
        response = self.client.get('/api/cache_assets/')
        self.assertEqual(response.status_code, 405)

    def test_cache_assets_returns_unauthorized_without_jwt(self):
        self.client.credentials()
        response = self.client.get('/api/cache_assets/')
        self.assertEqual(response.status_code, 401)

    def test_put_cache_assets_returns_see_other_with_no_linked_investments(self):
        client = APIClient()
        user = User.objects.get(email='lillydoe@example.org')
        client.login(email=user.email, password='Password123')
        response = client.post('/api/token/', {'email': user.email, 'password': 'Password123'}, format='json')
        jwt = str(response.data['access'])
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt)
        response = client.put('/api/cache_assets/')
        self.assertEqual(response.status_code, 303)

    def test_put_cache_assets_returns_see_other_with_no_linked_transactions(self):
        client = APIClient()
        user = User.objects.get(email='lillydoe@example.org')

        wrapper = SandboxWrapper()
        public_token = wrapper.create_public_token(bank_id='ins_115616', products_chosen=['investments'])
        wrapper.exchange_public_token(public_token)
        wrapper.save_access_token(user, ['investments'])

        client.login(email=user.email, password='Password123')
        response = client.post('/api/token/', {'email': user.email, 'password': 'Password123'}, format='json')
        jwt = str(response.data['access'])
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt)
        response = client.put('/api/cache_assets/')
        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.content.decode('utf-8'), '{"error":"Transactions Not Linked."}')

    def test_put_cache_assets_works(self):
        #cache.delete('investments' + self.user.email)
        # setup investments

        self.assertFalse(cache.has_key('transactions' + self.user.email))
        self.assertFalse(cache.has_key('balances' + self.user.email))
        self.assertFalse(cache.has_key('investments' + self.user.email))
        self.assertFalse(cache.has_key('currency' + self.user.email))


        wrapper = SandboxWrapper()
        public_token = wrapper.create_public_token(bank_id='ins_115616', products_chosen=['investments','transactions'])
        wrapper.exchange_public_token(public_token)
        wrapper.save_access_token(self.user, ['investments','transactions'])
        response = self.client.put('/api/cache_assets/')
        self.assertEqual(response.status_code, 200)

        stock_getter = StocksGetter(wrapper)
        stock_getter.query_investments(self.user)
        investments = stock_getter.investments
        cached_investments = cache.get('investments' + self.user.email)
        self.assertEqual(len(investments), len(cached_investments))

        balances = cache.get('balances' + self.user.email)
        self.assertEqual(list(balances.keys())[0], 'Vanguard')

        for all_accounts in balances['Vanguard']:
            self.assertTrue('name' in balances['Vanguard'][all_accounts])
            self.assertTrue('available_amount' in balances['Vanguard'][all_accounts])
            self.assertTrue('current_amount' in balances['Vanguard'][all_accounts])
            self.assertTrue('type' in balances['Vanguard'][all_accounts])
            self.assertTrue('currency' in balances['Vanguard'][all_accounts])

        currency = cache.get('currency' + self.user.email)
        


    #extend this
    def test_delete_cache_assets_works(self):
        account_balances = {'Royal Bank of Scotland - Current Accounts': {'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}}}
        cache.set('balances' + self.user.email,account_balances)
        balances = reformat_balances_into_currency(account_balances)
        cache.set('currency' + self.user.email,balances)
        reformatted_transactions = BankGraphData(single_transaction_dict)
        cache.set('transactions' + self.user.email,reformatted_transactions.transactionInsight.transaction_history)

        self.assertTrue(cache.has_key('investments' + self.user.email))
        self.assertTrue(cache.has_key('balances' + self.user.email))
        self.assertTrue(cache.has_key('currency' + self.user.email))
        self.assertTrue(cache.has_key('transactions' + self.user.email))

        response = self.client.delete('/api/cache_assets/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(cache.has_key('investments' + self.user.email))
        self.assertFalse(cache.has_key('balances' + self.user.email))
        self.assertFalse(cache.has_key('currency' + self.user.email))
        self.assertFalse(cache.has_key('transactions' + self.user.email))

    def test_delete_cache_assets_works_for_some_loaded_keys(self):
        account_balances = {'Royal Bank of Scotland - Current Accounts': {'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}}}
        cache.set('balances' + self.user.email,account_balances)

        self.assertTrue(cache.has_key('investments' + self.user.email))
        self.assertTrue(cache.has_key('balances' + self.user.email))

        response = self.client.delete('/api/cache_assets/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(cache.has_key('investments' + self.user.email))
        self.assertFalse(cache.has_key('balances' + self.user.email))


    def test_cache_assets_works_with_development(self):
        settings.PLAID_DEVELOPMENT = True
        response = self.client.delete('/api/cache_assets/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(cache.has_key('investments' + self.user.email))
        settings.PLAID_DEVELOPMENT = False

    def test_get_stock_history_work(self):
        response = self.client.get('/api/stock_history/?param=iShares%20Inc%20MSCI%20Brazil')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 10)

    def test_stock_history_returns_see_other_with_no_investments_linked(self):
        cache.clear()
        client = APIClient()
        user = User.objects.get(email='lillydoe@example.org')
        client.login(email=user.email, password='Password123')
        response = client.post('/api/token/', {'email': user.email, 'password': 'Password123'}, format='json')
        jwt = str(response.data['access'])
        client.credentials(HTTP_AUTHORIZATION='Bearer '+ jwt)
        response = client.get('/api/investment_category_breakdown/?param=NFLX')
        self.assertEqual(response.status_code, 303)

    def test_get_stock_history_returns_bad_request_without_param(self):
        response = self.client.get('/api/stock_history/')
        self.assertEqual(response.status_code, 400)

    def test_get_link_token_returns_error_for_wrong_product(self):
        response = self.client.get('/api/link_token/?product=thisdoesntexit')
        self.assertEqual(response.status_code, 400)

    def test_get_link_token_works(self):
        response = self.client.get('/api/link_token/?product=investments')
        self.assertEqual(response.status_code, 200)
        link_token = response.data['link_token']
        self.assertIsNotNone(re.match(r"^link-development-[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$", link_token))

    def test_get_link_token_returns_error_with_no_product_param(self):
        response = self.client.get('/api/link_token/')
        self.assertEqual(response.status_code, 400)

    def test_post_exchange_public_token_returns_error_for_bad_public_token(self):
        cache.set('product_link' + self.user.email, 'transactions')
        response = self.client.post('/api/exchange_public_token/', {'public_token': 'notapublictoken'}, format='json')
        self.assertEqual(response.status_code, 400)
        cache.delete('product_link' + self.user.email)

    def test_post_exchange_public_token_returns_error_code_with_no_public_token(self):
        cache.set('product_link' + self.user.email, 'transactions')
        response = self.client.post('/api/exchange_public_token/')
        self.assertEqual(response.status_code, 400)
        cache.delete('product_link' + self.user.email)

    def test_retrieve_stock_getter_works(self):
        stock_getter = retrieve_stock_getter(self.user)
        self.assertEqual(len(self.stock_getter.investments), len(stock_getter.investments))

    def test_retrieve_stock_getter_raises_error_without_cached_investments_and_without_linked_investments(self):
        cache.delete('investments' + self.user.email)
        with self.assertRaises(InvestmentsNotLinked):
            retrieve_stock_getter(self.user)

    def test_retrieve_stock_getter_works_without_cached_investments_with_linked_investments(self):
        cache.delete('investments' + self.user.email)
        wrapper = SandboxWrapper()
        public_token = wrapper.create_public_token(bank_id='ins_115616', products_chosen=['investments'])
        wrapper.exchange_public_token(public_token)
        wrapper.save_access_token(self.user, ['investments'])

        stock_getter = retrieve_stock_getter(self.user)
        self.assertTrue(len(stock_getter.investments) > 0)
        self.assertTrue(cache.has_key('investments' + self.user.email))
        self.assertEqual(len(stock_getter.investments), len(cache.get('investments'+self.user.email)))

    def test_retrieve_stock_getter_works_with_development_wrapper(self):
        settings.PLAID_DEVELOPMENT = True
        cache.delete('investments' + self.user.email)
        with self.assertRaises(InvestmentsNotLinked):
            retrieve_stock_getter(self.user)
        settings.PLAID_DEVELOPMENT = False
