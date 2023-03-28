"""
Get balance given a wallet address
"""

# pip3 install blockcypher
from blockcypher import get_address_full, get_address_overview
import json
import requests as re

from assetManager.models import AccountType, AccountTypeEnum
from assetManager.helpers import make_aware_date
from datetime import datetime
from django.db import IntegrityError

# KEY is BTC/ETH and Value is List of addresses
ADDRESSES = {"btc" : ["34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo", "16ftSEQ4ctQFDtVZiUBusQUjRrGhM3JYwe"], 
             "eth" : ["0x6090a6e47849629b7245dfa1ca21d94cd15878ef", "0x4675C7e5BaAFBFFbca748158bEcBA61ef3b0a263"]}

# All return values in JSON form
# BTC Docs available @ https://www.blockcypher.com/dev/bitcoin/?python#address-endpoint
# ETH Docs available @ https://www.blockcypher.com/dev/ethereum/#address-balance-endpoint
class getCryptoAddressData:
    def BTC_all(addr):
        return get_address_full(address=addr, confirmations=3, api_key='9c75ffab7c524ab19cee9d749110a3b2')

    def ETH_all(addr):
        command = "https://api.blockcypher.com/v1/eth/main/addrs/" + str(addr)
        return re.get(command).json()

    def BTC_overview(addr):
        return(get_address_overview(address=addr, api_key='9c75ffab7c524ab19cee9d749110a3b2'))

    def ETH_overview(addr):
        command = "https://api.blockcypher.com/v1/eth/main/addrs/" + str(addr) + "/balance"
        return re.get(command).json()


def toBase(amount, type):
    if(type == "btc"):
        amount = amount/(10**(8))
    elif(type == "eth"):
        amount = amount/(10**(18))

    return amount


class getUsableCrypto:
    def getAddress(data, type):
        return (data.get("address"))

    def getBalance(data, type):
        return toBase((data.get("final_balance")), type)
    
    def getNoTx(data, type):
        return (data.get("n_tx"))

    def getTotalReceived(data, type):
        return toBase((data.get("total_received")), type)

    def getTotalSent(data, type):
        return toBase((data.get("total_sent")), type)

    def getTxs(data, type):
        if(type == "btc"):
            value = data.get("txs")
        elif(type == "eth"):
            value = data.get("txrefs")
        
        return value

# When run collect data for all addresses listed
def getAllCryptoData(user):
    data = {} # Dict where key is address and value is 2d array where index 0 is coin type and index 1 is value returned

    btcAddresses = AccountType.objects.all().filter(user=user, account_asset_type="CRYPTO", account_institution_name="btc")
    ethAddresses = AccountType.objects.all().filter(user=user, account_asset_type="CRYPTO", account_institution_name="eth")

    if(btcAddresses != None):
        for account in btcAddresses:
            addr = account.access_token

            value = getCryptoAddressData.BTC_all(addr)
            arrVal = [value, "btc"]

            data[addr] = arrVal

    if(ethAddresses != None):
        for account in ethAddresses:
            addr = account.access_token

            value = getCryptoAddressData.ETH_all(addr)
            arrVal = [value, "eth"]

            data[addr] = arrVal
    return data

# Collect select data from api instead of requesting all data
def getAlternateCryptoData(user, command, data):

    # Command format is getUsable.{function}((data[i]), data[i][-1])
    #data = {} # Dict where key is address and value is 2d array where index 0 is coin type and index 1 is value returned

    btcAddresses = AccountType.objects.all().filter(user=user, account_asset_type="CRYPTO", account_institution_name="btc")
    ethAddresses = AccountType.objects.all().filter(user=user, account_asset_type="CRYPTO", account_institution_name="eth")

    if(btcAddresses != None):
        for account in btcAddresses:
            addr = account.access_token
            if(addr in list(data.keys())):

                value = data.get(addr)[0]
                
                if command == "address":
                    value = getUsableCrypto.getAddress(value, "btc")
                elif command == "balance":
                    value = getUsableCrypto.getBalance(value, "btc")
                elif command == "notx":
                    value = getUsableCrypto.getNoTx(value, "btc")
                elif command == "received":
                    value = getUsableCrypto.getTotalReceived(value, "btc")
                elif command == "sent":
                    value = getUsableCrypto.getTotalSent(value, "btc")
                elif command == "txs":
                    value = getUsableCrypto.getTxs(value, "btc")
                    
                arrVal = [value, "btc"]

                data[addr] = arrVal

    if(ethAddresses != None):
        for account in ethAddresses:
            addr = account.access_token
            if(addr in list(data.keys())):

                value = data.get(addr)[0]

            if command == "address":
                value = getUsableCrypto.getAddress(value, "eth")
            elif command == "balance":
                value = getUsableCrypto.getBalance(value, "eth")
            elif command == "notx":
                value = getUsableCrypto.getNoTx(value, "eth")
            elif command == "received":
                value = getUsableCrypto.getTotalReceived(value, "eth")
            elif command == "sent":
                value = getUsableCrypto.getTotalSent(value, "eth")
            elif command == "txs":
                value = getUsableCrypto.getTxs(value, "eth")
            
            arrVal = [value, "eth"]

            data[addr] = arrVal

    return data

def save_wallet_address(user, address):
    try:
        AccountType.objects.create(
            user = user,
            account_asset_type = AccountTypeEnum("CRYPTO"),
            account_date_linked = make_aware_date(datetime.now()),
            access_token = address,
            account_institution_name = "eth" if address[0:2] == "0x" else "btc"
        )
    except IntegrityError:
        return # if there is an integrity error the address this user already linked this address

def get_wallets(user):
    accounts = AccountType.objects.all().filter(user=user, account_asset_type="CRYPTO")
    wallets = []
    for wallet in accounts:
        wallets.append(wallet.access_token)
    return wallets

