from django.test import TestCase
from django.urls import reverse
from django.contrib import messages
from assetManager.models import User
import json
from assetManager.api.views import reformatBalancesData

from assetManager.api.views import get_balances_data

from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from django.conf import settings
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper

class GetBalancesDataViewTestCase(TestCase):
    """Tests of the log in view."""
    fixtures = [
        'assetManager/tests/fixtures/users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.org')
        self.client = APIClient()
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.post('/api/token/', {'email': self.user.email, 'password': 'Password123'}, format='json')
        jwt = str(response.data['access'])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ jwt)

        self.url = reverse('get_balances_data')


    def test_balances_url(self):
        self.assertEqual(self.url,'/api/get_balances_data/')

    def test_get_balances_data_without_jwt_not_logged_in(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_reformatBalancesData_incorrect_param_type(self):
        incorrect_account_balances = ['account1', 'account2']
        with self.assertRaises(TypeError) as cm:
            reformatBalancesData(incorrect_account_balances)

    def test_get_reformatted_balances_data_correctly(self):
        account_balances = {'Royal Bank of Scotland - Current Accounts': {'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}}}
        balances = reformatBalancesData(account_balances)
        self.assertEqual(len(balances),1)
        self.assertEqual(list(balances.keys())[0], 'Royal Bank of Scotland - Current Accounts')
        self.assertEqual(balances[list(balances.keys())[0]], 1000.0)


    def test_make_post_request_to_url(self):
        response = self.client.post(self.url, follow = True)
        self.assertEqual(response.status_code,405)


    def test_get_balances_succesfully(self):
        response = self.client.get(self.url, follow=True)
        response_json = json.loads(response.content)
        response_data = response.json()
        self.assertEqual(response_data['Royal Bank of Scotland - Current Accounts'], 1000.0)
        self.assertEqual(response.status_code,200)

    def test_get_balances_succesfully_for_multiple_accounts(self):
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token(bank_id='ins_1', products_chosen=['transactions'])
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(self.user, ['transactions'])
        settings.PLAID_DEVELOPMENT = False

        response = self.client.get(self.url, follow = True)
        self.assertEqual(response.status_code, 200)
        account_balances = json.loads(response.content)

        self.assertEqual(list(account_balances.keys())[0], 'Bank of America')
        self.assertEqual(list(account_balances.keys())[1], 'Royal Bank of Scotland - Current Accounts')

        self.assertEqual(account_balances[list(account_balances.keys())[0]], 43500.0)
        self.assertEqual(account_balances[list(account_balances.keys())[1]], 1000.0)
