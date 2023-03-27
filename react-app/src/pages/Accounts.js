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
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Type</th>
          <th>Remove</th>
        </tr>
      </thead>
      <tbody>
        {banks.map(bank => (
          <tr key={bank}>
            <td>{bank}</td>
            <td>Institution</td>
            <td>
              <button onClick={() => handleRemoveBank(bank)}>Remove</button>
            </td>
          </tr>
        ))}
        {brokerages.map(brokerage => (
          <tr key={brokerage}>
            <td>{brokerage}</td>
            <td>Brokerage</td>
            <td>
              <button onClick={() => handleRemoveBrokerage(brokerage)}>Remove</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default Accounts;
