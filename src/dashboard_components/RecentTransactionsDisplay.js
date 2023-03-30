import React, { useState, useEffect, useContext } from 'react';
import useHandleError from '../custom_hooks/useHandleError';
import usePlaid from '../custom_hooks/usePlaid';
import { Typography, Table, TableBody, TableHead, TableRow, TableCell, TableContainer } from '@mui/material';

function RecentTransactions() {
  const endpoint = 'recent_transactions';
  const [transactionData, error] = usePlaid({endpoint});
  const [data, setData] = useState(null);
  
  useEffect(() => {
    setData(transactionData);
  }, [transactionData]);
 
  useHandleError(error);

  const styles = {
    container: {
      backgroundColor: 'transparent',
      boxShadow: 'none',
    },
    title: {
      textAlign: 'center',
      marginBottom: '1rem', // Add some margin below the title
      color: '#fff'
    },
    table: {
      backgroundColor: 'transparent',
      boxShadow: 'none',
    },
  };

  const categories = ['Institution', 'Amount (£)', 'Date', 'Category', 'Merchant'];

  return (
    <div styles={styles.container}>
    {
      data === null ? (
      <p className='text-white'>Loading...</p> 
      ) : (
      <TableContainer styles={styles.container} style = {{ maxHeight: '57vh'}}>
      <Typography variant="h6" style={styles.title}>
        Recent Transactions
      </Typography>
      <Table>
      <TableHead>
      <TableRow>
          {categories.map((category) => (
            <TableCell 
              key={category}
              style={{color: 'white', fontWeight: 'bold', fontSize: '0.9rem'}}
            >
              {category}
            </TableCell>
          ))}
        </TableRow>
      </TableHead>
      <TableBody>
        {Object.entries(data).map(([institution, transactions]) => (
          transactions.map((transaction, index) => (
            <TableRow key={`${institution}-${index}`}>
              <TableCell style={{color: 'white'}}>{institution}</TableCell>
              <TableCell style={{color: 'white'}}>{(transaction.amount.replace('£', '') * (-1))}</TableCell>
              <TableCell style={{color: 'white'}}>{transaction.date}</TableCell>
              <TableCell style={{color: 'white'}}>{transaction.merchant}</TableCell>
              <TableCell style={{color: 'white'}}>{transaction.category}</TableCell>
            </TableRow>
          ))
        ))}
      </TableBody>
      </Table>
      </TableContainer>
      )}
    </div>
  );
}

export default RecentTransactions;