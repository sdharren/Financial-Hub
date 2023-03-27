import React, { useState, useEffect, useContext } from 'react';
import AuthContext from '../context/AuthContext';

function Accounts() {
    const [banks, setBanks] = useState([]);
    const [brokerages, setBrokerages] = useState([]);
    let {authTokens, logoutUser} = useContext(AuthContext);
    
    let getAccounts = async () => {
      try {
        
        const bankurl = 'http://127.0.0.1:8000/api/get_linked_banks/';
        const bankresponse = await fetch(bankurl, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + String(authTokens.access)
          }
        });
        const bankdata = await bankresponse.json();
        setBanks(bankdata);
    
        const stockurl = 'http://127.0.0.1:8000/api/linked_brokerage/';
        const stockresponse = await fetch(stockurl, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + String(authTokens.access)
          }
        });
        const stockdata = await stockresponse.json();
        setBrokerages(stockdata);
    
      } catch (error) {
        console.error(error);
      }
    }
    
    useEffect(() => {
      // Call the async function `getAccounts` to fetch the linked accounts
      getAccounts();
    }, []);

    const handleRemoveBank = async (institution) => {
      try {
        // Send DELETE request to unlink bank account
        const response = await fetch(`/api/delete_linked_banks/${institution}/`, {
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
        console.error(error);
      }
    };

  const handleRemoveBrokerage = async (brokerage) => {
    // Send DELETE request to unlink brokerage account
    try {
      
      const response = await fetch(`/api/delete_linked_brokerage/${brokerage}/`, {
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
      setBrokerages(brokerages.filter(b => b !== brokerage));
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className='signup-container mt-20 mx-20 p-10 rounded-3xl shadow-lg bg-gradient-to-r from-violet-500 to-violet-600'>
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
              <button onClick={() => handleRemoveBank(bank)}>Remove</button>
            </td>
          </tr>
        ))}
        {brokerages.map(brokerage => (
          <tr key={brokerage} className='w-full table table-fixed'>
            <td className='text-left py-3 px-4 text-white'>{brokerage}</td>
            <td className='text-left py-3 px-4'>Brokerage</td>
            <td className='text-left py-3 px-4 text-white'>
              <button onClick={() => handleRemoveBrokerage(brokerage)}>Remove</button>
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
