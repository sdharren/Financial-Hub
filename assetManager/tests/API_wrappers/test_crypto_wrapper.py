from django.test import TestCase
from assetManager.API_wrappers.crypto_wrapper import save_wallet_address, get_wallets, getAllCryptoData
from assetManager.models import User, AccountType
from django.db import IntegrityError, transaction


class CryptoWraperTestCase(TestCase):
    fixtures = [
        'assetManager/tests/fixtures/users.json',
        'assetManager/tests/fixtures/account_types.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.org')
        self.btc_address = '34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo'
        self.eth_address = '0x6090a6e47849629b7245dfa1ca21d94cd15878ef'

    def test_save_wallet_address_works_with_eth(self):
        count_before = AccountType.objects.all().count()
        save_wallet_address(self.user, self.eth_address)
        count_after = AccountType.objects.all().count()
        self.assertEqual(count_before + 1, count_after)

        account_type = AccountType.objects.filter(user = self.user, account_asset_type="CRYPTO")[0]
        self.assertEqual(account_type.access_token, self.eth_address)
        self.assertEqual(account_type.account_asset_type, 'CRYPTO')
        self.assertEqual(account_type.account_institution_name, 'eth')

    def test_save_wallet_address_works_with_btc(self):
        count_before = AccountType.objects.all().count()
        save_wallet_address(self.user, self.btc_address)
        count_after = AccountType.objects.all().count()
        self.assertEqual(count_before + 1, count_after)

        account_type = AccountType.objects.filter(user = self.user, account_asset_type="CRYPTO")[0]
        self.assertEqual(account_type.access_token, self.btc_address)
        self.assertEqual(account_type.account_asset_type, 'CRYPTO')
        self.assertEqual(account_type.account_institution_name, 'btc')

    def test_saving_duplicate_address_does_nothing(self):
        save_wallet_address(self.user, self.eth_address)
        count_before = AccountType.objects.all().count()
        with transaction.atomic():
            save_wallet_address(self.user, self.eth_address)
        count_after = AccountType.objects.all().count()
        self.assertEqual(count_before, count_after)

    def test_get_wallets_works_for_one_wallet(self):
        save_wallet_address(self.user, self.eth_address)
        wallets = get_wallets(self.user)
        self.assertEqual(len(wallets), 1)
        self.assertEqual(wallets[0], self.eth_address)

    def test_get_wallets_works_for_multiple_wallets(self):
        save_wallet_address(self.user, self.eth_address)
        save_wallet_address(self.user, self.btc_address)
        wallets = get_wallets(self.user)
        self.assertEqual(len(wallets), 2)

    def test_data_recieved_in_dictionary(self):
        

    

    