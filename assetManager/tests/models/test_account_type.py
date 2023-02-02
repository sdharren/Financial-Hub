from django.test import TestCase
from django.core.exceptions import ValidationError
from assetManager.models import AccountType, AccountTypeEnum, is_debit, is_credit, is_stock, is_crypto
from datetime import datetime

class AccountTypeCase(TestCase):

    def setUp(self):
        self.debit_card_account = AccountType.objects.create(
            account_date_linked = datetime(2020, 10, 19,20,20,20),
            account_asset_type = AccountTypeEnum.DEBIT,
            access_token = "access-development-8ab976e6-64bc-4b38-98f7-731e7a349970"
        )

        self.credit_card_account = AccountType.objects.create(
            account_date_linked = datetime(2020, 10, 19,20,20,20),
            account_asset_type = AccountTypeEnum.CREDIT,
            access_token = "access-development-8ab976e6-64bc-4b38-98f7-731e7a349970"
        )

    def _assert_account_type_is_valid(self,account_type):
         try:
             account_type.full_clean()
         except(ValidationError):
             self.fail('Test invoice should be valid')

    def _assert_account_type_is_invalid(self,account_type):
         with self.assertRaises(ValidationError):
             account_type.full_clean()

    def _assert_account_type_using_plaid_api_is_invalid(self,account_type):
         with self.assertRaises(ValueError):
             account_type.full_clean()

    def test_accounts_are_valid(self):
        self._assert_account_type_is_valid(self.debit_card_account)
        self._assert_account_type_is_valid(self.credit_card_account)

    def test_debit_card_is_debit(self):
        self.assertTrue(is_debit(self.debit_card_account.account_asset_type))
