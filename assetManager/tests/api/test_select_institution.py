import json
from django.test import TestCase, RequestFactory
from django.urls import reverse
from assetManager.tests.helpers import LogInTester
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from assetManager.models import User
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from rest_framework.exceptions import ErrorDetail
from assetManager.api.views import set_bank_access_token, select_bank_account
from assetManager.api.views_helpers import *
from django.contrib.auth import get_user_model
from django.core.cache import cache
from assetManager.transactionInsight.bank_graph_data import BankGraphData
from django.conf import settings
from assetManager.tests.helpers import LogInTester

class CacheTransactionsViewTestCase(TestCase, LogInTester):
    """Tests of the views for dropdown menu."""

    def setUp(self):
        settings.PLAID_DEVELOPMENT = False
        self.factory = RequestFactory()
        User = get_user_model()
        users = User.objects.all()
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.org',
            'password': 'Password123',
            'password_confirmation':
            'Password123'
        }
        self.url = reverse('sign_up')
        self.client.post(self.url, self.form_input, follow=True)
        self.user = User.objects.get(email='janedoe@example.org')
        self.request_factory = RequestFactory()

    def tearDown(self):
        cache.clear()

    # def test_set_bank_access_token_with_valid_body(self):
    #     request = self.request_factory.post('/api/set_bank_access_token/', data=json.dumps({'selectedOption': '123'}), content_type='application/json')
    #     force_authenticate(request, user=self.user)
    #     response = set_bank_access_token(request)
    #     self.assertEqual(200,response)
    #     self.assertEqual(cache.get('access_token'+self.user.email),'123')
