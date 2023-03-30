import React, { useState, useEffect, useContext } from 'react';
import AuthContext from '../context/AuthContext';

function Accounts() {
    const [banks, setBanks] = useState([]);
    const [brokerages, setBrokerages] = useState([]);
    let {authTokens, logoutUser} = useContext(AuthContext) || {};
    
    //Function sends three GET request to the server. One to get the bank accounts the user has linked, and the one to get the linked brokerage accounts.
    //The response is then parsed as JSON. 
    //If the response is successful (HTTP status code 200), the component sets the banks, brokerages and crypto constants to the response  
    const [cryptos, setCryptos] = useState([]);

    let getAccounts = async () => {
      try {

        const bankurl = 'api/get_linked_banks/';
        const bankresponse = await fetch(bankurl, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + String(authTokens.access)
          }
        });
        const bankdata = await bankresponse.json();
        setBanks(bankdata);

        const stockurl = 'api/linked_brokerage/';
        const stockresponse = await fetch(stockurl, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + String(authTokens.access)
          }
        });
        const stockdata = await stockresponse.json();
        setBrokerages(stockdata);

        const cryptourl = 'api/linked_crypto/';
        const cryptoresponse = await fetch(cryptourl, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + String(authTokens.access)
          }
        });
        const cryptodata = await cryptoresponse.json();
        setCryptos(cryptodata);

      } catch (error) {
        console.log(error);
      }
    }

    useEffect(() => {
      // Call the async function `getAccounts` to fetch the linked accounts
      getAccounts();

    }, []);
    
    //This defines a function handleRemoveBank that sends a DELETE request to an API endpoint to unlink a bank account
    //Updates the banks state variable by removing the specified institution.
    const handleRemoveBank = async (institution) => {
      try {
        
        const delstockurl = `api/delete_linked_banks/${institution}/`
        const response = await fetch(delstockurl, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + String(authTokens.access)
          }
        });
        if (!response.ok) {
          throw new Error(`Failed to remove bank: ${response.status} ${response.statusText}`);
        }
        // Remove bank from list of linked banks
        setBanks(banks.filter(bank => bank !== institution));
      } catch (error) {
        console.log(error);
      }
    };

  //This defines a function handleRemoveBrokerage that sends a DELETE request to an API endpoint to unlink a brokerage account
  //Updates the brokerage state variable by removing the specified institution.
  const handleRemoveBrokerage = async (brokerage) => {
    
    try {
      const delbrokerageurl = `api/delete_linked_brokerage/${brokerage}/`
      const response = await fetch(delbrokerageurl, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + String(authTokens.access)
        }
      });
      if (!response.ok) {
        throw new Error(`Failed to remove brokerage: ${response.status} ${response.statusText}`);
      }
      // Remove brokerage from list of linked brokerages
      setBrokerages(brokerages.filter(b => b !== brokerage));
  
    } catch (error) {
      console.log(error);
    }
  };

  //This defines a function handleRemoveCrypto that sends a DELETE request to an API endpoint to unlink a crypto account
  //Updates the crypto state variable by removing the specified wallet.
  const handleRemoveCrypto = async (crypto) => {
    try {
      // Send DELETE request to unlink crypto account
      const response = await fetch(`api/delete_linked_crypto/${crypto}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + String(authTokens.access)
        }
      });
      if (!response.ok) {
        throw new Error(`Failed to remove crypto wallet: ${response.status} ${response.statusText}`);
      }
      // Remove bank from list of linked banks
      setCryptos(cryptos.filter(c => c !== crypto));
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className='signup-container mt-20 mx-20 p-10 rounded-3xl shadow-lg bg-gradient-to-r from-violet-500 to-violet-600' data-testid ="accountstest">
    <div className='overflow-hidden rounded border-gray-200'>
    <table className="transaction-table flex flex-col w-full h-[60vh] bg-transparent">
    <thead className='bg-gray-800 flex-[0_0_auto] text-white'>
    <tr className='w-full table table-fixed'>
          <th className='text-left py-3 px-4 uppercase font-semibold text-sm'>Name</th>
          <th className='text-left py-3 px-4 uppercase font-semibold text-sm'>Type</th>
          <th className='text-left py-3 px-4 uppercase font-semibold text-sm'>Remove</th>
        </tr>
      </thead>
      <tbody className='text-violet-300 flex-auto block overflow-y-scroll'>
        {banks.map(bank => (
          <tr className='w-full table table-fixed' key={bank}>
            <td className='text-left py-3 px-4 text-white'>{bank}</td>
            <td className='text-left py-3 px-4'>Institution</td>
            <td className='text-left py-3 px-4 text-white'>
              <button data-testid = "remove-bank" onClick={() => handleRemoveBank(bank)}>Delete</button>
            </td>
          </tr>
        ))}
        {brokerages.map(brokerage => (
          <tr key={brokerage} className='w-full table table-fixed'>
            <td className='text-left py-3 px-4 text-white'>{brokerage}</td>
            <td className='text-left py-3 px-4'>Brokerage</td>
            <td className='text-left py-3 px-4 text-white'>
              <button data-testid = "remove-brokerage"  onClick={() => handleRemoveBrokerage(brokerage)}>Delete</button>
            </td>
          </tr>
        ))}
        {cryptos.map(crypto => (
          <tr key={crypto} className='w-full table table-fixed'>
            <td className='text-left py-3 px-4 text-white'>{crypto.slice(0, 10) + "..."}</td>
            <td className='text-left py-3 px-4'>Crypto</td>
            <td className='text-left py-3 px-4 text-white'>
              <button data-testid="remove-crypto"onClick={() => handleRemoveCrypto(crypto)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
    </div>
    </div>
  );
}

export default Accounts;
