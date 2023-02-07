from django.test import TestCase
from django.urls import reverse
from django.contrib import messages
from assetManager.forms import LogInForm
from assetManager.models import User
from assetManager.tests.helpers import LogInTester


class LogInViewTestCase(TestCase, LogInTester):
    """Tests of the log in view."""
    fixtures = [
        'assetManager/tests/fixtures/users.json'
    ]

    def setUp(self):
        self.url = reverse('log_in')

    def test_log_in_url(self):
        self.assertEqual(self.url,'/log_in/')

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_unsuccessful_log_in(self):
        form_input = {'email': 'johndoe@example.org', 'password': 'WrongPassword123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_successful_log_in(self):
        form_input = {'email': 'johndoe@example.org', 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('home_page')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')