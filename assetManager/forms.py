from django import forms
from assetManager.models import User
from django.core.validators import RegexValidator

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
    password = forms.CharField(
        validators=[
            RegexValidator(
                regex=r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$",
                message="Password must contain at least one uppercase character, one lowercase character and a number",
            )
        ],
        label='Password',
        widget=forms.PasswordInput(),
    )
    password_confirmation = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput(),
    )

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            self.add_error(
                'password_confirmation', 'Password does not match password confirmation'
            )

    def save(self):
        super().save(commit=False)
        user = User.objects.create_user(
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password'),
        )
        return user

class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
