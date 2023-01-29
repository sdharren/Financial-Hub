"""
Get balance given a wallet address
"""

# pip3 install blockcypher
from blockcypher import get_address_full
import requests as re

# KEY is BTC/ETH and Value is List of addresses
ADDRESSES = {"btc" : [], 
             "eth" : []}

# All return values in JSON form
# BTC Docs available @ https://www.blockcypher.com/dev/bitcoin/?python#address-endpoint
# ETH Docs available @ https://www.blockcypher.com/dev/ethereum/#address-balance-endpoint
class getAddressData:
    def BTC_all(addr):
        return get_address_full(address=addr, confirmations=3)

    def ETH_all(addr):
        command = "https://api.blockcypher.com/v1/eth/main/addrs/" + str(addr)
        return re.get(command).json()


def toBase(amount, type):
    if(type == "btc"):
            amount = amount/(10^8)
    elif(type == "eth"):
        amount = amount/(10^(18))

    return amount


class getUsable:
    def getAddress(data):
        return (data["address"])

    def getBalance(data, type):
        return toBase((data["final_balance"]), type)
    
    def getNoTx(data):
        return (data["n_tx"])

    def getTotalReceived(data, type):
        return toBase((data["total_received"]), type)

    def getTotalSent(data, type):
        return toBase((data["total_sent"]), type)

    def getTxs(data, type):
        if(type == "btc"):
            value = data["txs"]
        elif(type == "eth"):
            value = data["txrefs"]
        
        return value

    
if __name__ == '__main__':
    data = [] # 2D Array where index 0 is actual data and index 1 is type of coin

    btcAddresses = ADDRESSES.get("btc", None)
    ethAddresses = ADDRESSES.get("eth", None)

    if(btcAddresses != None):
        for addr in btcAddresses:
            value = [getAddressData.BTC_all(addr), "btc"]
            data.append(value)

    if(ethAddresses != None):
        for addr in ethAddresses:
            value = [getAddressData.ETH_all(addr), "eth"]
            data.append(value)