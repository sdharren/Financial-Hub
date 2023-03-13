from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.assets.debit_card import DebitCard
from django.test import TestCase
from assetManager.models import User, AccountType
from datetime import date
from assetManager.API_wrappers.plaid_wrapper import AccessTokenInvalid,PublicTokenNotExchanged
from unittest import skip
from django.core.exceptions import ObjectDoesNotExist
from assetManager.transactionInsight.bank_graph_data import BankGraphData
class DebitCardSandBoxWrapperTestCase(TestCase):
    fixtures = ['assetManager/tests/fixtures/users.json']
    #recursively checks that two dictionaries have the same structure and have the same value

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
        self.assertEqual(self.debit_card.plaid_wrapper.get_institution_name(self.debit_card.plaid_wrapper.ACCESS_TOKEN),'Royal Bank of Scotland - Current Accounts')

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

    def test_get_balances_for_multiple_access_tokens(self):
        user_lilly = User.objects.get(email='lillydoe@example.org')
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token_custom_user(bank_id='ins_115642', products_chosen=['transactions'], override_username="custom_sixth")
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(user_lilly, ['transactions'])

        plaid_wrapper_2 = SandboxWrapper()
        public_token_2 = plaid_wrapper_2.create_public_token_custom_user(bank_id='ins_1', products_chosen=['transactions'], override_username="custom_sixth")
        plaid_wrapper_2.exchange_public_token(public_token_2)
        plaid_wrapper_2.save_access_token(user_lilly, ['transactions'])

        debit_card_lilly = DebitCard(plaid_wrapper, user_lilly)

        self.assertEqual(len(debit_card_lilly.access_tokens),2)

        balances = debit_card_lilly.get_account_balances()
        same_balances = debit_card_lilly.get_account_balances()
        self.assertTrue(self.are_dicts_same(balances,same_balances))

        self.assertTrue(list(balances.keys())[0], 'Royal Bank of Scotland - Current Accounts')
        self.assertTrue(list(balances.keys())[1], 'Bank of America')

    def test_refresh_api_with_incorrect_access_token(self):
        self.debit_card.plaid_wrapper.ACCESS_TOKEN = 'wrongaccesstokenstring'
        with self.assertRaises(AccessTokenInvalid):
            self.debit_card.refresh_api(self.debit_card.plaid_wrapper.ACCESS_TOKEN)

    def test_get_transactions_with_incorrect_access_token(self):
        self.debit_card.access_tokens = ['wrongaccesstokenstring']
        with self.assertRaises(AccessTokenInvalid):
            start_date = date.fromisoformat('2022-12-16')
            end_date = date.fromisoformat('2022-12-19')
            transactions = self.debit_card.get_transactions_by_date(start_date,end_date)

    def test_get_transactions_with_one_and_multiple_access_token(self):
        user_lilly = User.objects.get(email='lillydoe@example.org')
        plaid_wrapper = SandboxWrapper()
        plaid_wrapper_2 = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token_custom_user()
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(user_lilly, ['transactions'])

        public_token_2 = plaid_wrapper_2.create_public_token_custom_user(bank_id='ins_1', products_chosen=['transactions'], override_username="custom_sixth")
        plaid_wrapper_2.exchange_public_token(public_token_2)
        plaid_wrapper_2.save_access_token(user_lilly, ['transactions'])

        debit_card_lilly = DebitCard(plaid_wrapper, user_lilly)

        self.assertEqual(len(debit_card_lilly.access_tokens),2)

        start_date = date.fromisoformat('2022-12-16')
        end_date = date.fromisoformat('2022-12-19')
        transactions = debit_card_lilly.get_transactions_by_date(start_date,end_date)

        self.assertEqual(len(transactions),2)
        self.assertEqual(len(transactions[0]),4)
        self.assertEqual(len(transactions[1]),4)

        self.assertFalse(self.are_dicts_same(transactions[0], transactions[1]))

        start_date = date.fromisoformat('2022-12-16')
        end_date = date.fromisoformat('2022-12-19')
        transactions = self.debit_card.get_transactions_by_date(start_date,end_date)
        self.assertEqual(len(transactions),1)
        self.assertEqual(len(transactions[0]),4)

        self.assertEqual(transactions[0][0]['amount'], 896.65)
        self.assertEqual(transactions[0][1]['amount'], 398.34)
        self.assertEqual(transactions[0][2]['amount'], 1708.12)
        self.assertEqual(transactions[0][3]['amount'], 1109.01)


    def test_get_non_existent_institution_name_from_db(self):
        access_tokens = 'wrongaccesstokenstring'
        institution_name = self.debit_card.get_institution_name_from_db(access_tokens)
        self.assertEqual(institution_name,None)

    def test_get_empty_insight_data_dict(self):
        self.assertEqual(self.debit_card.get_insight_data(), None)


    def test_make_transaction_data_insight_with_one_access_token(self):
        user = User.objects.get(email='lillydoe@example.org')
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token()
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(user, ['transactions'])
        debit_card = DebitCard(plaid_wrapper, user)

        start_date = date.fromisoformat('2022-06-13')
        end_date = date.fromisoformat('2022-12-16')
        debit_card.make_graph_transaction_data_insight(start_date,end_date)

        insights = debit_card.get_insight_data()
        self.assertTrue(insights is not None)
        self.assertEqual(list(insights.keys())[0],'Royal Bank of Scotland - Current Accounts')
        self.assertTrue(isinstance(insights['Royal Bank of Scotland - Current Accounts'], BankGraphData))
