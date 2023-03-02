from django.test import TestCase
from django.urls import reverse
from django.contrib import messages
from assetManager.models import User
import json

class GetBalancesDataViewTestCase(TestCase):
    """Tests of the log in view."""
    fixtures = [
        'assetManager/tests/fixtures/users.json'
    ]

    def setUp(self):
        self.url = reverse('get_balances_data')
        self.user = User.objects.get(email = 'johndoe@example.org')

    def test_balances_url(self):
        self.assertEqual(self.url,'/api/balances/')

    def test_make_post_request_to_url(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.post(self.url, follow = True)

        redirect_url = reverse('home_page')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')

        messages_list = list(response.context['messages'])
        self.assertEqual(str(messages_list[0]), 'POST query not permitted to this URL')
        self.assertEqual(messages_list[0].level, messages.ERROR)


    def test_get_balances_succesfully(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        response_json = json.loads(response.content)
        response_data = response.json()
        self.assertEqual(response_data['Royal Bank of Scotland - Current Accounts'], 1000.0)

    def test_get_balances_succesfully_for_multiple_accounts(self):
        pass
