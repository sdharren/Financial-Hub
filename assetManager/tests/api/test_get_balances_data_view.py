from django.test import TestCase
from django.urls import reverse
from django.contrib import messages
from assetManager.models import User
import json
from assetManager.api.views import reformatBalancesData

from assetManager.api.views import get_balances_data,delete_balances_cache

from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from django.conf import settings
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.models import AccountTypeEnum,AccountType

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
        settings.PLAID_DEVELOPMENT = False
        account_balances = {'Royal Bank of Scotland - Current Accounts': {'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}}}
        balances = reformatBalancesData(account_balances)
        self.assertEqual(len(balances),1)
        self.assertEqual(list(balances.keys())[0], 'Royal Bank of Scotland - Current Accounts')
        self.assertEqual(balances[list(balances.keys())[0]], 593.8004402054293)


    def test_make_post_request_to_url(self):
        response = self.client.post(self.url, follow = True)
        self.assertEqual(response.status_code,405)


    def test_get_balances_with_no_linked_transaction_access_token(self):
        user_lilly = User.objects.get(email='lillydoe@example.org')
        settings.PLAID_DEVELOPMENT = True
        client = APIClient()
        client.login(email=user_lilly.email, password='Password123')
        response = client.post('/api/token/', {'email': user_lilly.email, 'password': 'Password123'}, format='json')
        jwt = str(response.data['access'])
        client.credentials(HTTP_AUTHORIZATION='Bearer '+ jwt)

        response = client.get('/api/get_balances_data/')
        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.content.decode('utf-8'), '{"error":"Transactions Not Linked."}')


    def test_get_balances_succesfully(self):
        settings.PLAID_DEVELOPMENT = False
        response = self.client.get(self.url, follow=True)
        response_data = response.json()
        self.assertEqual(response_data['Royal Bank of Scotland - Current Accounts'], 593.8004402054293)
        self.assertEqual(response.status_code,200)
        delete_balances_cache(self.user)

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

        self.assertEqual(account_balances[list(account_balances.keys())[0]], 25830.31914893617)
        self.assertEqual(account_balances[list(account_balances.keys())[1]], 593.8004402054293)

        delete_balances_cache(self.user)

    def test_get_balances_data_enforce_cache_delete_due_to_new_institution_linked_in_application(self):
        settings.PLAID_DEVELOPMENT = False
        before_count = len(AccountType.objects.filter(user = self.user, account_asset_type = AccountTypeEnum.DEBIT))
        response_first = self.client.get(reverse('get_balances_data'), follow=True)
        self.assertEqual(response_first.status_code, 200)
        after_count = len(AccountType.objects.filter(user = self.user, account_asset_type = AccountTypeEnum.DEBIT))
        self.assertEqual(before_count + 1, after_count)

        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token(bank_id='ins_1', products_chosen=['transactions'])
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(self.user, ['transactions'])
        new_count = len(AccountType.objects.filter(user = self.user, account_asset_type = AccountTypeEnum.DEBIT))
        self.assertEqual(before_count + 2, new_count)
        response = self.client.get(reverse('get_balances_data'), follow=True)
        self.assertEqual(response.status_code, 200)
        account_balances = response.json()

        self.assertEqual(list(account_balances.keys())[0], 'Royal Bank of Scotland - Current Accounts')
        self.assertEqual(list(account_balances.keys())[1], 'Bank of America')

        self.assertEqual(account_balances[list(account_balances.keys())[0]], 593.8004402054293)
        self.assertEqual(account_balances[list(account_balances.keys())[1]], 25830.31914893617)
        delete_balances_cache(self.user)

    def test_get_balances_data_from_the_cache(self):
        settings.PLAID_DEVELOPMENT = False
        response = self.client.get(self.url, follow=True)
        response_data = response.json()
        self.assertEqual(response_data['Royal Bank of Scotland - Current Accounts'], 593.8004402054293)
        self.assertEqual(response.status_code,200)

        settings.PLAID_DEVELOPMENT = True
        response_second = self.client.get(self.url, follow=True)
        response_data_second = response_second.json()
        self.assertTrue(response_data_second['Royal Bank of Scotland - Current Accounts'] != response_data['Royal Bank of Scotland - Current Accounts'])
        self.assertEqual(response_second.status_code,200)
        delete_balances_cache(self.user)
