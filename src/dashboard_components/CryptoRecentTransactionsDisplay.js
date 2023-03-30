import React from 'react';
import { useState } from 'react';
import { useEffect } from 'react';
import { useContext } from 'react';
import AuthContext from '../context/AuthContext';
import usePlaid from '../custom_hooks/usePlaid';
import useHandleError from '../custom_hooks/useHandleError';


const CRecentTransactionsDisplay = () => {

  const [transactions, error] = usePlaid();
  useHandleError(error);


  // let getTransactions = async () => {
  //   let transactionURL = 'http://127.0.0.1:8000/api/crypto_select_data/?param=txs';
  //   let response = await fetch(transactionURL, {
  //     method: 'GET',
  //     headers: {
  //       'Content-Type':'application/json',
  //       'Authorization':'Bearer ' + String(authTokens.access)
  //     },
  //   });
  //   let data = await response.json();
  //   if (response.status === 200) {
  //       setTransactions(data);
  //   }
  //   else {
  //     console.error(`Failed to fetch recent transactions: ${response.status} ${response.statusText}`);
  //   }

  //   }


  // useEffect(() => {
  //   getTransactions();
  // }, []);

  return (
    <div className='overflow-hidden rounded border-gray-200'>
      <table className="transaction-table w-full h-[60vh] bg-transparent">
        <thead className='bg-gray-800 flex-[0_0_auto] text-white'>
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
                  <td>{transactions[wallet][1] == "btc" ? new Date(transactions[wallet][0][subheading].confirmed).toLocaleString() : new Date(transactions[wallet][0][subheading].confirmed).toLocaleString()}</td>
                  <td>{transactions[wallet][1] == "btc" ? transactions[wallet][0][subheading].fees : transactions[wallet][0][subheading].fees/1e18}</td>
                  <td>{transactions[wallet][1] == "btc" ? transactions[wallet][0][subheading].total/1e8 : transactions[wallet][0][subheading].total/1e18}</td>
                  <td>{transactions[wallet][1]}</td>
                </tr>
              ))}
            </React.Fragment>
          ))}
        </tbody>
      </table>
    </div>

  );
};

export default CRecentTransactionsDisplay;
