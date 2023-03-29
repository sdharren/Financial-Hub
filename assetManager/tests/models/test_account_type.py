from django.test import TestCase
from django.core.exceptions import ValidationError
from assetManager.models import User, AccountType, AccountTypeEnum, is_debit, is_stock, is_crypto
from datetime import datetime
import re
from django.db import IntegrityError

"""Tests for the AccountType model """
class AccountTypeCase(TestCase):

    fixtures = ['assetManager/tests/fixtures/users.json'],['assetManager/tests/fixtures/account_types.json']
    def setUp(self):
        self.debit_card_account = AccountType.objects.get(account_type_id = 1)
        self.credit_card_account = AccountType.objects.get(account_type_id = 2)
        self.stock_account = AccountType.objects.get(account_type_id = 3)
        self.crypto_account = AccountType.objects.get(account_type_id = 4)

    def _assert_account_type_is_valid(self,account_type):
         try:
             account_type.full_clean()
         except(ValidationError):
             self.fail('Test account type should be valid')

    def _assert_account_type_is_invalid(self,account_type):
         with self.assertRaises(ValidationError):
             account_type.full_clean()

    def _assert_account_type_using_plaid_api_is_invalid(self,account_type):
         with self.assertRaises(ValueError):
             account_type.save()

    def test_accounts_are_valid(self):
        self._assert_account_type_is_valid(self.debit_card_account)
        self._assert_account_type_is_valid(self.credit_card_account)
        self._assert_account_type_is_valid(self.stock_account)
        self._assert_account_type_is_valid(self.crypto_account)

    def test_debit_and_credit_card_belongs_to_john_doe(self):
        self.assertEqual(self.debit_card_account.user.email,'johndoe@example.org')
        self.assertEqual(self.credit_card_account.user.email,'johndoe@example.org')

    def test_stock_and_crypto_account_belongs_to_lilly(self):
        self.assertEqual(self.stock_account.user.email,'lillydoe@example.org')
        self.assertEqual(self.crypto_account.user.email,'lillydoe@example.org')

    def test_debit_card_is_debit(self):
        self.assertTrue(is_debit(self.debit_card_account.account_asset_type))

    def test_stock_is_stock(self):
        self.assertTrue(is_stock(self.stock_account.account_asset_type))

    def test_crypto_is_crypto(self):
        self.assertTrue(is_crypto(self.crypto_account.account_asset_type))

    def test_debit_card_non_correct_asset_type(self):
        self.debit_card_account.account_asset_type = 'NON VALID ACCOUNT TYPE'
        self._assert_account_type_is_invalid(self.debit_card_account)

    def test_credit_card_non_correct_asset_type(self):
        self.credit_card_account.account_asset_type = 'NON VALID ACCOUNT TYPE'
        self._assert_account_type_is_invalid(self.credit_card_account)

    def test_debit_card_has_correct_access_token_format_incorrect_numberformat(self):
        self.debit_card_account.access_token = "access-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349"
        self._assert_account_type_using_plaid_api_is_invalid(self.debit_card_account)

    def test_debit_card_has_correct_access_token_format_not_access_token(self):
        self.debit_card_account.access_token = "public-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349"
        self._assert_account_type_using_plaid_api_is_invalid(self.debit_card_account)

    def test_credit_card_has_correct_access_token_format_incorrect_numberformat(self):
        self.credit_card_account.access_token = "access-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349"
        self._assert_account_type_using_plaid_api_is_invalid(self.credit_card_account)

    def test_credit_card_has_correct_access_token_format_incorrect_numberformat(self):
        self.credit_card_account.access_token = "public-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349"
        self._assert_account_type_using_plaid_api_is_invalid(self.credit_card_account)

    def test_violate_composite_key_integrity(self):
        with self.assertRaises(IntegrityError):
            self.accountCopy = AccountType.objects.create(
                user = User.objects.get(email = 'johndoe@example.org'),
                account_type_id = 1,
                account_asset_type = AccountTypeEnum.DEBIT,
                account_date_linked = datetime(2020,10,10),
                access_token = "access-development-8ab976e6-64bc-4b38-98f7-731e7a349970"
                )

    def test_violate_same_primary_key(self):
        with self.assertRaises(IntegrityError):
            self.accountCopy = AccountType.objects.create(
                user = User.objects.get(email = 'johndoe@example.org'),
                account_type_id = 1,
                account_asset_type = AccountTypeEnum.DEBIT,
                account_date_linked = datetime(2020,10,10),
                access_token = "access-development-8ab976e6-64bc-4b38-98f7-731e7a349999"
                )
