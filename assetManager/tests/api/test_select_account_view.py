from django.test import TestCase
from django.urls import reverse
from django.contrib import messages
from assetManager.models import User
import json
from assetManager.api.views import reformatAccountBalancesData
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from django.conf import settings
from assetManager.models import AccountTypeEnum,AccountType
from django.core.cache import cache

class SelectAccountViewsTestCase(TestCase):
    """Tests for the select_account view."""
    fixtures = [
        'assetManager/tests/fixtures/users.json'
    ]

    def create_public_token(self):
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token_custom_user()
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(self.user, ['transactions'])

    def tearDown(self):
        cache.clear()

    def setUp(self):
        settings.PLAID_DEVELOPMENT = False
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

        self.assertEqual(balances[list(balances.keys())[0]], 296.9)
        self.assertEqual(balances[list(balances.keys())[1]], 296.9)

    def test_make_post_request_to_select_account_url(self):
        response = self.client.post(self.url, follow = True)
        self.assertEqual(response.status_code,405)

    def test_get_select_account_url_without_being_logged_in(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get_select_account_url_succesfully_for_single_institution(self):
        self.create_public_token()
        self.balances = self.client.get(reverse('get_balances_data'), follow=True)
        response = self.client.get('/api/select_account/?param=Royal Bank of Scotland - Current Accounts')

        response_data = response.json()

        self.assertEqual(len(list(response_data.keys())),2)
        self.assertTrue(list(response_data.keys())[0] == 'Savings' or list(response_data.keys())[0] == 'Checking')
        self.assertTrue(list(response_data.keys())[1] == 'Savings' or list(response_data.keys())[1] == 'Checking')

        self.assertEqual(response_data[list(response_data.keys())[0]], 296.9)
        self.assertEqual(response_data[list(response_data.keys())[1]], 296.9)

    def test_get_select_account_url_for_multiple_institutions(self):
        before_count = len(AccountType.objects.filter(user = self.user, account_asset_type = AccountTypeEnum.DEBIT))
        self.create_public_token()
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token(bank_id='ins_1', products_chosen=['transactions'])
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(self.user, ['transactions'])


        self.client.get(reverse('get_balances_data'), follow=True)
        after_count = len(AccountType.objects.filter(user = self.user, account_asset_type = AccountTypeEnum.DEBIT))
        self.assertEqual(before_count + 2, after_count)

        response = self.client.get('/api/select_account/?param=Royal Bank of Scotland - Current Accounts')
        self.assertEqual(response.status_code, 200)
        response_data_first = response.json()
        self.assertEqual(len(list(response_data_first.keys())),2)
        self.assertTrue(list(response_data_first.keys())[0] == 'Savings' or list(response_data_first.keys())[0] == 'Checking')
        self.assertTrue(list(response_data_first.keys())[1] == 'Savings' or list(response_data_first.keys())[1] == 'Checking')

        self.assertEqual(response_data_first[list(response_data_first.keys())[0]], 296.9)
        self.assertEqual(response_data_first[list(response_data_first.keys())[1]], 296.9)

        response_second = self.client.get('/api/select_account/?param=Bank of America')
        self.assertEqual(response_second.status_code, 200)
        response_data_second = response_second.json()
        self.assertEqual(len(list(response_data_second.keys())),9)
        self.assertEqual(list(response_data_second.keys())[0] , 'Plaid Checking')
        self.assertEqual(list(response_data_second.keys())[1] , 'Plaid Saving')
        self.assertEqual(list(response_data_second.keys())[4] , 'Plaid Money Market')

        self.assertEqual(response_data_second[list(response_data_second.keys())[0]],59.38)
        self.assertEqual(response_data_second[list(response_data_second.keys())[1]],118.76)
        self.assertEqual(response_data_second[list(response_data_second.keys())[4]],25652.18)


    def test_get_select_account_url_without_giving_param_field_a_value(self):
        response = self.client.get('/api/select_account/?param=')
        self.assertEqual(response.status_code, 303)

        response_data = response.json()
        self.assertEqual(list(response_data.keys())[0],'error')
        self.assertEqual(response_data[list(response_data.keys())[0]],'No param field supplied.')


    def test_get_select_accounts_url_with_incorrect_key(self):
        self.create_public_token()
        self.balances = self.client.get(reverse('get_balances_data'), follow=True)
        response = self.client.get('/api/select_account/?param=Royal Bank of Scotland - Current Accounts')
        self.assertEqual(response.status_code, 200)
        response_data_first = response.json()
        self.assertEqual(len(list(response_data_first.keys())),2)
        self.assertTrue(list(response_data_first.keys())[0] == 'Savings' or list(response_data_first.keys())[0] == 'Checking')
        self.assertTrue(list(response_data_first.keys())[1] == 'Savings' or list(response_data_first.keys())[1] == 'Checking')

        self.assertEqual(response_data_first[list(response_data_first.keys())[0]], 296.9)
        self.assertEqual(response_data_first[list(response_data_first.keys())[1]], 296.9)

        response_second = self.client.get('/api/select_account/?param=HSBC (UK)')
        self.assertEqual(response_second.status_code, 303)

        response_data = response_second.json()
        self.assertEqual(list(response_data.keys())[0],'error')
        self.assertEqual(response_data[list(response_data.keys())[0]],'Invalid Insitution ID.')

    def test_get_select_account_balances_without_having_first_queried_get_balances_data(self):
        response = self.client.get('/api/select_account/?param=Royal Bank of Scotland - Current Accounts')
        self.assertEqual(response.status_code, 303)
        response_data = response.json()
        self.assertEqual(list(response_data.keys())[0],'error')
        self.assertEqual(response_data[list(response_data.keys())[0]],'Balances not queried.')

    def test_reformat_balances_data_duplicate_account_name(self):
        duplicated_account_balances = {'Royal Bank of Scotland - Current Accounts': {'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}}}
        institution_name = 'Royal Bank of Scotland - Current Accounts'
        response_data_first = reformatAccountBalancesData(duplicated_account_balances,institution_name)
        self.assertEqual(len(list(response_data_first.keys())),2)
        self.assertTrue(list(response_data_first.keys())[0] == 'Checking')
        self.assertTrue(list(response_data_first.keys())[1] == 'Checking_1')
        self.assertEqual(response_data_first[list(response_data_first.keys())[0]], 296.9)
        self.assertEqual(response_data_first[list(response_data_first.keys())[1]], 296.9)
