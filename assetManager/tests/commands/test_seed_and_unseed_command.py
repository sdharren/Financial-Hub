from django.core.management import call_command
from django.test import TestCase
from assetManager.models import User,AccountType,AccountTypeEnum
class SeedAndUnseedCommandTestCase(TestCase):

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
        self.assertEqual(before_account_types_count + 4, after_account_types_count)

        user_john = User.objects.get(email = 'johnnydoe@example.org')

        bank_assets = AccountType.objects.filter(user = user_john, account_asset_type = AccountTypeEnum.DEBIT)
        investment_assets = AccountType.objects.filter(user = user_john, account_asset_type = AccountTypeEnum.STOCK)

        for bank in bank_assets:
            self.assertTrue(bank.account_institution_name == 'Vanguard' or bank.account_institution_name == 'Fidelity')

        for investment in investment_assets:
            self.assertTrue(investment.account_institution_name == 'Vanguard' or investment.account_institution_name == 'Fidelity')

    def test_unseed_command(self):
        call_command('seed')
        before_account_types_count = AccountType.objects.count()
        before_user_count = User.objects.count()
        call_command('unseed')
        after_account_types_count = AccountType.objects.count()
        after_user_count = User.objects.count()
        self.assertEqual(after_user_count, before_user_count - 1)
        self.assertEqual(after_account_types_count, before_account_types_count - 4)

        accounttypes = AccountType.objects.all()
        users = User.objects.all()

        before_account_types_count = AccountType.objects.count()
        before_user_count = User.objects.count()

        for account_type in accounttypes:
            self.assertTrue(account_type.user.email != 'johnnydoe@example.org')

        for single_user in users:
            self.assertTrue(single_user.email != 'johnnydoe@example.org')
