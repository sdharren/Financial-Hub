from django.test import TestCase
from assetManager.models import UserManager

"""Tests for the UserManager BaseUserManager """

class UserManagerModelTestCase(TestCase):
    def setUp(self):
        self.email = 'johndoe@example.org'
        self.first_name = 'john'
        self.last_name = 'doe'
        self.password = 'Password123'

    def test_cannot_create_user_without_email(self):
        self.email = None
        self._assert_user_invalid()

    def test_cannot_create_user_without_password(self):
        self.password = None
        self._assert_user_invalid()

    def test_cannot_create_user_without_first_name(self):
        self.first_name = None
        self._assert_user_invalid()

    def test_cannot_create_user_without_last_name(self):
        self.last_name = None
        self._assert_user_invalid()


    def _assert_user_invalid(self):
        manager = UserManager()
        with self.assertRaises(ValueError):
            manager.create_user(self.email, self.password, self.first_name, self.last_name)
