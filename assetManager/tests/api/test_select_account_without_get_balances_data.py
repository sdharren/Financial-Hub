from django.test import TestCase
from django.urls import reverse
from django.contrib import messages
from assetManager.models import User
import json
from assetManager.api.views import reformatAccountBalancesData,delete_balances_cache
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from django.conf import settings
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper



class SelectAccountViewsWithoutGettingBalanceTestCase(TestCase):
    """Tests of the log in view."""
    fixtures = [
        'assetManager/tests/fixtures/users.json'
    ]

    def setUp(self):
        self.url = reverse('select_account')
        self.user = User.objects.get(email='johndoe@example.org')
        self.client = APIClient()
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.post('/api/token/', {'email': self.user.email, 'password': 'Password123'}, format='json')
        jwt = str(response.data['access'])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ jwt)

    def test_get_select_account_without_first_querying_get_balances_data(self):
        delete_balances_cache(self.user)
        with self.assertRaises(Exception) as cm:
            response = self.client.get(self.url,{'param':'Royal Bank of Scotland - Current Accounts'}, follow=True)

        self.assertEqual(str(cm.exception),'get_balances_data was not queried')
