import React from 'react';
import '../../table.css';
import { useState } from 'react';
import { useEffect } from 'react';
import { useContext } from 'react';
import AuthContext from '../../context/AuthContext';





const CRecentTransactionsDisplay = () => {
  const [transactions, setTransactions] = useState([]);
  let {authTokens, logoutUser} = useContext(AuthContext);


  let getTransactions = async () => {
    let transactionURL = 'http://127.0.0.1:8000/api/crypto_select_data/?param=txs';
    let response = await fetch(transactionURL, {
      method: 'GET',
      headers: {
        'Content-Type':'application/json',
        'Authorization':'Bearer ' + String(authTokens.access)
      },
    });
    let data = await response.json();
    if (response.status === 200) {
        setTransactions(data);
    }
    else {
      console.error(`Failed to fetch recent transactions: ${response.status} ${response.statusText}`);
    }

    }


  useEffect(() => {
    // Call the async function `getTransactions` to fetch the recent transactions
    getTransactions();
  }, []);

  const renderTableHeader = () => {
    return (
      <tr>
        <th>Address</th>
        <th>Confirmations</th>
        <th>Amount</th>
      </tr>
    );
  }

  const renderTableData = () => {
    return transactions[transactions].map(({ address, confirmations, amount }) => {
      return (
        <tr key={address}>
          <td>{address}</td>
          <td>{confirmations}</td>
          <td>{amount}</td>
        </tr>
      );
    });
  }

  return (
    <table className="transaction-table">
      <thead>{renderTableHeader()}</thead>
      <tbody>{renderTableData()}</tbody>
    </table>
  );
};

export default CRecentTransactionsDisplay;
