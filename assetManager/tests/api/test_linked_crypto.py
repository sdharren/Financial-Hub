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
from django.core.cache import cache

class GetLinkedCryptoViewsTestCase(TestCase):
    """Tests of the log in view."""
    fixtures = [
        'assetManager/tests/fixtures/users.json'
    ]

    def setUp(self):
        settings.PLAID_DEVELOPMENT = False
        self.url = reverse('linked_crypto')
        self.user = User.objects.get(email='johndoe@example.org')
        self.client = APIClient()
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.post('/api/token/', {'email': self.user.email, 'password': 'Password123'}, format='json')
        jwt = str(response.data['access'])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ jwt)

    def tearDown(self):
        cache.clear()

    def test_link_banks_transactions_url(self):
        self.assertEqual(self.url,'/api/linked_crypto/')

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
            account_asset_type = AccountTypeEnum.CRYPTO,
            access_token = '0x9696f59e4d72e237be84ffd425dcad154bf96976',
            account_institution_name = 'btc',
        )
        response = self.client.get(self.url,follow = True)
        self.assertEqual(response.status_code,200)
        wallet_address = response.json()
        self.assertEqual(wallet_address,['0x9696f59e4d72e237be84ffd425dcad154bf96976'])


    def test_get_no_linked_institution(self):
        response = self.client.get(self.url,follow = True)
        self.assertEqual(response.status_code,200)
        wallet_address = response.json()
        self.assertEqual(wallet_address,[])


    def test_get_multiple_linked_institution_names(self):
        AccountType.objects.create(
            user = self.user,
            account_asset_type = AccountTypeEnum.CRYPTO,
            access_token = '0x9696f59e4d72e237be84ffd425dcad154bf96979',
            account_institution_name = 'eth',
        )
        AccountType.objects.create(
            user = self.user,
            account_asset_type = AccountTypeEnum.CRYPTO,
            access_token = '0x9696f59e4d72e237be84ffd425dcad154bf96970',
            account_institution_name = 'btc',
        )
        response = self.client.get(self.url,follow = True)
        self.assertEqual(response.status_code,200)
        wallet_address = response.json()
        self.assertEqual(wallet_address,['0x9696f59e4d72e237be84ffd425dcad154bf96979', '0x9696f59e4d72e237be84ffd425dcad154bf96970'])


    def test_get_linked_banks_with_unauthenticated_user(self):
        self.client.logout()
        url = reverse('linked_crypto')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 401)
