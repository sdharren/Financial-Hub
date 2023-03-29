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
from django.conf import settings

class GetLinkedBankViewsTestCase(TestCase):
    """Tests of the log in view."""
    fixtures = [
        'assetManager/tests/fixtures/users.json'
    ]

    def setUp(self):
        settings.PLAID_DEVELOPMENT = False
        self.url = reverse('get_linked_banks')
        self.user = User.objects.get(email='johndoe@example.org')
        self.client = APIClient()
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.post('/api/token/', {'email': self.user.email, 'password': 'Password123'}, format='json')
        jwt = str(response.data['access'])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ jwt)

    def test_link_banks_transactions_url(self):
        self.assertEqual(self.url,'/api/get_linked_banks/')

    def test_get_institution_data_without_jwt_not_logged_in(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_make_post_request_to_get_linked_banks_url(self):
        response = self.client.post(self.url, follow = True)
        self.assertEqual(response.status_code,405)



    def test_get_linked_institution_name(self):
      
        AccountType.objects.create(
            user = self.user,
            account_asset_type = AccountTypeEnum.DEBIT,
            access_token = 'access-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349971',
            account_institution_name = 'HSBC',
        )
        response = self.client.get(self.url,follow = True)
        self.assertEqual(response.status_code,200)
        institution_name = response.json()
        self.assertEqual(institution_name,['HSBC'])

    def test_get_no_linked_institution(self):
        settings.PLAID_DEVELOPMENT = False
        response = self.client.get(self.url,follow = True)
        self.assertEqual(response.status_code,200)
        institution_name = response.json()
        self.assertEqual(institution_name,[])


    def test_get_multiple_linked_institution_names(self):
        
        AccountType.objects.create(
            user = self.user,
            account_asset_type = AccountTypeEnum.DEBIT,
            access_token = 'access-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349111',
            account_institution_name = 'HSBC',
        )
        AccountType.objects.create(
            user = self.user,
            account_asset_type = AccountTypeEnum.DEBIT,
            access_token = 'access-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349112',
            account_institution_name = 'Barclays',
        )
        response = self.client.get(self.url,follow = True)
        self.assertEqual(response.status_code,200)
        institution_name = response.json()
        self.assertEqual(institution_name,['HSBC','Barclays'])


    def test_get_linked_banks_with_unauthenticated_user(self):
        
        self.client.logout()
        url = reverse('get_linked_banks')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 401)
