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

  return (
    <div>
      {transactions.map((wallet, walletIndex) => (
        <div key={walletIndex}>
          <h2>Wallet: {wallet.address}</h2>
          <table>
            <thead>
              <tr>
                <th>Block Hash</th>
                <th>Block Height</th>
                <th>Confidence</th>
                <th>Confirmations</th>
                <th>Confirmed</th>
                <th>Double Spend</th>
                <th>Fees</th>
              </tr>
            </thead>
            <tbody>
              {wallet.txs.map((transaction, transactionIndex) => (
                <tr key={transactionIndex}>
                  <td>{transaction.block_hash}</td>
                  <td>{transaction.block_height}</td>
                  <td>{transaction.confidence}</td>
                  <td>{transaction.confirmations}</td>
                  <td>{transaction.confirmed}</td>
                  <td>{transaction.double_spend ? "Yes" : "No"}</td>
                  <td>{transaction.fees}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
};

export default CRecentTransactionsDisplay;
