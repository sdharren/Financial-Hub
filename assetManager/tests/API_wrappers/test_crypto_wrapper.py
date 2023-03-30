from django.test import TestCase
from assetManager.API_wrappers.crypto_wrapper import *
from assetManager.models import User, AccountType
from django.db import IntegrityError, transaction
import re


class CryptoWraperTestCase(TestCase):
    fixtures = [
        'assetManager/tests/fixtures/users.json',
        'assetManager/tests/fixtures/account_types.json'
    ]
    crypto_btc_example_data = {"1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD": [{
        "address": "1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD",
        "balance": 4433416,
        "final_balance": 4433416,
        "final_n_tx": 7,
        "n_tx": 7,
        "total_received": 4433416,
        "total_sent": 0,
        "txs": [
            {
                "addresses": [
                    "18KXZzuC3xvz6upUMQpsZzXrBwNPWZjdSa",
                    "1AAuRETEcHDqL4VM3R97aZHP8DSUHxpkFV",
                    "1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD",
                    "1VxsEDjo6ZLMT99dpcLu4RQonMDVEQQTG"
                ],
                "block_hash": "0000000000000000af64802c79f9b22e9091eb5548b4b662d5e444e61885923b",
                "block_height": 292586,
                "confidence": 1,
                "confirmations": 87238,
                "confirmed": "datetime.datetime(2014, 3, 26, 17, 8, 4, 0, tzinfo=tzutc())",
                "double_spend": False,
                "fees": 20000,
                "hash": "b4735a0690dab16b8789fceaf81c511f3be484e319f684cc214380eaa2851030",
                "inputs": [
                    {
                        "addresses": [
                            "1VxsEDjo6ZLMT99dpcLu4RQonMDVEQQTG"
                        ],
                        "output_index": 0,
                        "output_value": 3500000,
                        "prev_hash": "729f6469b59fea5da77457f3291e2623c2516e3e8e7afc782687c6d59f4c5e41",
                        "script": "483045022100d06cdad1a54081e8499a4117f9f52d7fbc83c679dda7e3c22c08e964915b7354022010a2d6af1601d28d33a456dab2bccf3fbde35b2f3a9db82f72d675c90d015571014104672a00c8ee6fa23d68094dd98188ea1491848498554a10e13194851b614168b225b28b7f5a1c6ba98b5463438ef030c48b60533031ff2de84104e549d8d06ea9",
                        "script_type": "pay-to-pubkey-hash",
                        "sequence": 4294967295
                    }

                ],
                "lock_time": 0,
                "outputs": [
                    {
                        "addresses": [
                            "1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD"
                        ],
                        "script": "76a9148629647bd642a2372d846a7660e210c8414f047c88ac",
                        "script_type": "pay-to-pubkey-hash",
                        "value": 3500000
                    }
                ],
                "preference": "medium",
                "received": "datetime.datetime(2014, 3, 26, 17, 8, 4, 0, tzinfo=tzutc())",
                "relayed_by": "",
                "size": 438,
                "total": 3537488,
                "ver": 1,
                "vin_sz": 2,
                "vout_sz": 2
            }
        ],
        "unconfirmed_balance": 0,
        "unconfirmed_n_tx": 0}, "btc"]}

    crypto_eth_example_data = { "0x7CEcBd7a618146Cb251735b524e98f62d548177b": [{
        "address": "0x7CEcBd7a618146Cb251735b524e98f62d548177b",
        "total_received": 613136037139846027,
        "total_sent": 609820639361600898,
        "balance": 3315397778245129,
        "unconfirmed_balance": 0,
        "final_balance": 3315397778245129,
        "n_tx": 58,
        "unconfirmed_n_tx": 0,
        "final_n_tx": 58,
        "nonce": 36,
        "pool_nonce": 36,
        "hasMore": True,
        "txs": [
            {
            "block_hash": "eec1dd4d7271a53ada4cf3145577d0610e8648aefa42a9420a7ab1d3ae9a787b",
            "block_height": 13113955,
            "block_index": 550,
            "hash": "5b199d5a3b3a3f9b2ffe37878bb3b428affbec117e7888202ba22503b3967a79",
            "addresses": [
                "7cecbd7a618146cb251735b524e98f62d548177b",
                "f9209e6809e0a08ae18b1366c437cb3cad2b6182"
            ],
            "total": 1550897349206251,
            "fees": 735000000000000,
            "size": 109,
            "gas_limit": 21000,
            "gas_used": 21000,
            "gas_price": 35000000000,
            "gas_tip_cap": 35000000000,
            "gas_fee_cap": 35000000000,
            "confirmed": "2021-08-28T12:41:39Z",
            "received": "2021-08-28T12:01:08.52Z",
            "ver": 0,
            "double_spend": False,
            "vin_sz": 1,
            "vout_sz": 1,
            "confirmations": 111695,
            "confidence": 1,
            "inputs": [
                {
                "sequence": 35,
                "addresses": [
                    "7cecbd7a618146cb251735b524e98f62d548177b"
                ]
                }
            ],
            "outputs": [
                {
                "value": 1550897349206251,
                "addresses": [
                    "f9209e6809e0a08ae18b1366c437cb3cad2b6182"
                ]
                }
            ]
            },
        ]
        }, "eth"]}
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
        self.assertEqual(list(crypto_data.keys())[0],'0x7CEcBd7a618146Cb251735b524e98f62d548177b')
        
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
