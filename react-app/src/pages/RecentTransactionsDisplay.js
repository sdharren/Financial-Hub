
import React, { useState, useEffect, useContext } from 'react';
import AuthContext from '../context/AuthContext';

const transactionss = {
  'Royal Bank of Scotland - Current Accounts': [
    {
      amount: '$896.65',
      date: new Date(2023, 2, 12),
      category: ['Transfer', 'Debit'],
      merchant: 'Bank Of Switzerland'
    },
    // {
    //   amount: '£398.34',
    //   date: new Date(2023, 2, 12),
    //   category: ['Food and Drink', 'Restaurants', 'Fast Food'],
    //   merchant: 'Eat Tokyo'
    // },
    // {
    //   amount: '₹1708.12',
    //   date: new Date(2023, 2, 12),
    //   category: ['Food and Drink', 'Restaurants'],
    //   merchant: 'Burger and Lobster'
    // },{
    //   amount: '₹1708.12',
    //   date: new Date(2023, 2, 12),
    //   category: ['Food and Drink', 'Restaurants'],
    //   merchant: 'Burger and Lobster'
    // },{
    //   amount: '₹1708.12',
    //   date: new Date(2023, 2, 12),
    //   category: ['Food and Drink', 'Restaurants'],
    //   merchant: 'Burger and Lobster'
    // },{
    //   amount: '₹1708.12',
    //   date: new Date(2023, 2, 12),
    //   category: ['Food and Drink', 'Restaurants'],
    //   merchant: 'Burger and Lobster'
    // },{
    //   amount: '₹1708.12',
    //   date: new Date(2023, 2, 12),
    //   category: ['Food and Drink', 'Restaurants'],
    //   merchant: 'Burger and Lobster'
    // },{
    //   amount: '₹1708.12',
    //   date: new Date(2023, 2, 12),
    //   category: ['Food and Drink', 'Restaurants'],
    //   merchant: 'Burger and Lobster'
    // },{
    //   amount: '₹1708.12',
    //   date: new Date(2023, 2, 12),
    //   category: ['Food and Drink', 'Restaurants'],
    //   merchant: 'Burger and Lobster'
    // },{
    //   amount: '₹1708.12',
    //   date: new Date(2023, 2, 12),
    //   category: ['Food and Drink', 'Restaurants'],
    //   merchant: 'Burger and Lobster'
    // },{
    //   amount: '₹1708.12',
    //   date: new Date(2023, 2, 12),
    //   category: ['Food and Drink', 'Restaurants'],
    //   merchant: 'Burger and Lobster'
    // },
    {
      amount: '1109.01',
      date: new Date(2023, 2, 12),
      category: ['Transfer', 'Debit'],
      merchant: 'Not provided'
    }
  ]
};

export default function RecentTransactions() {
  let {authTokens, logoutUser} = useContext(AuthContext);
  const [transactions, setTransactions] = useState([]);

  const renderTableHeader = () => {
    let headers = ["Merchant", "Catagory", "Amount", "Date"]
    return (
      <tr>
        {headers.map((header) => (<th className='text-left py-3 px-4 uppercase font-semibold text-sm'>{header}</th>))}
      </tr>
    );
  }

  const renderTableData = () => {
    return transactions.map(({ amount, date, category, merchant }) => {

      return (
        <tr className='hover:bg-neutral-100' key={merchant}>
          <td className='text-left py-3 px-4'>{merchant}</td>
          <td className='text-left py-3 px-4'>{category.join(', ')}</td>
          <td className='text-left py-3 px-4'>{amount}</td>
          <td className='text-left py-3 px-4'>{date}</td>
        </tr>
      );
    })
  }

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
    <div className='shadow overflow-hidden rounded border-b border-gray-200'>
      <table className="transaction-table min-w-full bg-white">
        <thead className='bg-gray-800 text-white'>
          {renderTableHeader()}
        </thead>
        <tbody className='text-gray-700'>
          {renderTableData()}
        </tbody>
      </table>
    </div>
  );
}
