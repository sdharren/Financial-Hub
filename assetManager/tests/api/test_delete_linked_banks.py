from django.test import TestCase
from django.urls import reverse
from assetManager.models import User, AccountTypeEnum, AccountType
from rest_framework.test import APIClient
from rest_framework import status
import json
from assetManager.api.views import get_linked_banks
from django.conf import settings
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from django.conf import settings
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.models import AccountTypeEnum,AccountType
from assetManager.assets.debit_card import DebitCard
from django.core.cache import cache

class DeleteLinkedBanksViewTestCase(TestCase):
    """Tests for the delete_linked_banks view function."""

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

        self.institution = 'HSBC'
        self.account_type = AccountType.objects.create(
            user=self.user,
            account_asset_type=AccountTypeEnum.DEBIT,
            access_token='access-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349971',
            account_institution_name=self.institution,
        )

    def tearDown(self):
        cache.clear()

    def test_delete_linked_banks_with_valid_institution_no_cache(self):
        self.assertFalse(cache.has_key('transactions' + self.user.email))
        self.assertFalse(cache.has_key('currency' + self.user.email))
        self.assertFalse(cache.has_key('balances' + self.user.email))

        institutions_number_change = self.client.get(reverse("get_linked_banks"), format="json")
        self.assertEqual(institutions_number_change.status_code, 200)
        institutions_2 = institutions_number_change.json()

        self.assertEqual(len(institutions_2), 1)

        url = reverse('delete_linked_banks', kwargs={'institution': self.institution})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(cache.has_key('transactions' + self.user.email))
        self.assertFalse(cache.has_key('currency' + self.user.email))
        self.assertFalse(cache.has_key('balances' + self.user.email))

        institutions_number_change = self.client.get(reverse("get_linked_banks"), format="json")
        self.assertEqual(institutions_number_change.status_code, 200)
        institutions_2 = institutions_number_change.json()

        self.assertEqual(len(institutions_2), 0)


        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AccountType.objects.filter(user=self.user, account_asset_type=AccountTypeEnum.DEBIT, account_institution_name=self.institution).exists())

    def test_delete_linked_banks_with_invalid_institution(self):
        url = reverse('delete_linked_banks', kwargs={'institution': 'Non-existent bank'})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(AccountType.objects.filter(user=self.user, account_asset_type=AccountTypeEnum.DEBIT, account_institution_name=self.institution).exists())

    def test_delete_linked_banks_with_unauthenticated_user(self):
        self.client.credentials()
        url = reverse('delete_linked_banks', kwargs={'institution': self.institution})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(AccountType.objects.filter(user=self.user, account_asset_type=AccountTypeEnum.DEBIT, account_institution_name=self.institution).exists())

    def test_delete_linked_banks_with_wrong_method(self):
        url = reverse('delete_linked_banks', kwargs={'institution': self.institution})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(AccountType.objects.filter(user=self.user, account_asset_type=AccountTypeEnum.DEBIT, account_institution_name=self.institution).exists())

    def test_add_delete_institution_with_cache(self):
        cache.set('balances' + self.user.email, {'Fidelity': {'v448a7e8nRcA68Z4mBklURyBqXozmWFnp1XXa': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, '9xx9bgy9EwCRXBpakQw8HJBM7DZV6kcVrgEEe': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}}, 'Royal Bank of Scotland - Current Accounts': {'g1Ro1DZ44EC3g5nx6vADUwMLD4aEdDH4W7VXw': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'oAKvA6NMMltzMqEX7lmAcKqWakRJpatkEVM3E': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}}})

        cache.set('transactions' + self.user.email, {'Fidelity': [{'authorized_date': [2022, 12, 16], 'date': [2022, 12, 17], 'amount': 532.43, 'category': ['Payment', 'Credit Card'], 'name': 'DEBIT CRD AUTOPAY 98712 000000000028791 KIUYPWRSGTKF UXYOTLLKJHA C', 'iso_currency_code': 'USD', 'merchant_name': 'Not Provided'}, {'authorized_date': [2022, 12, 16], 'date': [2022, 12, 17], 'amount': 236.53, 'category': ['Payment', 'Credit Card'], 'name': 'DEBIT CRD AUTOPAY 98712 000000000098712 WRSGTKIUYPKF KJHAUXYOTLL A', 'iso_currency_code': 'USD', 'merchant_name': 'Not Provided'}, {'authorized_date': [2022, 12, 16], 'date': [2022, 12, 16], 'amount': 1014.28, 'category': ['Payment', 'Credit Card'], 'name': 'CREDIT CRD AUTOPAY 29812 000000000098123 CRGKFKKSPABG UXZYOTAYLDA D', 'iso_currency_code': 'USD', 'merchant_name': 'Not Provided'}, {'authorized_date': [2022, 12, 16], 'date': [2022, 12, 16], 'amount': 658.53, 'category': ['Payment', 'Credit Card'], 'name': 'CREDIT CRD AUTOPAY 29812 000000000098123 KABCRGKSPKFG YOTALDUXZYA B', 'iso_currency_code': 'USD', 'merchant_name': 'Not Provided'}], 'Royal Bank of Scotland - Current Accounts': [{'authorized_date': [2022, 12, 16], 'date': [2022, 12, 17], 'amount': 532.43, 'category': ['Transfer', 'Debit'], 'name': 'DEBIT CRD AUTOPAY 98712 000000000028791 KIUYPWRSGTKF UXYOTLLKJHA C', 'iso_currency_code': 'USD', 'merchant_name': 'Not Provided'}, {'authorized_date': [2022, 12, 16], 'date': [2022, 12, 17], 'amount': 236.53, 'category': ['Transfer', 'Debit'], 'name': 'DEBIT CRD AUTOPAY 98712 000000000098712 WRSGTKIUYPKF KJHAUXYOTLL A', 'iso_currency_code': 'USD', 'merchant_name': 'Not Provided'}, {'authorized_date': [2022, 12, 16], 'date': [2022, 12, 16], 'amount': 1014.28, 'category': ['Food and Drink', 'Restaurants'], 'name': 'CREDIT CRD AUTOPAY 29812 000000000098123 CRGKFKKSPABG UXZYOTAYLDA D', 'iso_currency_code': 'USD', 'merchant_name': 'Not Provided'}, {'authorized_date': [2022, 12, 16], 'date': [2022, 12, 16], 'amount': 658.53, 'category': ['Transfer', 'Debit'], 'name': 'CREDIT CRD AUTOPAY 29812 000000000098123 KABCRGKSPKFG YOTALDUXZYA B', 'iso_currency_code': 'USD', 'merchant_name': 'Not Provided'}]})

        self.assertTrue(len(list(cache.get('balances' + self.user.email).keys())), 2)
        self.assertTrue(len(list(cache.get('transactions' + self.user.email).keys())), 2)

        institution_name_add = "Fidelity"
        AccountType.objects.create(
            user=self.user,
            account_asset_type=AccountTypeEnum.DEBIT,
            access_token="access-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349111",
            account_institution_name=institution_name_add,
        )

        #Check number of linked institutions after adding
        response = self.client.get(reverse("get_linked_banks"), format="json")
        self.assertEqual(response.status_code, 200)
        institutions = response.json()

        self.assertEqual(len(institutions), 2)

        # Delete institution
        url = reverse('delete_linked_banks', kwargs={'institution': institution_name_add})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(cache.has_key('transactions' + self.user.email))
        self.assertTrue(cache.has_key('balances' + self.user.email))

        self.assertTrue(len(list(cache.get('balances' + self.user.email).keys())), 1)
        self.assertTrue(len(list(cache.get('transactions' + self.user.email).keys())), 1)

        # Check number of linked institutions after deleting
        response = self.client.get(reverse("get_linked_banks"), format="json")
        self.assertEqual(response.status_code, 200)
        institutions = response.json()
    
        self.assertEqual(len(institutions), 1)

    def test_delete_same_institution_name_different_type(self):
        self.account_type = AccountType.objects.create(
            user=self.user,
            account_asset_type=AccountTypeEnum.STOCK,
            access_token='access-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349972',
            account_institution_name=self.institution,
        )
        before_count = AccountType.objects.count()
        url = reverse('delete_linked_banks', kwargs={'institution': self.account_type.account_institution_name})
        response = self.client.delete(url)
        after_count = AccountType.objects.count()
        self.assertEqual(before_count - 1, after_count)

        deleted_institution = AccountType.objects.filter(user = self.user, account_asset_type = AccountTypeEnum.DEBIT, account_institution_name=self.institution)
        self.assertEqual(len(deleted_institution),0)
        not_deleted_institution = AccountType.objects.filter(user = self.user, account_asset_type = AccountTypeEnum.STOCK, account_institution_name=self.institution)
        self.assertEqual(len(not_deleted_institution),1)
    def test_delete_linked_bank_with_only_one_bank_saved_in_cache(self):
        cache.set('balances' + self.user.email, {'Fidelity': {'v448a7e8nRcA68Z4mBklURyBqXozmWFnp1XXa': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, '9xx9bgy9EwCRXBpakQw8HJBM7DZV6kcVrgEEe': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}}})

        cache.set('transactions' + self.user.email, {'Fidelity': [{'authorized_date': [2022, 12, 16], 'date': [2022, 12, 17], 'amount': 532.43, 'category': ['Payment', 'Credit Card'], 'name': 'DEBIT CRD AUTOPAY 98712 000000000028791 KIUYPWRSGTKF UXYOTLLKJHA C', 'iso_currency_code': 'USD', 'merchant_name': 'Not Provided'}, {'authorized_date': [2022, 12, 16], 'date': [2022, 12, 17], 'amount': 236.53, 'category': ['Payment', 'Credit Card'], 'name': 'DEBIT CRD AUTOPAY 98712 000000000098712 WRSGTKIUYPKF KJHAUXYOTLL A', 'iso_currency_code': 'USD', 'merchant_name': 'Not Provided'}, {'authorized_date': [2022, 12, 16], 'date': [2022, 12, 16], 'amount': 1014.28, 'category': ['Payment', 'Credit Card'], 'name': 'CREDIT CRD AUTOPAY 29812 000000000098123 CRGKFKKSPABG UXZYOTAYLDA D', 'iso_currency_code': 'USD', 'merchant_name': 'Not Provided'}, {'authorized_date': [2022, 12, 16], 'date': [2022, 12, 16], 'amount': 658.53, 'category': ['Payment', 'Credit Card'], 'name': 'CREDIT CRD AUTOPAY 29812 000000000098123 KABCRGKSPKFG YOTALDUXZYA B', 'iso_currency_code': 'USD', 'merchant_name': 'Not Provided'}]})

        self.assertTrue(cache.has_key('balances' + self.user.email))
        self.assertTrue(cache.has_key('transactions' + self.user.email))
        self.assertTrue(len(list(cache.get('balances' + self.user.email).keys())), 1)
        self.assertTrue(len(list(cache.get('transactions' + self.user.email).keys())), 1)

        institution_name_add = "Fidelity"
        AccountType.objects.create(
            user=self.user,
            account_asset_type=AccountTypeEnum.DEBIT,
            access_token="access-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349111",
            account_institution_name=institution_name_add,
        )

        response = self.client.get(reverse("get_linked_banks"), format="json")
        self.assertEqual(response.status_code, 200)
        institutions = response.json()

        self.assertEqual(len(institutions), 2)

        # Delete institution
        url = reverse('delete_linked_banks', kwargs={'institution': institution_name_add})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(cache.has_key('transactions' + self.user.email))
        self.assertFalse(cache.has_key('balances' + self.user.email))
