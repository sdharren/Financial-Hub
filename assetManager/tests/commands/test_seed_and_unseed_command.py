from django.core.management import call_command
from django.test import TestCase
from assetManager.models import User,AccountType,AccountTypeEnum
from django.conf import settings

"""Tests for the seed and unseed commands for SANDBOX LOCAL ENVIRONMENT"""
class SeedAndUnseedCommandTestCase(TestCase):
    def setUp(self):
        settings.PLAID_DEVELOPMENT = False

    def test_seed_command_twice(self):
        accounttypes = AccountType.objects.all()
        users = User.objects.all()

        before_account_types_count = AccountType.objects.count()
        before_user_count = User.objects.count()

        for account_type in accounttypes:
            self.assertTrue(account_type.user.email != 'johnnydoe@example.org')

        for single_user in users:
            self.assertTrue(single_user.email != 'johnnydoe@example.org')

        call_command('seed')
        call_command('seed')

        after_account_types_count = AccountType.objects.count()
        after_user_count = User.objects.count()

        self.assertEqual(before_user_count + 1, after_user_count)
        self.assertEqual(before_account_types_count + 7, after_account_types_count)

        user_john = User.objects.get(email = 'johnnydoe@example.org')

        bank_assets = AccountType.objects.filter(user = user_john, account_asset_type = AccountTypeEnum.DEBIT)
        investment_assets = AccountType.objects.filter(user = user_john, account_asset_type = AccountTypeEnum.STOCK)
        crypto_assets = AccountType.objects.filter(user = user_john, account_asset_type = AccountTypeEnum.CRYPTO)

        for bank in bank_assets:
            self.assertTrue(bank.account_institution_name == 'Vanguard' or bank.account_institution_name == 'Fidelity' or bank.account_institution_name == 'Royal Bank of Scotland - Current Accounts')

        for investment in investment_assets:
            self.assertTrue(investment.account_institution_name == 'Vanguard' or investment.account_institution_name == 'Fidelity')

        for crypto in crypto_assets:
            self.assertTrue(crypto.access_token == "1AV4KGCsvtPZ9tG7hvwgb85wJyFd9xdpFv" or crypto.access_token == "0x6B17141D06d70B50AA4e8C263C0B4BA598c4b8a0")
            self.assertTrue(crypto.account_institution_name == "btc" or crypto.account_institution_name == "eth")

    def test_seed_command(self):
        accounttypes = AccountType.objects.all()
        users = User.objects.all()

        before_account_types_count = AccountType.objects.count()
        before_user_count = User.objects.count()

        for account_type in accounttypes:
            self.assertTrue(account_type.user.email != 'johnnydoe@example.org')

        for single_user in users:
            self.assertTrue(single_user.email != 'johnnydoe@example.org')

        call_command('seed')

        after_account_types_count = AccountType.objects.count()
        after_user_count = User.objects.count()

        self.assertEqual(before_user_count + 1, after_user_count)
        self.assertEqual(before_account_types_count + 7, after_account_types_count)

        user_john = User.objects.get(email = 'johnnydoe@example.org')

        bank_assets = AccountType.objects.filter(user = user_john, account_asset_type = AccountTypeEnum.DEBIT)
        investment_assets = AccountType.objects.filter(user = user_john, account_asset_type = AccountTypeEnum.STOCK)
        crypto_assets = AccountType.objects.filter(user = user_john, account_asset_type = AccountTypeEnum.CRYPTO)

        for bank in bank_assets:
            self.assertTrue(bank.account_institution_name == 'Vanguard' or bank.account_institution_name == 'Fidelity' or bank.account_institution_name == 'Royal Bank of Scotland - Current Accounts')

        for investment in investment_assets:
            self.assertTrue(investment.account_institution_name == 'Vanguard' or investment.account_institution_name == 'Fidelity')

        for crypto in crypto_assets:
            self.assertTrue(crypto.access_token == "1AV4KGCsvtPZ9tG7hvwgb85wJyFd9xdpFv" or crypto.access_token == "0x6B17141D06d70B50AA4e8C263C0B4BA598c4b8a0")
            self.assertTrue(crypto.account_institution_name == "btc" or crypto.account_institution_name == "eth")

    def test_unseed_command(self):
        call_command('seed')
        before_account_types_count = AccountType.objects.count()
        before_user_count = User.objects.count()
        call_command('unseed')
        after_account_types_count = AccountType.objects.count()
        after_user_count = User.objects.count()
        self.assertEqual(after_user_count, before_user_count - 1)
        self.assertEqual(after_account_types_count, before_account_types_count - 7)

        accounttypes = AccountType.objects.all()
        users = User.objects.all()

        for account_type in accounttypes:
            self.assertTrue(account_type.user.email != 'johnnydoe@example.org')

        for single_user in users:
            self.assertTrue(single_user.email != 'johnnydoe@example.org')

    def test_unseed_command_with_existing_user(self):
        user = User.objects.create_user(
        email = 'johndoe@example.org',
        first_name = 'Johnny',
        last_name = 'Doe',
        password = 'Password123',
        )
        before_account_types_count = AccountType.objects.count()
        before_user_count = User.objects.count()
        call_command('unseed')
        after_account_types_count = AccountType.objects.count()
        after_user_count = User.objects.count()
        self.assertEqual(after_user_count, before_user_count)
        self.assertEqual(after_account_types_count, before_account_types_count)
        users = User.objects.filter(email = 'johndoe@example.org')
        self.assertEqual(len(users),1)
