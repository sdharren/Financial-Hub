
import React from 'react';
import '../table.css';

const transactions = {
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



const TransactionTable = () => {
  const renderTableHeader = () => {
    let headers = ["Amount", "Date", "Category", "Merchant"]
    return (
      <tr>
        {headers.map((header) => (<th className='text-left py-3 px-4 uppercase font-semibold text-sm'>{header}</th>))}
      </tr>
    );
  }

  const renderTableData = () => {
    return transactions['Royal Bank of Scotland - Current Accounts'].map(({ amount, date, category, merchant }) => {

      return (
        <tr className='hover:bg-neutral-100' key={amount}>
          <td className='text-left py-3 px-4'>{amount}</td>
          <td className='text-left py-3 px-4'>{date.toLocaleDateString()}</td>
          <td className='text-left py-3 px-4'>{category.join(', ')}</td>
          <td className='text-left py-3 px-4'>{merchant}</td>
        </tr>
      );
    });
  }

  return (
    <div className='shadow overflow-hidden rounded border-b border-gray-200'>
      <table className="transaction-table min-w-full bg-white">
        <thead className='bg-gray-800 text-white'>{renderTableHeader()}</thead>
        <tbody className='text-gray-700'>{renderTableData()}</tbody>
      </table>
    </div>
  );
};

export default TransactionTable;
