import React, { useState, useEffect, useContext } from 'react';
import useHandleError from '../custom_hooks/useHandleError';
import usePlaid from '../custom_hooks/usePlaid';
import { Table, TableBody, TableHead, TableRow, TableCell, TableSortLabel } from '@mui/material';

function RecentTransactions() {
  const endpoint = 'recent_transactions';
  const [data, setData] = useState(usePlaid({endpoint}));
 
  useHandleError(data[1]);

  const categories = ['Institution', 'Amount', 'Date', 'Category', 'Merchant'];

  const [sort, setSort] = useState({ category: '', direction: 'asc' });
  
  const sortData = (category, direction) => {
    const sortedData = [...data[0]].sort((a, b) => {
      if (a[category] < b[category]) return direction === 'asc' ? -1 : 1;
      if (a[category] > b[category]) return direction === 'asc' ? 1 : -1;
      return 0;
    });
    setData(sortedData);
    setSort({ category, direction });
  };

  return (
    <div>
    {
      data[0] === null ?
      <p>Loading...</p> :
      <Table>
      <TableHead>
        <TableRow>
          {categories.map((category) => (
            <TableCell key={category}>
              <TableSortLabel
                active={sort.category === category}
                direction={sort.direction}
                onClick={() => {
                  const direction = sort.category === category ? sort.direction === 'asc' ? 'desc' : 'asc' : 'asc';
                  sortData(category, direction);
                }}
              >
                {category}
              </TableSortLabel>
            </TableCell>
          ))}
        </TableRow>
      </TableHead>
      <TableBody>
        {data[0].map((item, index) => (
          <TableRow key={index}>
            {categories.map((category) => (
              <TableCell key={`${index}-${category}`}>
                {item[category]}
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
      }
    </div>
  );
}

export default RecentTransactions;