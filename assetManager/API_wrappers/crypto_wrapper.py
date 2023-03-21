"""
Get balance given a wallet address
"""

# pip3 install blockcypher
from blockcypher import get_address_full
import json
import requests as re

# KEY is BTC/ETH and Value is List of addresses
ADDRESSES = {"btc" : ["34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo", "16ftSEQ4ctQFDtVZiUBusQUjRrGhM3JYwe"], 
             "eth" : ["0x6090a6e47849629b7245dfa1ca21d94cd15878ef", "0x4675C7e5BaAFBFFbca748158bEcBA61ef3b0a263"]}

# All return values in JSON form
# BTC Docs available @ https://www.blockcypher.com/dev/bitcoin/?python#address-endpoint
# ETH Docs available @ https://www.blockcypher.com/dev/ethereum/#address-balance-endpoint
class getCryptoAddressData:
    def BTC_all(addr):
        return get_address_full(address=addr, confirmations=3)

    def ETH_all(addr):
        command = "https://api.blockcypher.com/v1/eth/main/addrs/" + str(addr)
        return re.get(command).json()


def toBase(amount, type):
    if(type == "btc"):
            amount = amount/(10**(8))
    elif(type == "eth"):
        amount = amount/(10**(18))

    return amount


class getUsableCrypto:
    def getAddress(data, type):
        return (data[0].get("address"))

    def getBalance(data, type):
        return toBase((data[0].get("final_balance")), type)
    
    def getNoTx(data, type):
        return (data[0].get("n_tx"))

    def getTotalReceived(data, type):
        return toBase((data[0].get("total_received")), type)

    def getTotalSent(data, type):
        return toBase((data[0].get("total_sent")), type)

    def getTxs(data, type):
        if(type == "btc"):
            value = data[0].get("txs")
        elif(type == "eth"):
            value = data[0].get("txrefs")
        
        return value

# When run collect data for all addresses listed
def getAllCryptoData(addresses):
    # Command format is getUsable.{function}((data[i]), data[i][-1])
    data = {} # Dict where key is address and value is 2d array where index 0 is coin type and index 1 is value returned

    btcAddresses = addresses.get("btc", None)
    ethAddresses = addresses.get("eth", None)

    if(btcAddresses != None):
        for addr in btcAddresses:
            value = getCryptoAddressData.BTC_all(addr)
            arrVal = [value, "btc"]

            data[addr] = arrVal

    if(ethAddresses != None):
        for addr in ethAddresses:
            value = getCryptoAddressData.ETH_all(addr)
            arrVal = [value, "eth"]

            data[addr] = arrVal
    
    return data

# Collect select data from api instead of requesting all data
def getAlternateCryptoData(addresses, alternate):
    # Command format is getUsable.{function}((data[i]), data[i][-1])
    data = {} # Dict where key is address and value is 2d array where index 0 is coin type and index 1 is value returned

    btcAddresses = ADDRESSES.get("btc", None)
    ethAddresses = ADDRESSES.get("eth", None)

    if(btcAddresses != None):
        for addr in btcAddresses:
            value = getCryptoAddressData.BTC_all(addr)

            if alternate == "address":
                value = getUsableCrypto.getAddress(value, "btc")
            elif alternate == "balance":
                value = getUsableCrypto.getBalance(value, "btc")
            elif alternate == "notx":
                value = getUsableCrypto.getNoTx(value, "btc")
            elif alternate == "received":
                value = getUsableCrypto.getTotalReceived(value, "btc")
            elif alternate == "sent":
                value = getUsableCrypto.getTotalSent(value, "btc")
            elif alternate == "txs":
                value = getUsableCrypto.getTxs(value, "btc")
                
            arrVal = [value, "btc"]

            data[addr] = arrVal

    if(ethAddresses != None):
        for addr in ethAddresses:
            value = getCryptoAddressData.ETH_all(addr)

            if alternate == "address":
                value = getUsableCrypto.getAddress(value, "eth")
            elif alternate == "balance":
                value = getUsableCrypto.getBalance(value, "eth")
            elif alternate == "notx":
                value = getUsableCrypto.getNoTx(value, "eth")
            elif alternate == "received":
                value = getUsableCrypto.getTotalReceived(value, "eth")
            elif alternate == "sent":
                value = getUsableCrypto.getTotalSent(value, "eth")
            elif alternate == "txs":
                value = getUsableCrypto.getTxs(value, "eth")
            
            arrVal = [value, "eth"]

            data[addr] = arrVal

    return data
