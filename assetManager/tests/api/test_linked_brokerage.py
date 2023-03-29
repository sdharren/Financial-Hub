from django.test import TestCase
from django.urls import reverse
from django.contrib import messages
from assetManager.models import User
import json

from assetManager.api.views import get_linked_banks

from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from django.conf import settings
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.models import AccountTypeEnum,AccountType
from assetManager.assets.debit_card import DebitCard

class GetLinkedBrokerageViewsTestCase(TestCase):
    """Tests of the log in view."""
    fixtures = [
        'assetManager/tests/fixtures/users.json'
    ]

    def setUp(self):
        settings.PLAID_DEVELOPMENT = False
        self.url = reverse('linked_brokerage')
        self.user = User.objects.get(email='johndoe@example.org')
        self.client = APIClient()
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.post('/api/token/', {'email': self.user.email, 'password': 'Password123'}, format='json')
        jwt = str(response.data['access'])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ jwt)

    def test_link_banks_transactions_url(self):
        self.assertEqual(self.url,'/api/linked_brokerage/')

    def test_get_institution_data_without_jwt_not_logged_in(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_make_post_request_to_get_linked_banks_url(self):
        response = self.client.post(self.url, follow = True)
        self.assertEqual(response.status_code,405)



    def test_get_linked_brokerage_name(self):
        
        AccountType.objects.create(
            user = self.user,
            account_asset_type = AccountTypeEnum.STOCK,
            access_token = 'access-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349971',
            account_institution_name = 'Vanguard',
        )
        response = self.client.get(self.url,follow = True)
        self.assertEqual(response.status_code,200)
        brokerage_name = response.json()
        self.assertEqual(brokerage_name,['Vanguard'])


    def test_get_no_linked_institution(self):
        
        response = self.client.get(self.url,follow = True)
        self.assertEqual(response.status_code,200)
        institution_name = response.json()
        self.assertEqual(institution_name,[])


    def test_get_multiple_linked_institution_names(self):
        
        AccountType.objects.create(
            user = self.user,
            account_asset_type = AccountTypeEnum.STOCK,
            access_token = 'access-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349111',
            account_institution_name = 'Vanguard',
        )
        AccountType.objects.create(
            user = self.user,
            account_asset_type = AccountTypeEnum.STOCK,
            access_token = 'access-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349112',
            account_institution_name = 'Fidelity',
        )
        response = self.client.get(self.url,follow = True)
        self.assertEqual(response.status_code,200)
        institution_name = response.json()
        self.assertEqual(institution_name,['Vanguard', 'Fidelity'])


    def test_get_linked_banks_with_unauthenticated_user(self):
        
        self.client.logout()
        url = reverse('linked_brokerage')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 401)
