import React from 'react';
import { useEffect } from 'react';
import usePlaid from '../custom_hooks/usePlaid';
import useHandleError from '../custom_hooks/useHandleError';
import { Typography, Table, TableBody, TableHead, TableRow, TableCell, TableContainer } from '@mui/material';



const CRecentTransactionsDisplay = () => {
  const endpoint = "crypto_select_data";
  const endpoint_parameter = "txs";
  const [transactions, error] = usePlaid({endpoint, endpoint_parameter});
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

  const categories = ['From Address', 'To Address', 'Confirmations', 'Confirmed', 'Fees', 'Total', 'Coin'];

  return (
    <div styles={styles.container}>
    {
      transactions === null ? (
      <p className='text-white'>Loading...</p> 
      ) : (
      <TableContainer styles={styles.container} style = {{ maxHeight: '57vh'}}>
      <Typography variant="h6" style={styles.title}>
        Transactions
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
        {Object.keys(transactions).map((wallet, index) => (
          <React.Fragment>
            {Object.keys(transactions[wallet][0]).map((subheading, subindex) => (
            <TableRow key={subindex}>
              <TableCell style={{color: 'white'}}>{wallet.slice(0,10) + "..."}</TableCell>
              <TableCell style={{color: 'white'}}>
                <a href={'https://www.blockchain.com/explorer/transactions/btc/' + (transactions[wallet][0][subheading].hash)}>
                  {(transactions[wallet][0][subheading].addresses).length}
                </a>
              </TableCell>
              <TableCell style={{color: 'white'}}>{transactions[wallet][0][subheading].confirmations.toLocaleString()}</TableCell>
              <TableCell style={{color: 'white'}}>{transactions[wallet][1] == "btc" ? new Date(transactions[wallet][0][subheading].confirmed).toLocaleString() : new Date(transactions[wallet][0][subheading].confirmed).toLocaleString()}</TableCell>
              <TableCell style={{color: 'white'}}>{transactions[wallet][1] == "btc" ? transactions[wallet][0][subheading].fees : transactions[wallet][0][subheading].fees/1e18}</TableCell>
              <TableCell style={{color: 'white'}}>{transactions[wallet][1] == "btc" ? transactions[wallet][0][subheading].total/1e8 : transactions[wallet][0][subheading].total/1e18}</TableCell>
              <TableCell style={{color: 'white'}}>{transactions[wallet][1]}</TableCell>
            </TableRow>
          ))}
          </React.Fragment>
        ))}
      </TableBody>
      </Table>
      </TableContainer>
      )}
    </div>
  );
};

export default CRecentTransactionsDisplay;
