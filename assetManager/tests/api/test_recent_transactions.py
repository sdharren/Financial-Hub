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
from django.conf import settings
from assetManager.models import AccountTypeEnum,AccountType
from django.core.cache import cache
from datetime import datetime, date

class RecentTransactionsViewsTestCase(TestCase):
    """Tests of the log in view."""
    fixtures = [
        'assetManager/tests/fixtures/users.json'
    ]

    def tearDown(self):
        cache.clear()

    def setUp(self):
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

    def test_get_recent_transactions_without_institution_name_param(self):
        settings.PLAID_DEVELOPMENT = False
        response = self.client.get('/api/recent_transactions/?param=')
        self.assertEqual(response.status_code, 303)

        response_data = response.json()
        self.assertEqual(list(response_data.keys())[0],'error')
        self.assertEqual(response_data[list(response_data.keys())[0]],'Institution Name Not Selected')

    def test_get_recent_transactions_with_non_linked_institution_name(self):
        settings.PLAID_DEVELOPMENT = False
        response = self.client.get('/api/recent_transactions/?param=HSBC UK')
        self.assertEqual(response.status_code, 303)

        response_data = response.json()
        self.assertEqual(list(response_data.keys())[0],'error')
        self.assertEqual(response_data[list(response_data.keys())[0]],'Institution Selected Is Not Linked.')
        
    def test_get_recent_transactions_with_correctly_linked_institution(self):
        settings.PLAID_DEVELOPMENT = False
        response = self.client.get('/api/recent_transactions/?param=Royal Bank of Scotland - Current Accounts')
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(list(response_data.keys())[0],'Royal Bank of Scotland - Current Accounts')
        self.assertTrue(0 < len(response_data['Royal Bank of Scotland - Current Accounts']) <= 5)
        self.assertTrue(datetime.strptime(response_data['Royal Bank of Scotland - Current Accounts'][0]['date'], '%Y-%m-%d').date() <= date.today())
        #self.assertEqual(response_data['Royal Bank of Scotland - Current Accounts'][0]['amount'],'£500.0')
        #self.assertEqual(response_data['Royal Bank of Scotland - Current Accounts'][0]['date'],'2023-03-16')
        #self.assertEqual(response_data['Royal Bank of Scotland - Current Accounts'][0]['category'],['Travel', 'Airlines and Aviation Services'])
        #self.assertEqual(response_data['Royal Bank of Scotland - Current Accounts'][0]['merchant'],'United Airlines')
