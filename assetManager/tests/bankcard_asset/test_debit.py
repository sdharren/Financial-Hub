from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.assets.debit_card import DebitCard
from django.test import TestCase
from assetManager.models import User, AccountType
from datetime import date
from assetManager.API_wrappers.plaid_wrapper import AccessTokenInvalid,PublicTokenNotExchanged

class DebitCardSandBoxWrapperTestCase(TestCase):
    fixtures = ['assetManager/tests/fixtures/users.json']
    #recursively checks that two dictionaries have the same structure and have the same values
    def are_dicts_same(self,dict1, dict2):
        if isinstance(dict1, dict) and isinstance(dict2, dict):
            if len(dict1) != len(dict2):
                return False
            for key in dict1:
                if key not in dict2 or not self.are_dicts_same(dict1[key], dict2[key]):
                    return False
            return True
        else:
            return dict1 == dict2

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.org')
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token_custom_user()
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(self.user, ['transactions'])
        self.debit_card = DebitCard(plaid_wrapper, self.user)

    def test_debit_card_set_up_correctly(self):
        self.assertTrue(self.debit_card.plaid_wrapper.ACCESS_TOKEN is not None)
        self.assertEqual(self.debit_card.plaid_wrapper.SANDBOX_KEY, '3c1540e977fb113fe9bdbb12bf61fd')
        self.assertTrue(self.debit_card.plaid_wrapper.client is not None)
        self.assertEqual(self.debit_card.plaid_wrapper.CLIENT_ID, '63d288b343e6370012e5be86')
        self.assertEqual(self.debit_card.plaid_wrapper.retrieve_access_tokens(self.user,'transactions')[0], self.debit_card.access_tokens[0])
        identity = self.debit_card.plaid_wrapper.get_identity()
        self.assertEqual(identity['names'][0],'John Smith')
        self.assertEqual(self.user.email, self.debit_card.user.email)
        accounts = AccountType.objects.filter(user = self.user)
        self.assertEqual(len(accounts),1)


    def test_correct_instution_for_access_token(self):
        self.assertEqual(self.debit_card.plaid_wrapper.get_institution_name(),'Royal Bank of Scotland - Current Accounts')

    def test_get_balances_with_incorrect_access_token(self):
        self.debit_card.access_tokens = ['wrongaccesstokenstring']
        with self.assertRaises(AccessTokenInvalid):
            self.debit_card.get_account_balances()

    def test_get_balances_for_custom_user_one_access_token(self):
        accounts = self.debit_card.get_account_balances()
        same_accounts = self.debit_card.get_account_balances()
        self.assertTrue(self.are_dicts_same(accounts,same_accounts))
        self.assertEqual(len(list(accounts.keys())),1)
        self.assertEqual(list(accounts.keys())[0], 'Royal Bank of Scotland - Current Accounts')
        self.assertEqual(len(list(accounts[list(accounts.keys())[0]].keys())), 2)

    def test_get_balances_for_custom_user_one_access_token_different_amounts(self):
        accounts = self.debit_card.get_account_balances()
        same_accounts = self.debit_card.get_account_balances()
        account_ids = list(same_accounts['Royal Bank of Scotland - Current Accounts'].keys())
        same_accounts['Royal Bank of Scotland - Current Accounts'][account_ids[0]]['available_amount'] = 0
        same_accounts['Royal Bank of Scotland - Current Accounts'][account_ids[0]]['currency'] = 'GBP'
        self.assertFalse(self.are_dicts_same(accounts,same_accounts))

    def test_refresh_api_with_incorrect_access_token(self):
        self.debit_card.plaid_wrapper.ACCESS_TOKEN = 'wrongaccesstokenstring'
        with self.assertRaises(AccessTokenInvalid):
            self.debit_card.refresh_api()

    def test_get_transactions(self):
        pass
        #start_date = date.fromisoformat('2022-09-01') #change dates to within two years
        #end_date = date.fromisoformat('2022-09-03')
        #self.debit_card.get_transactions(start_date,end_date)

        #self.debit_card.get_institution_name_from_db()
        #self.debit_card.get_account_balances()
