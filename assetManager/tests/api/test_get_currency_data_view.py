from django.test import TestCase
from django.urls import reverse
from django.contrib import messages
from assetManager.models import User
import json
from assetManager.api.views import reformat_balances_into_currency,calculate_perentage_proportions_of_currency_data
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from django.conf import settings
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from django.core.cache import cache
from assetManager.assets.debit_card import DebitCard
from assetManager.models import User,AccountType,AccountTypeEnum

class GetCurrencyDataViewTestCase(TestCase):
    """Tests for the get_currency_data view."""
    fixtures = [
        'assetManager/tests/fixtures/users.json'
    ]

    def create_public_token(self):
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token_custom_user()
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(self.user, ['transactions'])

    def tearDown(self):
        cache.clear()

    def setUp(self):
        settings.PLAID_DEVELOPMENT = False
        self.url = reverse('currency_data')
        self.user = User.objects.get(email='johndoe@example.org')
        self.client = APIClient()
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.post('/api/token/', {'email': self.user.email, 'password': 'Password123'}, format='json')
        jwt = str(response.data['access'])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ jwt)


    def test_balances_url(self):
        self.assertEqual(self.url,'/api/currency_data/')

    def test_get_balances_data_without_jwt_not_logged_in(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_reformat_balances_into_currency_incorrect_param_type(self):
        incorrect_account_balances = ['account1', 'account2']
        with self.assertRaises(TypeError) as cm:
            reformat_balances_into_currency(incorrect_account_balances)

    def test_reformat_balances_into_currency_empty_dict(self):
        account_balances = {'Royal Bank of Scotland - Current Accounts':{}}
        self.assertEqual(reformat_balances_into_currency(account_balances),{})

    def test_get_currency_data_without_any_access_tokens_saved_with_development_wrapper(self):
        settings.PLAID_DEVELOPMENT = True
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 303)

        response_data = response.json()
        self.assertEqual(list(response_data.keys())[0],'error')
        self.assertEqual(response_data[list(response_data.keys())[0]],'Transactions Not Linked.')

    def test_get_currency_data_with_incorrectly_saved_token_causing_an_error(self):
        settings.PLAID_DEVELOPMENT = True
        AccountType.objects.create(
            user = self.user,
            account_asset_type = AccountTypeEnum.DEBIT,
            access_token = 'access-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349971',
            account_institution_name = 'HSBC',
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 303)

        response_data = response.json()
        self.assertEqual(list(response_data.keys())[0],'error')
        self.assertEqual(response_data[list(response_data.keys())[0]],'Something went wrong querying PLAID.')



    def test_get_reformatted_balances_into_currency_data_correctly_same_currency_usd(self):
        account_balances = {'Royal Bank of Scotland - Current Accounts': {'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}}}
        balances = reformat_balances_into_currency(account_balances)
        self.assertEqual(len(balances),1)
        self.assertEqual(list(balances.keys())[0], 'USD')
        self.assertEqual(balances[list(balances.keys())[0]], 593.8004402054293)


    def test_get_reformatted_balances_into_currency_data_correctly_same_currency_gbp(self):
        account_balances = {'Royal Bank of Scotland - Current Accounts': {'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'GBP'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'GBP'}}}
        balances = reformat_balances_into_currency(account_balances)
        self.assertEqual(len(balances),1)
        self.assertEqual(list(balances.keys())[0], 'GBP')
        self.assertEqual(balances[list(balances.keys())[0]], 1000)


    def test_get_reformatted_balances_into_currency_data_correctly_same_currency_eur(self):
        account_balances = {'Royal Bank of Scotland - Current Accounts': {'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'EUR'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'EUR'}}}
        balances = reformat_balances_into_currency(account_balances)
        self.assertEqual(len(balances),1)
        self.assertEqual(list(balances.keys())[0], 'EUR')
        self.assertEqual(balances[list(balances.keys())[0]], 809.35)

    def test_reformat_balances_into_currency_multiple_institutions_different_currencies(self):
        account_balances = {'Royal Bank of Scotland - Current Accounts': {'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}},'HSBC':{'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'EUR'}}}
        balances = reformat_balances_into_currency(account_balances)
        self.assertEqual(len(balances),2)
        self.assertEqual(list(balances.keys())[0], 'USD')
        self.assertEqual(list(balances.keys())[1], 'EUR')

        self.assertEqual(balances[list(balances.keys())[0]], 890.7006603081438)
        self.assertEqual(balances[list(balances.keys())[1]], 404.675)

    def test_get_reformatted_balances_data_today_is_different_from_2014_exchange_rates(self):
        account_balances = {'Royal Bank of Scotland - Current Accounts': {'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}},'HSBC':{'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'EUR'}}}
        balances = reformat_balances_into_currency(account_balances)

        self.assertEqual(len(balances),2)
        self.assertEqual(list(balances.keys())[0], 'USD')
        self.assertEqual(list(balances.keys())[1], 'EUR')

        self.assertEqual(balances[list(balances.keys())[0]], 890.7006603081438)
        self.assertEqual(balances[list(balances.keys())[1]], 404.675)

        settings.PLAID_DEVELOPMENT = True
        new_balances = reformat_balances_into_currency(account_balances)
        self.assertEqual(len(new_balances),2)
        self.assertEqual(list(new_balances.keys())[0], 'USD')
        self.assertEqual(list(new_balances.keys())[1], 'EUR')

        self.assertTrue(new_balances['EUR'] != balances['EUR'])
        self.assertTrue(new_balances['USD'] != balances['USD'])



    def test_calculate_percentage_proportions_from_returned_reformatted_account_balances_data(self):
        currency_total = {'USD': 890.7006603081438, 'EUR': 404.675}
        balances = calculate_perentage_proportions_of_currency_data(currency_total)
        self.assertEqual(len(balances),2)
        self.assertEqual(list(balances.keys())[0], 'USD')
        self.assertEqual(list(balances.keys())[1], 'EUR')

        self.assertEqual(balances['USD'], round((890.7006603081438/(890.7006603081438 + 404.675))*100,2))
        self.assertEqual(balances['EUR'], round((404.675/(890.7006603081438 + 404.675))*100,2))

    def test_get_reformatted_balances_data_and_apply_calculate_perentage_proportions_of_currency_data(self):
        account_balances = {'Royal Bank of Scotland - Current Accounts': {'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'GBP'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}},'HSBC':{'JP4gb79D1RUbW96a98qVc5w1JDxPNjIo7xRkx': {'name': 'Checking', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'USD'}, 'k1xZm8kWJjCnRqmjqGgrt96VaexNzGczPaZoA': {'name': 'Savings', 'available_amount': 500.0, 'current_amount': 500.0, 'type': 'depository', 'currency': 'EUR'}}}
        balances = reformat_balances_into_currency(account_balances)

        self.assertEqual(len(balances),3)
        self.assertEqual(list(balances.keys())[0], 'GBP')
        self.assertEqual(list(balances.keys())[1], 'USD')
        self.assertEqual(list(balances.keys())[2], 'EUR')

        self.assertEqual(balances['GBP'],500)
        self.assertEqual(balances['USD'],593.8004402054293)
        self.assertEqual(balances['EUR'], 404.675)


        percentages = calculate_perentage_proportions_of_currency_data(balances)
        self.assertEqual(len(percentages),3)
        self.assertEqual(list(percentages.keys())[0], 'GBP')
        self.assertEqual(list(percentages.keys())[1], 'USD')
        self.assertEqual(list(percentages.keys())[2], 'EUR')

        self.assertEqual(percentages['GBP'],round(500/(500 + 593.8004402054293 +404.675 )*100,2))
        self.assertEqual(percentages['USD'],round(593.8004402054293/(500 + 593.8004402054293 +404.675 )*100,2))
        self.assertEqual(percentages['EUR'],round(404.675/(500 + 593.8004402054293 +404.675)*100,2))


    def test_make_post_request_to_url(self):
        response = self.client.post(self.url, follow = True)
        self.assertEqual(response.status_code,405)

    def test_get_currenccy_succesfully_with_no_existing_cache(self):
        self.create_public_token()
        response = self.client.get(self.url, follow=True)
        response_json = json.loads(response.content)
        response_data = response.json()
        self.assertEqual(list(response_data.keys())[0], "USD")
        self.assertEqual(response_data['USD'], 100)
        self.assertEqual(response.status_code,200)

    def test_get_currenccy_succesfully_with_existing_cache(self):
        self.create_public_token()
        response = self.client.get(self.url, follow=True)
        response_2 = self.client.get(self.url, follow=True)
        response_json = response_2.json()
        self.assertEqual(list(response_json.keys())[0], "USD")
        self.assertEqual(response_json['USD'], 100)
        self.assertEqual(response_2.status_code,200)

    def test_get_currencies_for_multiple_institution(self):
        before_count = len(AccountType.objects.filter(user = self.user, account_asset_type = AccountTypeEnum.DEBIT))
        self.create_public_token()
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token(bank_id='ins_1', products_chosen=['transactions'])
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(self.user, ['transactions'])
        debit_card = DebitCard(plaid_wrapper, self.user)
        response = self.client.get(self.url, follow=True)
        after_count = len(AccountType.objects.filter(user = self.user, account_asset_type = AccountTypeEnum.DEBIT))
        self.assertEqual(after_count, before_count + 2)
        response_data = response.json()
        self.assertEqual(list(response_data.keys())[0], "USD")
        self.assertEqual(response_data['USD'], 100)
        self.assertEqual(response.status_code,200)
