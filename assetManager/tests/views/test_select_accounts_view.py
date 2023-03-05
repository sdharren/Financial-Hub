from django.test import TestCase
from django.urls import reverse
from django.contrib import messages
from assetManager.models import User
import json

class SelectAccountViewsTestCase(TestCase):
    """Tests of the log in view."""
    fixtures = [
        'assetManager/tests/fixtures/users.json'
    ]

    def setUp(self):
        self.url = reverse('select_account')
        self.user = User.objects.get(email = 'johndoe@example.org')

    def test_balances_url(self):
        self.assertEqual(self.url,'/api/select_account/')

    def test_make_post_request_to_url(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.post(self.url, follow = True)

        redirect_url = reverse('home_page')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

        messages_list = list(response.context['messages'])
        self.assertEqual(str(messages_list[0]), 'POST query not permitted to this URL')
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_get_select_account_url_without_being_logged_in(self):
        response = self.client.post(self.url, follow = True)

        redirect_url = reverse('home_page')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')

        messages_list = list(response.context['messages'])
        self.assertEqual(str(messages_list[0]), 'Not Logged In')
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_get_select_account_url_succesfully(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url,{'param':'Royal Bank of Scotland - Current Accounts'}, follow=True)
        response_json = json.loads(response.content)
        response_data = response.json()

        self.assertEqual(len(list(response_data.keys())),2)
        self.assertEqual(response_data[list(response_data.keys())[0]], 500.0)
        self.assertEqual(response_data[list(response_data.keys())[1]], 500.0)

    def test_get_select_account_url_without_giving_param_field_a_value(self):
        self.client.login(email=self.user.email, password="Password123")
        with self.assertRaises(Exception) as cm:
            response = self.client.get(self.url,{'param':''}, follow=True)

        self.assertEqual(str(cm.exception),'No param field supplied to select_account url')

    def test_get_select_accounts_url_with_incorrect_key(self):
        self.client.login(email=self.user.email, password="Password123")
        with self.assertRaises(Exception) as cm:
            response = self.client.get(self.url,{'param':'HSBC (UK)'}, follow=True)

        self.assertEqual(str(cm.exception),'Provided institution name does not exist in the requested accounts')

    def test_reformat_correctand_incorrect(self):
        pass
