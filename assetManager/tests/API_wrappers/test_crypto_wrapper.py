from django.test import TestCase
from assetManager.API_wrappers.crypto_wrapper import *
from assetManager.models import User, AccountType
from django.db import IntegrityError, transaction
import re
from assetManager.tests.API_wrappers.etheureum import eth
from assetManager.tests.API_wrappers.bitcoin import bitcoin


class CryptoWraperTestCase(TestCase):
    fixtures = [
        'assetManager/tests/fixtures/users.json',
        'assetManager/tests/fixtures/account_types.json'
    ]
    crypto_btc_example_data = bitcoin

    crypto_eth_example_data = eth
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

    def test_get_all_crypto_data_linked_wallets(self):
        save_wallet_address(self.user,"1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD")
        save_wallet_address(self.user,"0x7CEcBd7a618146Cb251735b524e98f62d548177b")
        data = getAllCryptoData(self.user)
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)

    def test_addr_regex_correct(self, data=crypto_btc_example_data):
        self.assertTrue(re.match(r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$", list(data.keys())[0]) or re.match(r"(\b0x[a-f0-9]{40}\b)", list(data.keys())[0]))

    def test_find_fiat_rates(self):
        conversion_rates = find_fiat_rates()
        self.assertEqual(2,len(conversion_rates))
        self.assertNotEqual(conversion_rates[0],None)
        self.assertNotEqual(conversion_rates[1],None)

    def test_get_usable_crypto(self,data=crypto_btc_example_data.get("1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD")[0]):
        self.assertNotEqual(getAddress(data,"etc"),None)
        self.assertNotEqual(getBalance(data,"etc"),None)
        self.assertNotEqual(getNoTx(data,"etc"),None)
        self.assertNotEqual(getTotalReceived(data,"etc"),None)
        self.assertNotEqual(getTotalSent(data,"etc"),None)
        self.assertNotEqual(getTxs(data,"etc"),None)

    def test_get_all_crypto_data_with_no_wallet_linked(self):
        crypto_data = getAllCryptoData(self.user)
        self.assertEqual(crypto_data,{})
        self.assertIsInstance(crypto_data,dict)

    def test_get_alternate_crypto_data_with_wallet_linked_address(self,data=crypto_eth_example_data):
        save_wallet_address(self.user, "0x00000000219ab540356cBB839Cbe05303d7705Fa")
        crypto_data = getAlternateCryptoData(self.user,"address",data)
        self.assertNotEqual(crypto_data,None)
        self.assertIsInstance(crypto_data,dict)
        self.assertEqual(list(crypto_data.keys())[0],'0x00000000219ab540356cBB839Cbe05303d7705Fa')


    def test_get_alternate_crypto_data_with_no_wallet_linked(self,data={}):
        crypto_data = getAlternateCryptoData(self.user,"address",data)
        self.assertEqual(crypto_data,{})
        self.assertIsInstance(crypto_data,dict)

    def test_BTC_all(self):
        self.assertNotEqual(BTC_all("1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD"),{})

    def test_ETH_all(self):
        self.assertNotEqual(ETH_all("0xbd3Afb0bB76683eCb4225F9DBc91f998713C3b01"),{})

    def test_to_base(self):
        self.assertEqual(toBase(100,"btc"),1e-06)
        self.assertEqual(toBase(100,"eth"),1e-16)

    def test_alternate_crypto_command_address(self, data=crypto_btc_example_data):
        value = data.get("1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD")[0].get("address")
        returned = getAlternateCryptoData(self.user, "address", data).get("1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD")[0].get("address")
        self.assertEqual(returned, value)

    def test_alternate_crypto_command_balance(self, data=crypto_btc_example_data):
        value = data["1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD"][0].get("balance")
        returned = getAlternateCryptoData(self.user, "balance", data).get("1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD")[0].get("balance")
        self.assertEqual(returned, value)

    def test_alternate_crypto_command_n_tx(self, data=crypto_btc_example_data):
        value = data["1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD"][0].get("n_tx")
        returned = getAlternateCryptoData(self.user, "notx", data).get("1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD")[0].get("n_tx")
        self.assertEqual(returned, value)

    def test_alternate_crypto_command_total_received(self, data=crypto_btc_example_data):
        value = data["1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD"][0].get("total_received")
        returned = getAlternateCryptoData(self.user, "received", data).get("1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD")[0].get("total_received")
        self.assertEqual(returned, value)

    def test_alternate_crypto_command_total_sent(self, data=crypto_btc_example_data):
        value = data["1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD"][0].get("total_sent")
        returned = getAlternateCryptoData(self.user, "sent", data).get("1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD")[0].get("total_sent")
        self.assertEqual(returned, value)

    def test_alternate_crypto_command_txs(self, data=crypto_btc_example_data):
        value = data["1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD"][0].get("txs")
        returned = getAlternateCryptoData(self.user, "txs", data).get("1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD")[0].get("txs")
        self.assertEqual(returned, value)
