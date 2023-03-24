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
        const delstockurl = `http://127.0.0.1:8000/api/delete_linked_bank/${institution}/`
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
        console.error(error);
      }
    };

  const handleRemoveBrokerage = async (brokerage) => {
    // Send DELETE request to unlink brokerage account
    try {
      const delbrokerageurl = `http://127.0.0.1:8000/api/delete_linked_brokerage/${brokerage}/`
      const response = await fetch(delbrokerageurl, {
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
    <div>
      <h1 className='accounts-name'>Accounts</h1>
      <table className='accounts-table'>
        <thead className='accounts-head'>
          <tr className='accounts-row'>
            <th className='accounts-head'>Name</th>
            <th className='accounts-head'>Type</th>
            <th className='accounts-head'>Remove</th>
          </tr>
        </thead>
        <tbody>
          {banks.map(bank => (
            <tr  key={bank}>
              <td className='accounts-column'>{bank}</td>
              <td className='accounts-column'>Institution</td>
              <td className='accounts-column'>
                <button className='accounts-removebutton' onClick={() => handleRemoveBank(bank)}>Remove</button>
              </td>
            </tr>
          ))}
          {brokerages.map(brokerage => (
            <tr  key={brokerage}>
              <td className='accounts-column'>{brokerage}</td>
              <td className='accounts-column'>Brokerage</td>
              <td className='accounts-column'>
                <button className='accounts-removebutton' onClick={() => handleRemoveBrokerage(brokerage)}>Remove</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Accounts;
