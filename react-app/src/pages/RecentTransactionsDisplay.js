
import React from 'react';
import '../static/css/table.css';

const transactions = {
  'Royal Bank of Scotland - Current Accounts': [
    {
      amount: '$896.65',
      date: new Date(2023, 2, 12),
      category: ['Transfer', 'Debit'],
      merchant: 'Bank Of Switzerland'
    },
    {
      amount: '£398.34',
      date: new Date(2023, 2, 12),
      category: ['Food and Drink', 'Restaurants', 'Fast Food'],
      merchant: 'Eat Tokyo'
    },
    {
      amount: '₹1708.12',
      date: new Date(2023, 2, 12),
      category: ['Food and Drink', 'Restaurants'],
      merchant: 'Burger and Lobster'
    },
    {
      amount: '1109.01',
      date: new Date(2023, 2, 12),
      category: ['Transfer', 'Debit'],
      merchant: 'Not provided'
    }
  ]
};



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
