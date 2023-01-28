from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator

# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, first_name, last_name):
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    password = models.CharField(    
        max_length=520,     
        validators=[
            RegexValidator(   
                regex=r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$",
                message="Password must contain at least one uppercase character, one lowercase character and a number",
            )
        ],
    )
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    
