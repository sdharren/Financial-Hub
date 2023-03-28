import React, { useState, useEffect, useContext } from 'react';
import useHandleError from '../custom_hooks/useHandleError';
import usePlaid from '../custom_hooks/usePlaid';
import { Table, TableBody, TableHead, TableRow, TableCell, TableSortLabel, TableContainer } from '@mui/material';

function RecentTransactions() {
  const endpoint = 'recent_transactions';
  const [transactionData, error] = usePlaid({endpoint});
  const [data, setData] = useState(null);
  
  useEffect(() => {
    setData(transactionData);
  }, [transactionData]);
 
  useHandleError(error);

  const categories = ['Institution', 'Amount', 'Date', 'Category', 'Merchant'];

  // const [sort, setSort] = useState({ category: 'institution', direction: 'asc' });

  // const sortData = (category) => {
  //   const isAscending = sort.category === category && sort.direction === 'asc';
  //   const sortedData = Object.entries(data).sort((a, b) => {
  //     const aValue = a[1][0][category];
  //     const bValue = b[1][0][category];
  //     if (aValue < bValue) {
  //       return isAscending ? -1 : 1;
  //     }
  //     if (aValue > bValue) {
  //       return isAscending ? 1 : -1;
  //     }
  //     return 0;
  //   });
  //   setSort({ category, direction: isAscending ? 'desc' : 'asc' });
  //   setData(Object.fromEntries(sortedData));
  // };

  return (
    <div>
    {
      data === null ? (
      <p>Loading...</p> 
      ) : (
      <TableContainer style={{maxHeight: '57vh'}}>
      <Table stickyHeader>
      <TableHead>
      <TableRow>
          {categories.map((category) => (
            <TableCell key={category}>
              {/* <TableSortLabel
                active={sort.category === category}
                direction={sort.category === category ? sort.direction : 'asc'}
                onClick={() => sortData(category)}
              >
                {category}
              </TableSortLabel> */}
            </TableCell>
          ))}
        </TableRow>
      </TableHead>
      <TableBody>
        {Object.entries(data).map(([institution, transactions]) => (
          transactions.map((transaction, index) => (
            <TableRow key={`${institution}-${index}`}>
              <TableCell>{institution}</TableCell>
              <TableCell>{'£' + (transaction.amount.replace('£', '') * (-1))}</TableCell>
              <TableCell>{transaction.date}</TableCell>
              <TableCell>{transaction.merchant}</TableCell>
              <TableCell>{transaction.category}</TableCell>
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