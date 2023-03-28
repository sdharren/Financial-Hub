from django.test import TestCase
from assetManager.models import User
from django.core.exceptions import ValidationError

"""Tests for the User model """
class UserModelTestCase(TestCase):
    fixtures = ['assetManager/tests/fixtures/users.json']
    def setUp(self):
        self.user = User.objects.get(email = 'johndoe@example.org')

    def test_first_name_cannot_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_need_not_be_unique(self):
        second_user = self._create_second_user()
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid()

    def test_first_name_may_contain_50_characters(self):
        self.user.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_first_name_must_not_contain_more_than_50_characters(self):
        self.user.first_name = 'x' * 51
        self._assert_user_is_invalid()

    def test_last_name_cannot_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_need_not_be_unique(self):
        second_user = self._create_second_user()
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid()

    def test_last_name_may_contain_50_characters(self):
        self.user.last_name = 'x' * 50
        self._assert_user_is_valid()

    def test_last_name_must_not_contain_more_than_50_characters(self):
        self.user.last_name = 'x' * 51
        self._assert_user_is_invalid()

    def test_email_must_not_be_blank(self):
        self.user.email = ''
        self._assert_user_is_invalid()

    def test_email_must_be_unique(self):
        second_user = self._create_second_user()
        self.user.email = second_user.email
        self._assert_user_is_invalid()

    def test_email_must_contain_first_part(self):
        self.user.email = '@example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.user.email = 'johndoe.example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.user.email = 'johndoe@.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.user.email = 'johndoe@example'
        self._assert_user_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        self.user.email = 'johndoe@@example.org'
        self._assert_user_is_invalid()

    def test_password_must_contain_one_upper_case_character(self):
        self.user.password = 'password123'
        self._assert_user_is_invalid()

    def test_password_must_contain_one_lower_case_character(self):
        self.user.password = 'PASSWORD123'
        self._assert_user_is_invalid()

    def test_password_must_contain_a_number(self):
        self.user.password = 'Password'
        self._assert_user_is_invalid()

    def test_password_cannot_be_longer_than_520_characters(self):
        self.user.password = 'Password123' * 50
        self._assert_user_is_invalid()


    def test_valid_user(self):
        self._assert_user_is_valid()

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def _create_second_user(self):
        user = User.objects.create_user(
            first_name='Jane',
            last_name='Doe',
            email='janedoe@example.org',
            password='Password123',
        )
        return user

    def test_super_user_is_valid(self):
        try:
            super_user = User.objects.create_superuser(
                email = "mikedoe@gmail.com",
                first_name = "Mike",
                last_name = "Doe",
                password = "Password123"
            )
            super_user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def test_super_user_super_user_flag_must_be_true(self):
        with self.assertRaises(ValueError):
            super_user = User.objects.create_superuser(
                email = "mikedoe@gmail.com",
                first_name = "Mike",
                last_name = "Doe",
                password = "Password123",
                is_superuser = False
            )

    def test_super_user_staff_flag_must_be_true(self):
        with self.assertRaises(ValueError):
            super_user = User.objects.create_superuser(
                email = "mikedoe@gmail.com",
                first_name = "Mike",
                last_name = "Doe",
                password = "Password123",
                is_staff = False
            )


    def test_super_user_super_must_have_name(self):
        with self.assertRaises(ValueError):
            super_user = User.objects.create_superuser(
                email = "mikedoe@gmail.com",
                last_name = "Doe",
                password = "Password123",
            )

    def test_super_user_super_must_have_last_name(self):
        with self.assertRaises(ValueError):
            super_user = User.objects.create_superuser(
                email = "mikedoe@gmail.com",
                first_name = "Mike",
                password = "Password123",
            )

    def test_super_user_super_must_have_valid_email(self):
        with self.assertRaises(ValueError):
            super_user = User.objects.create_superuser(
                email = "",
                first_name = "Mike",
                last_name = "Doe",
                password = "Password123",
            )

    def test_super_user_must_have_valid_password(self):
        with self.assertRaises(ValueError):
            super_user = User.objects.create_superuser(
                email = "mikedoe@gmail.com",
                first_name = "Mike",
                last_name = "Doe",
                password = "",
            )
