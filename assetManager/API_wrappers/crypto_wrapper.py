"""
Get balance given a wallet address
"""

# pip3 install blockcypher
from blockcypher import get_address_full, get_address_overview
import requests as re

from assetManager.models import AccountType, AccountTypeEnum
from assetManager.helpers import make_aware_date
from datetime import datetime
from django.db import IntegrityError

# KEY is BTC/ETH and Value is List of addresses
ADDRESSES = {"btc" : ["34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo", "16ftSEQ4ctQFDtVZiUBusQUjRrGhM3JYwe"], 
             "eth" : ["0x6090a6e47849629b7245dfa1ca21d94cd15878ef", "0x4675C7e5BaAFBFFbca748158bEcBA61ef3b0a263"]}


"""
@params: addr (str) - The cryptocurrency address for which data is to be fetched.

@Description:
The class getCryptoAddressData provides methods to retrieve data related to cryptocurrency addresses for Bitcoin (BTC) and Ethereum (ETH). The BTC_all() and ETH_all() methods return complete address data including transaction history.

The data is obtained using API requests to BlockCypher and requires an API key for Bitcoin methods. The addr parameter is the address for which the data is to be retrieved.

@return:
The methods return the requested data in JSON format.
"""
class getCryptoAddressData:
    def BTC_all(addr):
        return get_address_full(address=addr, confirmations=3, api_key='9c75ffab7c524ab19cee9d749110a3b2')

    def ETH_all(addr):
        command = "https://api.blockcypher.com/v1/eth/main/addrs/" + str(addr)
        return re.get(command).json()

"""
@params: None

@Description: This function retrieves the current exchange rates for Bitcoin and Ethereum in GBP (Great British Pound) from the CoinGecko API by making two GET requests. The rates are returned as a list of floats.

@return: A list of two floats representing the current exchange rates for Bitcoin and Ethereum in GBP.
"""
def find_fiat_rates():
    response_btc = re.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=gbp')
    btc_gbp = response_btc.json()["bitcoin"]["gbp"]

    # Make a GET request to the CoinGecko API to get the ETH-to-GBP exchange rate
    response_eth = re.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=gbp')
    eth_gbp = response_eth.json()["ethereum"]["gbp"]

    rates = [btc_gbp, eth_gbp]

    return(rates)


"""
@params: amount (float) - the amount to be converted to a different base, type (string) - the type of cryptocurrency to which the conversion needs to be done ('btc' or 'eth').

@Description: This function takes in an amount and a type of cryptocurrency, and converts the amount to a different base. If the type is 'btc', the amount is divided by 10^8, and if the type is 'eth', the amount is divided by 10^18. The converted amount is then returned.

@return: The converted amount (float).
"""
def toBase(amount, type):
    if(type == "btc"):
        amount = amount/(10**(8))
    elif(type == "eth"):
        amount = amount/(10**(18))
        

    return amount

"""
@params: data (dict), type (str)

@Description: 
This class contains several methods to extract different pieces of information related to cryptocurrencies, such as the address, balance, number of transactions, total amount received, total amount sent, and transaction details. These methods take in a dictionary 'data' that contains relevant information about a cryptocurrency and a string 'type' that specifies the type of cryptocurrency. 

@return: 
Each method returns a specific piece of information extracted from the 'data' dictionary in the specified format. The 'getAddress' method returns the address, the 'getBalance' method returns the final balance converted to the specified base, the 'getNoTx' method returns the number of transactions, the 'getTotalReceived' method returns the total amount received converted to the specified base, the 'getTotalSent' method returns the total amount sent converted to the specified base, and the 'getTxs' method returns transaction details.

"""
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

"""
@params: user (object)

@Description: This function retrieves all cryptocurrency data for a given user by querying the database for all Bitcoin and Ethereum addresses associated with their account. It then uses the getCryptoAddressData library to fetch the cryptocurrency data for each address and calculates the value in fiat currency using the current exchange rates. The resulting data is stored in a dictionary where the key is the address and the value is a 2D array containing the cryptocurrency data and the coin type.

@return: A dictionary containing all the cryptocurrency data for the user.
"""
def getAllCryptoData(user):
    data = {} # Dict where key is address and value is 2d array where index 0 is coin type and index 1 is value returned

    btcAddresses = AccountType.objects.all().filter(user=user, account_asset_type="CRYPTO", account_institution_name="btc")
    ethAddresses = AccountType.objects.all().filter(user=user, account_asset_type="CRYPTO", account_institution_name="eth")

    rate = find_fiat_rates()

    if(btcAddresses != None):
        for account in btcAddresses:
            addr = account.access_token

            value = getCryptoAddressData.BTC_all(addr)
            amount = value["final_balance"] 
            value["final_balance"] = (amount) * rate[0]
            arrVal = [value, "btc"]

            data[addr] = arrVal

    if(ethAddresses != None):
        for account in ethAddresses:
            addr = account.access_token

            value = getCryptoAddressData.ETH_all(addr)
            
            amount = value["final_balance"] 
            value["final_balance"] = (amount) * rate[1]
            
            arrVal = [value, "eth"]

            data[addr] = arrVal
    return data

"""
@params: user (str), command (str), data (dict)
- user: the user for whom the function retrieves cryptocurrency data
- command: the command to execute on the data (e.g., get address, balance, transaction history)
- data: a dictionary where the key is the cryptocurrency address and the value is a list containing the coin type and value returned

@Description: This function retrieves cryptocurrency data for a user based on a given command (e.g., get address, balance, transaction history). The function first retrieves Bitcoin and Ethereum addresses for the user from the AccountType table, then loops through the addresses to find those that are in the data dictionary. For each address found, the function executes the command on the associated cryptocurrency (Bitcoin or Ethereum) using the getUsableCrypto module and stores the result in the data dictionary. Finally, the function returns the updated data dictionary.

@return: data (dict) - the updated dictionary containing the retrieved cryptocurrency data.
"""
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

"""
@params: user (User object), address (str)
          - user: The user object to which the wallet address belongs
          - address: The wallet address to be saved in the database

@Description: This function saves a user's wallet address in the database as a new AccountType object. It checks whether the wallet address already exists in the database for the given user. If it does, the function returns without saving anything. Otherwise, it saves the new wallet address in the database along with some additional information such as the account asset type, date linked, access token, and institution name.

@return: None
"""
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

"""
@params: user (User object) - The user for whom the wallets need to be retrieved.
    
@Description: This function retrieves the wallets for a given user, by fetching all account types which have an account_asset_type of "CRYPTO" and belong to the specified user. It then extracts the access token for each of these accounts and returns them as a list of wallets.

@return: wallets (list) - A list of access tokens for all wallets owned by the specified user.
"""
def get_wallets(user):
    accounts = AccountType.objects.all().filter(user=user, account_asset_type="CRYPTO")
    wallets = []
    for wallet in accounts:
        wallets.append(wallet.access_token)
    return wallets

