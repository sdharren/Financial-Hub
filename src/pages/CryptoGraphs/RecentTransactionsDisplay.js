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
    getTransactions();
  }, []);

  return (
    <table>
      <thead>
        <tr>
          <th>From Address</th>
          <th>To Addresses</th>
          <th>Confirmations</th>
          <th>Confirmed</th>
          <th>Fees</th>
          <th>Total</th>
          <th>Coin Type</th>
        </tr>
      </thead>
      <tbody>
        {Object.keys(transactions).map((wallet, index) => (
          <React.Fragment key={index}>
            {Object.keys(transactions[wallet][0]).map((subheading, subindex) => (
              <tr key={subindex}>
                <td>{subindex === 0 ? wallet : ''}</td>
                <td>
                  <a href={'https://www.blockchain.com/explorer/transactions/btc/' + (transactions[wallet][0][subheading].hash)}>
                    {(transactions[wallet][0][subheading].addresses).length}
                  </a>
                </td>
                <td>{transactions[wallet][0][subheading].confirmations.toLocaleString()}</td>
                <td>{new Date(transactions[wallet][0][subheading].confirmed).toLocaleString()}</td>
                <td>{transactions[wallet][0][subheading].fees}</td>
                <td>{transactions[wallet][1] == "btc" ? transactions[wallet][0][subheading].total/1e8 : transactions[wallet][0][subheading].total/1e18}</td>
                <td>{transactions[wallet][1]}</td>
              </tr>
            ))}
          </React.Fragment>
        ))}
      </tbody>
    </table>

  );
};

export default CRecentTransactionsDisplay;
