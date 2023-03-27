from django.core.management.base import BaseCommand, CommandError
from assetManager.models import User,AccountType,AccountTypeEnum
from assetManager.API_wrappers import plaid_wrapper,crypto_wrapper,yfinance_wrapper
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.API_wrappers.crypto_wrapper import save_wallet_address

class Command(BaseCommand):
    def __init__(self):
        super().__init__()

    #seed the database with custom user to access the application
    def handle(self, *args, **options):
        users = User.objects.filter(email = 'johnnydoe@example.org')

        if(len(users) == 0):
            user = User.objects.create_user(
            email = 'johnnydoe@example.org',
            first_name = 'Johnny',
            last_name = 'Doe',
            password = 'Password123',
            )

            wrapper = SandboxWrapper()
            public_token = wrapper.create_public_token(bank_id='ins_115616', products_chosen=['investments','transactions'])
            wrapper.exchange_public_token(public_token)
            wrapper.save_access_token(user, ['investments','transactions'])

            second_public_token = wrapper.create_public_token(bank_id='ins_12', products_chosen=['investments','transactions'])
            wrapper.exchange_public_token(second_public_token)
            wrapper.save_access_token(user, ['transactions','investments'])
            #bitcoin
            save_wallet_address(user,"bc1qcw8ge4yr2xummxeey25y02g3v0nl4cdyhd095v")
            #euthereum
            save_wallet_address(user,"0x9696f59e4d72e237be84ffd425dcad154bf96976")


        else:
            return
