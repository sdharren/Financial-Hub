import re
from django.test import TestCase
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper, IncorrectInstitutionId,IncorrectProduct
from assetManager.API_wrappers.plaid_wrapper import PublicTokenNotExchanged, LinkTokenNotCreated,AccessTokenInvalid
from assetManager.models import User, AccountType, AccountTypeEnum
from django.db import IntegrityError, transaction

"""Tests of the PLAID sandbox wrapper class."""

class SandboxWrapperTestCase(TestCase):
    fixtures = ['assetManager/tests/fixtures/users.json']

    def setUp(self):
        self.wrapper = SandboxWrapper()
        self.user = User.objects.get(email='johndoe@example.org')

    def compare_accounts_dict(self,dict1, dict2):
        self.assertEqual(len(dict1), len(dict2))
        self.assertEqual(dict1[0]['account_id'], dict2[0]['account_id'])
        self.assertEqual(dict1[1]['account_id'], dict2[1]['account_id'])

        self.assertEqual(dict1[0]['mask'], dict2[0]['mask'])
        self.assertEqual(dict1[1]['mask'], dict2[1]['mask'])

        self.assertEqual(dict1[0]['official_name'], dict2[0]['official_name'])
        self.assertEqual(dict1[1]['official_name'], dict2[1]['official_name'])

        self.assertEqual(dict1[0]['type'], dict2[0]['type'])
        self.assertEqual(dict1[1]['type'], dict2[1]['type'])

    def compare_items_dict(self,dict1,dict2):
        self.assertEqual(dict1['item_id'], dict2['item_id'])
        self.assertEqual(dict1['products'][0], dict2['products'][0])


    def test_sandbox_initialised_correctly(self):
        self.assertEqual(self.wrapper.CLIENT_ID, '63d288b343e6370012e5be86')
        self.assertEqual(self.wrapper.ACCESS_TOKEN, None)
        self.assertEqual(self.wrapper.ITEM_ID, None)
        self.assertEqual(self.wrapper.LINK_TOKEN, None)
        self.assertTrue(self.wrapper.PUBLIC_TOKEN is None)
        self.assertEqual(self.wrapper.SANDBOX_KEY, '3c1540e977fb113fe9bdbb12bf61fd')
        self.assertTrue(self.wrapper.client is not None)

    def test_create_link_token_with_incorrect_instituionId_parameters(self):
        with self.assertRaises(IncorrectInstitutionId) as cm:
            self.wrapper.create_public_token(bank_id = 'incorrectid', products_chosen = ['transactions'])

        self.assertEqual(str(cm.exception.message),'Non Existing InstituionId Provided')

    def test_create_link_token_with_incorrect_product_parameters(self):
        with self.assertRaises(IncorrectProduct) as cm:
            self.wrapper.create_public_token(bank_id = 'ins_115642', products_chosen = ['incorrectproduct'])

        self.assertEqual(str(cm.exception.message),'Non Valid Products Provided')

    def test_create_sandbox_public_token_successfully(self):
        public_token = self.wrapper.create_public_token()
        regex_match = re.match(r"^public-sandbox-[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$", public_token)
        self.assertIsNotNone(regex_match)

    def test_get_identity_with_no_access_token(self):
        with self.assertRaises(PublicTokenNotExchanged):
            self.wrapper.get_identity()

    def test_get_identity_with_incorrect_access_token(self):
        self.wrapper.ACCESS_TOKEN = 'access-development-999f84d1-aa93-4fd9-90f0-6af8867a4f12'
        with self.assertRaises(AccessTokenInvalid):
            self.wrapper.get_identity()

    def test_create_link_custom_token_with_incorrect_instituionId_parameters(self):
        with self.assertRaises(IncorrectInstitutionId) as cm:
            self.wrapper.create_public_token_custom_user(bank_id = 'incorrectid', products_chosen = ['transactions'],override_username="custom_sixth")

        self.assertEqual(str(cm.exception.message),'Non Existing InstituionId Provided')

    def test_create_custom_link_token_with_incorrect_product_parameters(self):
        with self.assertRaises(IncorrectProduct) as cm:
            self.wrapper.create_public_token_custom_user(bank_id = 'ins_115642', products_chosen = ['incorrectproduct'],override_username="custom_sixth")

        self.assertEqual(str(cm.exception.message),'Non Valid Products Provided')


    def test_create_link_token_with_non_existing_dashboard_account_username(self):
        public_token = self.wrapper.create_public_token_custom_user(bank_id = 'ins_115642', products_chosen = ['transactions'],override_username="nonExistingNaMe")
        access_token = self.wrapper.exchange_public_token(public_token)
        identity = self.wrapper.get_identity()
        self.assertNotEqual(identity['names'][0],'John Smith')

    def test_create_custom_sandbox_public_token_with_existing_dashboard_account_username(self):
        public_token = self.wrapper.create_public_token_custom_user(bank_id = 'ins_115642', products_chosen = ['transactions'],override_username="custom_sixth")
        access_token = self.wrapper.exchange_public_token(public_token)
        identity = self.wrapper.get_identity()
        self.assertEqual(identity['names'][0],'John Smith')


    """
    Below tests are for the testing the super class PlaidWrapper within the sandbox Environment since a client is not defined to PlaidWrapper
    """
    def test_wrapper_saves_correct_access_token(self):
        public_token = self.wrapper.create_public_token_custom_user(bank_id = 'ins_115642', products_chosen = ['transactions'],override_username="custom_sixth")
        self.wrapper.exchange_public_token(public_token)
        access_token = self.wrapper.get_access_token()
        self.wrapper.save_access_token(self.user, ['transactions'])
        account_type = AccountType.objects.get(user=self.user)
        self.assertEqual(account_type.access_token, access_token)
        self.assertEqual(account_type.account_asset_type, 'transactions')
        self.assertEqual(account_type.account_institution_name, "Royal Bank of Scotland - Current Accounts")

    def test_wrapper_saves_correct_access_token_for_several_products(self):
        public_token = self.wrapper.create_public_token_custom_user(bank_id = 'ins_115616', products_chosen = ['transactions', 'investments'],override_username="custom_sixth")
        self.wrapper.exchange_public_token(public_token)
        account_count_before = AccountType.objects.all().count()
        self.wrapper.save_access_token(self.user, ['transactions', 'investments'])
        access_token = self.wrapper.get_access_token()

        account_count_after = AccountType.objects.all().count()
        self.assertEqual(account_count_before + 2, account_count_after)
        all_account_types = AccountType.objects.all()
        for account in all_account_types:
            self.assertEqual(account.access_token, access_token)
            self.assertEqual(account.account_institution_name,"Vanguard")
            self.assertTrue(account.account_asset_type == AccountTypeEnum.STOCK or account.account_asset_type == AccountTypeEnum.DEBIT)

    def test_get_accounts_with_incorrect_access_token(self):
        self.wrapper.ACCESS_TOKEN = 'access-development-999f84d1-aa93-4fd9-90f0-6af8867a4f12'
        with self.assertRaises(AccessTokenInvalid):
            self.wrapper.get_accounts(self.wrapper.ACCESS_TOKEN)

    def test_get_accounts_with_correct_access_token(self):
        public_token = self.wrapper.create_public_token_custom_user(bank_id = 'ins_115642', products_chosen = ['transactions'],override_username="custom_sixth")
        self.wrapper.exchange_public_token(public_token)
        accounts = self.wrapper.get_accounts(self.wrapper.ACCESS_TOKEN)
        same_accounts = self.wrapper.get_accounts(self.wrapper.ACCESS_TOKEN)
        self.compare_accounts_dict(accounts,same_accounts)

    def test_get_item_with_incorrect_access_token(self):
        self.wrapper.ACCESS_TOKEN = 'access-development-999f84d1-aa93-4fd9-90f0-6af8867a4f12'
        with self.assertRaises(AccessTokenInvalid):
            self.wrapper.get_item(self.wrapper.ACCESS_TOKEN)

    def test_get_item_with_correct_access_token(self):
        public_token = self.wrapper.create_public_token_custom_user(bank_id = 'ins_115616', products_chosen = ['transactions'])
        self.wrapper.exchange_public_token(public_token)
        item = self.wrapper.get_item(self.wrapper.ACCESS_TOKEN)
        same_item = self.wrapper.get_item(self.wrapper.ACCESS_TOKEN)
        self.compare_items_dict(item,same_item)

    def test_get_insitution_id_with_incorrect_access_token(self):
        self.wrapper.ACCESS_TOKEN = 'access-development-999f84d1-aa93-4fd9-90f0-6af8867a4f12'
        with self.assertRaises(AccessTokenInvalid):
            self.wrapper.get_institution_id(self.wrapper.ACCESS_TOKEN)

    def test_get_correct_institution_id(self):
        public_token = self.wrapper.create_public_token_custom_user(bank_id = 'ins_115616', products_chosen = ['transactions'])
        self.wrapper.exchange_public_token(public_token)
        institution_id = self.wrapper.get_institution_id(self.wrapper.ACCESS_TOKEN)
        self.assertEqual(institution_id,'ins_115616')

    def test_get_correct_institution_id_different_bank(self):
        public_token = self.wrapper.create_public_token_custom_user(bank_id = 'ins_1', products_chosen = ['transactions'])
        self.wrapper.exchange_public_token(public_token)
        institution_id = self.wrapper.get_institution_id(self.wrapper.ACCESS_TOKEN)
        self.assertEqual(institution_id,'ins_1')

    def test_get_instituion_name_with_incorrect_access_token(self):
        self.wrapper.ACCESS_TOKEN = 'access-development-999f84d1-aa93-4fd9-90f0-6af8867a4f12'
        with self.assertRaises(AccessTokenInvalid):
            self.wrapper.get_institution_name(self.wrapper.ACCESS_TOKEN)

    def test_get_correct_institution_name(self):
        public_token = self.wrapper.create_public_token_custom_user(bank_id = 'ins_115616', products_chosen = ['transactions'])
        self.wrapper.exchange_public_token(public_token)
        institution_name = self.wrapper.get_institution_name(self.wrapper.ACCESS_TOKEN)
        self.assertEqual(institution_name,'Vanguard')

    def test_get_correct_institution_name_with_differnt_id(self):
        public_token = self.wrapper.create_public_token_custom_user(bank_id = 'ins_1', products_chosen = ['transactions'])
        self.wrapper.exchange_public_token(public_token)
        institution_name = self.wrapper.get_institution_name(self.wrapper.ACCESS_TOKEN)
        self.assertEqual(institution_name,'Bank of America')

    def test_get_tem_id_correctly(self):
        public_token = self.wrapper.create_public_token_custom_user(bank_id = 'ins_115616', products_chosen = ['transactions'])
        self.wrapper.exchange_public_token(public_token)
        self.assertTrue(self.wrapper.get_item_id() != None)


    def test_force_intergrity_error_in_database(self):

        public_token = self.wrapper.create_public_token_custom_user(bank_id = 'ins_115616', products_chosen = ['transactions'])
        self.wrapper.exchange_public_token(public_token)

        access_token = self.wrapper.get_access_token()

        before_count = AccountType.objects.count()
        self.wrapper.save_access_token(self.user, ['transactions'])
        after_count = AccountType.objects.count()

        self.assertEqual(before_count + 1,after_count)

        with transaction.atomic():
            self.wrapper.save_access_token(self.user, ['transactions'])

        new_count = AccountType.objects.count()

        self.assertEqual(new_count,after_count)
