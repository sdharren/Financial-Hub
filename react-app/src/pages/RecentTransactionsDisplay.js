
import React, { useState, useEffect, useContext } from 'react';
import AuthContext from '../context/AuthContext';

function RecentTransactions() {
  let {authTokens, logoutUser} = useContext(AuthContext);
  const [transactions, setTransactions] = useState([]);



  let getTransactions = async () => {
    let transactionURL = 'http://127.0.0.1:8000/api/recent_transactions/?param=Royal Bank of Scotland - Current Accounts';
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



  return (
    <div>
    <table>
      <thead>
        <tr>
          <th>Merchant</th>
          <th>Category</th>
          <th>Amount</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody>
          {transactions.map(transaction => (
            <tr key={transaction.merchant}>
              <td>{transaction.merchant}</td>
              <td>{transaction.category.join(', ')}</td>
              <td>{transaction.amount}</td>
              <td>{transaction.date}</td>
            </tr>
          ))}
      </tbody>
    </table>
    </div>
  );
}

export default RecentTransactions;