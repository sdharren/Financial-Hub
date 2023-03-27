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
from assetManager.models import AccountTypeEnum,AccountType
from django.core.cache import cache
from datetime import datetime, date
from assetManager.api.views import reformatBalancesData

class RecentTransactionsViewsTestCase(TestCase):
    """Tests of the log in view."""
    fixtures = [
        'assetManager/tests/fixtures/users.json'
    ]

    def create_public_token(self):
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token()
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(self.user, ['transactions'])

    def tearDown(self):
        cache.clear()

    def setUp(self):
        settings.PLAID_DEVELOPMENT = False
        self.url = reverse('recent_transactions')
        self.user = User.objects.get(email='johndoe@example.org')
        self.client = APIClient()
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.post('/api/token/', {'email': self.user.email, 'password': 'Password123'}, format='json')
        jwt = str(response.data['access'])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ jwt)


    def test_recent_transactions_url(self):
        self.assertEqual(self.url,'/api/recent_transactions/')

    def test_get_recent_transanctions_without_jwt_not_logged_in(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_make_post_request_to_recent_transactions_url(self):
        response = self.client.post(self.url, follow = True)
        self.assertEqual(response.status_code,405)

    def test_get_recent_transactions_with_non_linked_institution_name(self):
        response = self.client.get('/api/recent_transactions/?param=HSBC UK')
        self.assertEqual(response.status_code, 303)
        response_data = response.json()
        self.assertEqual(list(response_data.keys())[0],'error')
        self.assertEqual(response_data[list(response_data.keys())[0]],'Transactions Not Linked.')

    def test_get_recent_transactions_with_correctly_linked_institution(self):
        self.create_public_token()
        self.assertFalse(cache.has_key('transactions' + self.user.email))
        response = self.client.get('/api/recent_transactions/?param=Royal Bank of Scotland - Current Accounts')
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(list(response_data.keys())[0],'Royal Bank of Scotland - Current Accounts')
        self.assertTrue(0 < len(response_data['Royal Bank of Scotland - Current Accounts']) <= 10)
        self.assertTrue(datetime.strptime(response_data['Royal Bank of Scotland - Current Accounts'][0]['date'], '%Y-%m-%d').date() <= date.today())

        if(len(response_data['Royal Bank of Scotland - Current Accounts']) > 0):
            self.assertTrue('amount' in response_data['Royal Bank of Scotland - Current Accounts'][0])
            self.assertTrue('date' in response_data['Royal Bank of Scotland - Current Accounts'][0])
            self.assertTrue('category' in response_data['Royal Bank of Scotland - Current Accounts'][0])
            self.assertTrue('merchant' in response_data['Royal Bank of Scotland - Current Accounts'][0])


    def test_recent_transactions_data_with_incorrectly_saved_token_causing_an_error(self):
        settings.PLAID_DEVELOPMENT = True
        AccountType.objects.create(
            user = self.user,
            account_asset_type = AccountTypeEnum.DEBIT,
            access_token = 'access-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349971',
            account_institution_name = 'HSBC',
        )

        response = self.client.get('/api/recent_transactions/?param=HSBC')
        self.assertEqual(response.status_code, 303)

        response_data = response.json()
        self.assertEqual(list(response_data.keys())[0],'error')
        self.assertEqual(response_data[list(response_data.keys())[0]],'Something went wrong querying PLAID.')

    def test_recent_transactions_with_no_cache_incorrect_access_token(self):
        settings.PLAID_DEVELOPMENT = True
        AccountType.objects.create(
            user = self.user,
            account_asset_type = AccountTypeEnum.DEBIT,
            access_token = 'access-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349971',
            account_institution_name = 'HSBC',
        )

        response = self.client.get('/api/recent_transactions/?param=HSBC')
        self.assertEqual(response.status_code, 303)

        response_data = response.json()
        self.assertEqual(list(response_data.keys())[0],'error')
        self.assertEqual(response_data[list(response_data.keys())[0]],'Something went wrong querying PLAID.')

    def test_recent_transactions_with_no_cache_no_access_token(self):
        settings.PLAID_DEVELOPMENT = True
        response = self.client.get('/api/recent_transactions/?param=HSBC')
        self.assertEqual(response.status_code, 303)

        response_data = response.json()
        self.assertEqual(list(response_data.keys())[0],'error')
        self.assertEqual(response_data[list(response_data.keys())[0]],'Transactions Not Linked.')
