import React, { useState, useEffect, useContext } from 'react';
import useHandleError from '../custom_hooks/useHandleError';
import usePlaid from '../custom_hooks/usePlaid';
import { Typography, Table, TableBody, TableHead, TableRow, TableCell, TableSortLabel, TableContainer } from '@mui/material';

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
    },
    tableRow: {
      color: '#fff', // Set the color of the table rows to white
    },
    tableCell: {
      color: '#fff', // Set the color of the table rows to white
    },
    tableBody: {
      color: '#fff', // Set the color of the table rows to white
    },
    table: {
      backgroundColor: 'transparent',
      boxShadow: 'none',
    },
  };

  const categories = ['Institution', 'Amount', 'Date', 'Category', 'Merchant'];

  const [sort, setSort] = useState({ category: 'institution', direction: 'asc' });

  const sortData = (category) => {
    const isAscending = sort.category === category && sort.direction === 'asc';
    const sortedData = Object.entries(data).sort((a, b) => {
      const aValue = a[1][0][category];
      const bValue = b[1][0][category];
      if (aValue < bValue) {
        return isAscending ? -1 : 1;
      }
      if (aValue > bValue) {
        return isAscending ? 1 : -1;
      }
      return 0;
    });
    setSort({ category, direction: isAscending ? 'desc' : 'asc' });
    setData(Object.fromEntries(sortedData));
  };

  return (
    <div styles={styles.container}>
    {
      data === null ? (
      <p>Loading...</p> 
      ) : (
      <TableContainer styles={styles.container}>
      <Typography variant="h6" style={styles.title}>
        Recent Transactions
      </Typography>
      <Table style={styles.table}>
      <TableHead>
      <TableRow styles={styles.tableRow}>
          {categories.map((category) => (
            <TableCell key={category} styles={styles.tableCell}>
              <TableSortLabel
                active={sort.category === category}
                direction={sort.category === category ? sort.direction : 'asc'}
                onClick={() => sortData(category)}
              >
                {category}
              </TableSortLabel>
            </TableCell>
          ))}
        </TableRow>
      </TableHead>
      <TableBody styles={styles.tableBody}>
        {Object.entries(data).map(([institution, transactions]) => (
          transactions.map((transaction, index) => (
            <TableRow key={`${institution}-${index}`} styles={styles.tableRow}>
              <TableCell styles={styles.tableCell}>{institution}</TableCell>
              <TableCell styles={styles.tableCell}>{'£' + (transaction.amount.replace('£', '') * (-1))}</TableCell>
              <TableCell styles={styles.tableCell}>{transaction.date}</TableCell>
              <TableCell styles={styles.tableCell}>{transaction.merchant}</TableCell>
              <TableCell styles={styles.tableCell}>{transaction.category}</TableCell>
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