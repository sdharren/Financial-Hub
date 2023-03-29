from django.test import TestCase
from django.urls import reverse
from assetManager.models import User, AccountTypeEnum, AccountType
from rest_framework.test import APIClient
from rest_framework import status
import json
from assetManager.api.views import get_linked_banks
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from django.conf import settings
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.models import AccountTypeEnum,AccountType
from assetManager.assets.debit_card import DebitCard
from django.core.cache import cache

class DeleteLinkedCrytpoViewTestCase(TestCase):
    """Tests for the delete_linked_crypto view function."""

    fixtures = [
        'assetManager/tests/fixtures/users.json'
    ]

    def setUp(self):
        settings.PLAID_DEVELOPMENT = False
        self.user = User.objects.get(email='johndoe@example.org')
        self.client = APIClient()
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.post('/api/token/', {'email': self.user.email, 'password': 'Password123'}, format='json')
        self.jwt = str(response.data['access'])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ self.jwt)

        self.crypto = 'bc1qcw8ge4yr2xummxeey25y02g3v0nl4cdyhd095v'
        self.account_type = AccountType.objects.create(
            user=self.user,
            account_asset_type=AccountTypeEnum.CRYPTO,
            access_token=self.crypto,
            account_institution_name='btc',
        )

    def tearDown(self):
        cache.clear()

    def test_delete_linked_crypto_with_valid_wallet_address_no_cache(self):
        self.assertFalse(cache.has_key('crypto' + self.user.email))
        institutions_number_change = self.client.get(reverse("linked_crypto"), format="json")
        self.assertEqual(institutions_number_change.status_code, 200)
        institutions_2 = institutions_number_change.json()

        self.assertEqual(len(institutions_2), 1)


        url = reverse('delete_linked_crypto', kwargs={'crypto': self.crypto})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(cache.has_key('crypto' + self.user.email))

        institutions_number_change = self.client.get(reverse("linked_crypto"), format="json")
        self.assertEqual(institutions_number_change.status_code, 200)
        institutions_2 = institutions_number_change.json()
        self.assertEqual(len(institutions_2), 0)


        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AccountType.objects.filter(user=self.user, account_asset_type=AccountTypeEnum.CRYPTO, access_token = 'bc1qcw8ge4yr2xummxeey25y02g3v0nl4cdyhd095v').exists())

    def test_delete_linked_crypto_account_with_invalid_wallet_address(self):
        url = reverse('delete_linked_crypto', kwargs={'crypto': 'bc1qcw8ge4yr2xummxeey25y02g3v0nl4cdyhd095K'})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(AccountType.objects.filter(user=self.user, account_asset_type=AccountTypeEnum.CRYPTO, access_token='bc1qcw8ge4yr2xummxeey25y02g3v0nl4cdyhd095v').exists())

    def test_delete_linked_crypto_with_unauthenticated_user(self):
        self.client.credentials()
        url = reverse('delete_linked_crypto', kwargs={'crypto': self.crypto})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(AccountType.objects.filter(user=self.user, account_asset_type=AccountTypeEnum.CRYPTO, access_token='bc1qcw8ge4yr2xummxeey25y02g3v0nl4cdyhd095v').exists())

    def test_delete_linked_crypto_with_wrong_method(self):
        url = reverse('delete_linked_crypto', kwargs={'crypto': self.crypto})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(AccountType.objects.filter(user=self.user, account_asset_type=AccountTypeEnum.CRYPTO, access_token='bc1qcw8ge4yr2xummxeey25y02g3v0nl4cdyhd095v').exists())


    def test_multiple_delete_crypto(self):
        cache.set('crypto' + self.user.email,'random-data-that-will-be-deleted')
        AccountType.objects.create(
            user=self.user,
            account_asset_type=AccountTypeEnum.CRYPTO,
            access_token="0x9696f59e4d72e237be84ffd425dcad154bf96976",
            account_institution_name='eth',
        )

        response = self.client.get(reverse("linked_crypto"), format="json")
        self.assertEqual(response.status_code, 200)
        cryptos = response.json()
        self.assertEqual(len(cryptos), 2)

        # Delete institution
        url = reverse('delete_linked_crypto', kwargs={'crypto':'0x9696f59e4d72e237be84ffd425dcad154bf96976'})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(cache.has_key("crypto" + self.user.email))
        # Check number of linked institutions after deleting
        response = self.client.get(reverse("linked_crypto"), format="json")
        self.assertEqual(response.status_code, 200)
        institutions = response.json()
        self.assertEqual(len(institutions), 1)
