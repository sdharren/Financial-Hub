from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import re
# Create your models here.
#test comment to associate commit on team feedback
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

    #write tests for this
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        first_name = extra_fields.get('first_name')
        last_name = extra_fields.get('last_name')

        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, is_superuser = extra_fields.get('is_superuser'),is_staff = extra_fields.get('is_staff'))
        user.set_password(password)
        user.save(using=self._db)
        return user

#minimum length instead of maximum length
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


"""
Enum Type to represent the different types of account that are available in our application : Debit, Credit, Stock and Crypto accounts
"""
class AccountTypeEnum(models.TextChoices):
    DEBIT = 'transactions', _('Debit Card'),
    STOCK = 'investments', _('Brokerage or Investement Account'),
    CRYPTO = 'CRYPTO',_('Crypto Wallet')

#shoud be in modelhelpers .py
# btw augosto i made a file called helpers.py in assetManager folder so could put it there
def is_debit(account_string):
    return AccountTypeEnum.DEBIT.value == account_string

def is_stock(account_string):
    return AccountTypeEnum.STOCK.value == account_string

def is_crypto(account_string):
    return AccountTypeEnum.CRYPTO.value == account_string

def check_access_token(access_token):
    if(re.match(r"^access-development-[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$",access_token) is None and re.match(r"^access-sandbox-[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$",access_token) is None):
        raise ValueError("PLAID API access token format is invalid")


class AccountTypeModelManager(models.Manager):
    def create(self, **obj_data):
        account_type = obj_data['account_asset_type']
        if is_crypto(account_type) is False:
            access_token = obj_data['access_token']
            check_access_token(access_token)

        # Now call the super method which does the actual creation
        return super().create(**obj_data) # Python 3 syntax!!
"""
The AccountType model refers to the single type of account that a user may have
Displays information related to the Account type, the date the account was linked on the financial-hub application, and the access token required to query the relevant API for that account
"""
class AccountType(models.Model):
    class Meta:
        unique_together = (('access_token','user', 'account_asset_type'),)


    account_type_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'client')
    account_date_linked = models.DateField('Account Linked Date', default=timezone.now)

    account_asset_type = models.CharField(
        max_length = 35,
        choices = AccountTypeEnum.choices,
        blank = True
    )

    access_token = models.CharField(
        max_length=250,
        blank=False,
    )

    account_institution_name = models.CharField(blank = False, max_length = 100)
    objects = AccountTypeModelManager()

    def save(self, *args, **kwargs):
        if is_crypto(self.account_asset_type) is False:
            check_access_token(self.access_token)

        super(AccountType, self).save(*args, **kwargs)
