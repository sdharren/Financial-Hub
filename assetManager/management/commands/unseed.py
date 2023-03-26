from django.core.management.base import BaseCommand, CommandError
from assetManager.models import User,AccountType,AccountTypeEnum
from assetManager.API_wrappers import plaid_wrapper,crypto_wrapper,yfinance_wrapper

class Command(BaseCommand):
    #unseed the database with the custom user
    def handle(self, *args, **options):
        accounttypes = AccountType.objects.all()
        users = User.objects.all()

        for account_type in accounttypes:
            if account_type.user.email == 'johnnydoe@example.org':
                account_type.delete()

        for single_user in users:
            if single_user.email == 'johnnydoe@example.org':
                single_user.delete()
