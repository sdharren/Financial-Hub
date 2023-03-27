import React from 'react';
import '../../table.css';
import { useState } from 'react';
import { useEffect } from 'react';
import AuthContext from '../../context/AuthContext';

function RecentTransactionsDisplay() {
  const [transactions, setTransactions] = useState([]);


let getTransactions = async () => {
  let transactionURL = 'http://127.0.0.1:8000/api/crypto_select_data?param=txs/';
  let response = await fetch(transactionURL, {
    method: 'GET',
    headers: {
      'Content-Type':'application/json',
      'Authorization':'Bearer ' + String(authTokens.access)
    },
  });
  let data = await response.json();
  if (response.status === 200) {
      setTransactions(data['Royal Bank of Scotland - Current Accounts']);
  }
  else {
    console.error(`Failed to fetch recent transactions: ${response.status} ${response.statusText}`);
  }

  }


useEffect(() => {
  // Call the async function `getTransactions` to fetch the recent transactions
  getTransactions();
}, []);

}



const TransactionTable = () => {
  const renderTableHeader = () => {
    return (
      <tr>
        <th>Amount</th>
        <th>Date</th>
        <th>Category</th>
        <th>Merchant</th>
      </tr>
    );
  }

  const renderTableData = () => {
    return transactions['Royal Bank of Scotland - Current Accounts'].map(({ amount, date, category, merchant }) => {
      return (
        <tr key={amount}>
          <td>{amount}</td>
          <td>{date.toLocaleDateString()}</td>
          <td>{category.join(', ')}</td>
          <td>{merchant}</td>
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

export default TransactionTable;
