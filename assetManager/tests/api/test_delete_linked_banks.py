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

class DeleteLinkedBanksViewTestCase(TestCase):
    """Tests for the delete_linked_banks view function."""

    fixtures = [
        'assetManager/tests/fixtures/users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.org')
        self.client = APIClient()
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.post('/api/token/', {'email': self.user.email, 'password': 'Password123'}, format='json')
        self.jwt = str(response.data['access'])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ self.jwt)

        self.institution = 'HSBC'
        self.account_type = AccountType.objects.create(
            user=self.user,
            account_asset_type=AccountTypeEnum.DEBIT,
            access_token='access-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349971',
            account_institution_name=self.institution,
        )

    def test_delete_linked_banks_with_valid_institution(self):
        settings.PLAID_DEVELOPMENT = False
        
        institutions_number_change = self.client.get(reverse("get_linked_banks"), format="json")
        self.assertEqual(institutions_number_change.status_code, 200)
        institutions_2 = institutions_number_change.json()
        print(institutions_2)
        self.assertEqual(len(institutions_2), 1)
        

        url = reverse('delete_linked_banks', kwargs={'institution': self.institution})
        response = self.client.delete(url)

        
        institutions_number_change = self.client.get(reverse("get_linked_banks"), format="json")
        self.assertEqual(institutions_number_change.status_code, 200)
        institutions_2 = institutions_number_change.json()
        print(institutions_2)
        self.assertEqual(len(institutions_2), 0)
        

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AccountType.objects.filter(user=self.user, account_asset_type=AccountTypeEnum.DEBIT, account_institution_name=self.institution).exists())

    def test_delete_linked_banks_with_invalid_institution(self):
        settings.PLAID_DEVELOPMENT = False
        url = reverse('delete_linked_banks', kwargs={'institution': 'Non-existent bank'})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(AccountType.objects.filter(user=self.user, account_asset_type=AccountTypeEnum.DEBIT, account_institution_name=self.institution).exists())

    def test_delete_linked_banks_with_unauthenticated_user(self):
        settings.PLAID_DEVELOPMENT = False
        self.client.credentials()
        url = reverse('delete_linked_banks', kwargs={'institution': self.institution})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(AccountType.objects.filter(user=self.user, account_asset_type=AccountTypeEnum.DEBIT, account_institution_name=self.institution).exists())

    def test_delete_linked_banks_with_wrong_method(self):
        settings.PLAID_DEVELOPMENT = False
        url = reverse('delete_linked_banks', kwargs={'institution': self.institution})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(AccountType.objects.filter(user=self.user, account_asset_type=AccountTypeEnum.DEBIT, account_institution_name=self.institution).exists())
    
    def test_add_delete_institution(self):
        settings.PLAID_DEVELOPMENT = False
        # Add institution
        institution_name_add = "Bank of America"
        AccountType.objects.create(
            user=self.user,
            account_asset_type=AccountTypeEnum.DEBIT,
            access_token="access-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349971",
            account_institution_name=institution_name_add,
        )

        #Check number of linked institutions after adding
        response = self.client.get(reverse("get_linked_banks"), format="json")
        self.assertEqual(response.status_code, 200)
        institutions = response.json()
        print(institutions)
        self.assertEqual(len(institutions), 2)

        # Delete institution
        url = reverse('delete_linked_banks', kwargs={'institution': institution_name_add})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
       

        # Check number of linked institutions after deleting
        response = self.client.get(reverse("get_linked_banks"), format="json")
        self.assertEqual(response.status_code, 200)
        institutions = response.json()
        print(institutions)
        self.assertEqual(len(institutions), 1)