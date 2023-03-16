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
from assetManager.api.views import monthlyGraph

from assetManager.tests.helpers import LogInTester

class LogInViewTestCase(TestCase, LogInTester):
    """Tests of the views for transactions bar graph."""

    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('sign_up')
        self.user = User.objects.create_user(
            first_name = 'Jane',
            last_name = 'Doe',
            email='janedoe@example.org',
            password='Password123'
        )

     def test_monthly_graph_with_param(self):
         request = self.factory.get('/monthly-graph/?param=2022')
         force_authenticate(request, user=self.user)
         response = monthlyGraph(request)
         self.assertEqual(response.status_code, 200)
         self.assertEqual(response['Content-Type'], 'application/json')
