from django.test import TestCase
from django.urls import reverse
from django.contrib import messages
from assetManager.models import User
import json
from assetManager.api.views import reformat_balances_into_currency,delete_balances_cache
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from django.conf import settings
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper

class GetCurrencyDataViewTestCase(TestCase):
    """Tests of the log in view."""
    fixtures = [
        'assetManager/tests/fixtures/users.json'
    ]

    def setUp(self):
        self.url = reverse('currency_data')
        self.user = User.objects.get(email='johndoe@example.org')
        self.client = APIClient()
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.post('/api/token/', {'email': self.user.email, 'password': 'Password123'}, format='json')
        jwt = str(response.data['access'])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ jwt)

    def test_balances_url(self):
        self.assertEqual(self.url,'/api/currency_data/')

    def test_get_balances_data_without_jwt_not_logged_in(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_reformat_balances_into_currency_incorrect_param_type(self):
        incorrect_account_balances = ['account1', 'account2']
        with self.assertRaises(TypeError) as cm:
            reformat_balances_into_currency(incorrect_account_balances)

    def test_get_reformatted_balances_into_currency_data_correctly_same_currency(self):
        account_balances = {'Royal Bank of Scotland - Current Accounts': {'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}}}
        balances = reformat_balances_into_currency(account_balances)
        self.assertEqual(len(balances),1)
        self.assertEqual(list(balances.keys())[0], 'USD')
        self.assertEqual(balances[list(balances.keys())[0]], 100)

    def test_get_currency_multiple_institutions(self):
        account_balances = {'Royal Bank of Scotland - Current Accounts': {'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}},'HSBC':{'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'EUR'}}}
        balances = reformat_balances_into_currency(account_balances)
        self.assertEqual(len(balances),2)
        self.assertEqual(list(balances.keys())[0], 'USD')
        self.assertEqual(list(balances.keys())[1], 'EUR')

        self.assertEqual(balances[list(balances.keys())[0]], 75)
        self.assertEqual(balances[list(balances.keys())[1]], 25)


    def test_get_reformatted_balances_into_currency_data_correctly_with_multiple_currencies_same_quantity_per_quantity(self):
        account_balances = {'Royal Bank of Scotland - Current Accounts': {'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'GBP'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZbP': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'GBP'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZLm': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczkaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'EUR'}, 'k1xZm8kW7jCnRqmkqGgrt96VaexNzGczkaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'GBP'}}}
        balances = reformat_balances_into_currency(account_balances)
        self.assertEqual(len(balances),3)
        self.assertEqual(list(balances.keys())[0], 'USD')
        self.assertEqual(list(balances.keys())[1], 'GBP')
        self.assertEqual(list(balances.keys())[2], 'EUR')

        self.assertEqual(balances[list(balances.keys())[0]], (1/3)*100)
        self.assertEqual(balances[list(balances.keys())[1]], 50)
        self.assertEqual(balances[list(balances.keys())[2]], (1/6)*100)

    def test_make_post_request_to_url(self):
        response = self.client.post(self.url, follow = True)
        self.assertEqual(response.status_code,405)

    def test_get_currenccy_succesfully_with_no_existing_cache(self):
        settings.PLAID_DEVELOPMENT = False
        response = self.client.get(self.url, follow=True)
        response_json = json.loads(response.content)
        response_data = response.json()
        self.assertEqual(list(response_data.keys())[0], "USD")
        self.assertEqual(response_data['USD'], 100)
        self.assertEqual(response.status_code,200)

    def test_get_currenccy_succesfully_with_existing_cache(self):
        settings.PLAID_DEVELOPMENT = False
        response = self.client.get(self.url, follow=True)
        response_2 = self.client.get(self.url, follow=True)
        response_json = json.loads(response_2.content)
        response_data = response.json()
        self.assertEqual(list(response_data.keys())[0], "USD")
        self.assertEqual(response_data['USD'], 100)
        self.assertEqual(response.status_code,200)
