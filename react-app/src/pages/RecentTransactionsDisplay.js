

// const transactions = {
//   'Royal Bank of Scotland - Current Accounts': [
//     {
//       amount: '$896.65',
//       date: new Date(2023, 2, 12),
//       category: ['Transfer', 'Debit'],
//       merchant: 'Bank Of Switzerland'
//     },
//     {
//       amount: '£398.34',
//       date: new Date(2023, 2, 12),
//       category: ['Food and Drink', 'Restaurants', 'Fast Food'],
//       merchant: 'Eat Tokyo'
//     },
//     {
//       amount: '₹1708.12',
//       date: new Date(2023, 2, 12),
//       category: ['Food and Drink', 'Restaurants'],
//       merchant: 'Burger and Lobster'
//     },
//     {
//       amount: '1109.01',
//       date: new Date(2023, 2, 12),
//       category: ['Transfer', 'Debit'],
//       merchant: 'Not provided'
//     }
//   ]
// };


// const TransactionTable = () => {
//   const renderTableHeader = () => {
//     return (
//       <tr>
//         <th>Amount</th>
//         <th>Date</th>
//         <th>Category</th>
//         <th>Merchant</th>
//       </tr>
//     );
//   }

//   const renderTableData = () => {
//     return transactions['Royal Bank of Scotland - Current Accounts'].map(({ amount, date, category, merchant }) => {
//       return (
//         <tr key={amount}>
//           <td>{amount}</td>
//           <td>{date.toLocaleDateString()}</td>
//           <td>{category.join(', ')}</td>
//           <td>{merchant}</td>
//         </tr>
//       );
//     });
//   }

//   return (
//     <table className="transaction-table">
//       <thead>{renderTableHeader()}</thead>
//       <tbody>{renderTableData()}</tbody>
//     </table>
//   );
// };

import React, { useState, useEffect, useContext } from 'react';
import AuthContext from '../context/AuthContext';

function RecentTransactions() {
  let {authTokens, logoutUser} = useContext(AuthContext);
  const [transactions, setTransactions] = useState([]);
  const [institutionName, setInstitutionName] = useState('');

  useEffect(() => {
    async function fetchTransactions() {
      let transactionURL = 'http://127.0.0.1:8000/api/recent_transactions/?param=Royal Bank of Scotland - Current Accounts';
      const response = await fetch(transactionURL, {
        method: 'GET',
        headers: {
          'Content-Type':'application/json',
          'Authorization':'Bearer ' + String(authTokens.access)
        },
      });
      if (!response.ok) {
        console.error(`Failed to fetch recent transactions: ${response.status} ${response.statusText}`);
        return;
      }
    
      const data = await response.json();
      console.log(data);
      const transactionList = Object.values(data)[0].flatMap((category) =>
        category.map((transaction) => ({ ...transaction }))
      );
      if (Array.isArray(transactionList)) {
        setTransactions(transactionList);
      } else {
        console.error(`Failed to fetch recent transactions: transactionList is not an array`);
      }
    }

    fetchTransactions();
  }, []);

  return (
    <table>
      <thead>
        <tr>
          <th>Date</th>
          <th>Merchant</th>
          <th>Category</th>
          <th>Amount</th>
        </tr>
      </thead>
      {transactions.length > 0 ? (
        <tbody>
          {transactions.map(transaction => (
            <tr key={transaction.id}>
              <td>{transaction.amount}</td>
              <td>{transaction.category}</td>
              <td>{transaction.date}</td>
              <td>{transaction.merchant}</td>
            </tr>
          ))}
        </tbody>
      ) : null}
    </table>
  );
}

export default RecentTransactions;