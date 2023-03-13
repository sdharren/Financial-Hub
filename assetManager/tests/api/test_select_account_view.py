from django.test import TestCase
from django.urls import reverse
from django.contrib import messages
from assetManager.models import User
import json
from assetManager.api.views import reformatAccountBalancesData
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from django.conf import settings
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper



class SelectAccountViewsTestCase(TestCase):
    """Tests of the log in view."""
    fixtures = [
        'assetManager/tests/fixtures/users.json'
    ]

    def setUp(self):
        self.url = reverse('select_account')
        self.user = User.objects.get(email='johndoe@example.org')
        self.client = APIClient()
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.post('/api/token/', {'email': self.user.email, 'password': 'Password123'}, format='json')
        jwt = str(response.data['access'])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ jwt)


    def test_balances_url(self):
        self.assertEqual(self.url,'/api/select_account/')

    def test_reformatAccountBalancesData_incorrect_param_type(self):
        incorrect_account_balances = ['account1', 'account2']
        institution_name = 'HSBC - UK'
        with self.assertRaises(TypeError) as cm:
            reformatAccountBalancesData(incorrect_account_balances,institution_name)

    def test_reformatAccountBalancesData_incorrect_institution_name_param(self):
        account_balances = {'Royal Bank of Scotland - Current Accounts': {'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}}}
        incorrectinstitution_name = 'HSBC - UK'
        with self.assertRaises(Exception) as cm:
            reformatAccountBalancesData(account_balances,incorrectinstitution_name)

        self.assertEqual(str(cm.exception),'passed institution_name is not account balances dictionary')

    def test_get_reformatted_account_balances_data_correctly(self):
        account_balances = {'Royal Bank of Scotland - Current Accounts': {'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}}}
        institution_name = 'Royal Bank of Scotland - Current Accounts'
        balances = reformatAccountBalancesData(account_balances,institution_name)
        self.assertEqual(len(balances),2)

        self.assertTrue(list(balances.keys())[0] == 'Checking')
        self.assertTrue(list(balances.keys())[1] == 'Savings')

        self.assertEqual(balances[list(balances.keys())[0]], 500.0)
        self.assertEqual(balances[list(balances.keys())[1]], 500.0)

    def test_make_post_request_to_select_account_url(self):
        response = self.client.post(self.url, follow = True)
        self.assertEqual(response.status_code,405)

    def test_get_select_account_url_without_being_logged_in(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get_select_account_url_succesfully(self):
        self.balances = self.client.get(reverse('get_balances_data'), follow=True)
        response = self.client.get(self.url,{'param':'Royal Bank of Scotland - Current Accounts'}, follow=True)
        response_json = json.loads(response.content)
        response_data = response.json()

        self.assertEqual(len(list(response_data.keys())),2)
        self.assertTrue(list(response_data.keys())[0] == 'Savings' or list(response_data.keys())[0] == 'Checking')
        self.assertTrue(list(response_data.keys())[1] == 'Savings' or list(response_data.keys())[1] == 'Checking')

        self.assertEqual(response_data[list(response_data.keys())[0]], 500.0)
        self.assertEqual(response_data[list(response_data.keys())[1]], 500.0)


    def test_get_select_account_url_without_giving_param_field_a_value(self):
        with self.assertRaises(Exception) as cm:
            response = self.client.get(self.url,{'param':''}, follow=True)

        self.assertEqual(str(cm.exception),'No param field supplied to select_account url')

    def test_get_select_accounts_url_with_incorrect_key(self):
        with self.assertRaises(Exception) as cm:
            response = self.client.get(self.url,{'param':'HSBC (UK)'}, follow=True)

        self.assertEqual(str(cm.exception),'Provided institution name does not exist in the requested accounts')
