from django.test import TestCase
from assetManager.forms import SignUpForm
from django import forms
from assetManager.models import User


class SignUpFormTestCase(TestCase):
    #Data for tests
    def setUp(self):
        self.form_input = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'Password123',
            'password_confirmation': 'Password123',
        }
 
    def test_valid_sign_up_form(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid)

    #Form has necessary fields
    def test_form_has_valid_fields(self):
        form = SignUpForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('password', form.fields)
        self.assertIn('password_confirmation', form.fields)
        password_field = form.fields['password'].widget
        self.assertTrue(isinstance(password_field, forms.PasswordInput))

    def test_form_uses_model_validation(self):
        self.form_input['email'] = 'bademail'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    #Password had correct format
    def test_password_must_have_capital_letter(self):
        self.form_input['password'] = 'badpassword'
        self.form_input['password_confirmation'] = 'badpassword'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_password_must_contain_lowercase_character(self):
        self.form_input['password'] = 'PASSWORD123'
        self.form_input['password_confirmation'] = 'PASSWORD123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['password'] = 'PasswordABC'
        self.form_input['password_confirmation'] = 'PasswordABC'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_match_password_confirmation(self):
        self.form_input['password_confirmation'] = 'incorrectpassword'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_correct_form_creates_new_user(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        user_count_before = User.objects.all().count()
        form.save()
        user_count_after = User.objects.all().count()
        self.assertEquals(user_count_before + 1, user_count_after)