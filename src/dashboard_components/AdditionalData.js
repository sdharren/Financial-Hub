import React, { useState } from "react";
import { useEffect } from "react";
import usePlaid from '../custom_hooks/usePlaid';
import useHandleError from "../custom_hooks/useHandleError";
import { Typography, Table, TableBody, TableHead, TableRow, TableCell, TableContainer } from '@mui/material';

const CAdditional = () => {
    const endpoint = "crypto_all_data";
    const [additionalData, error] = usePlaid({endpoint});
    const [data, setData] = useState(null);
    useHandleError(error);
  
    useEffect(() => {
      setData(additionalData);
      }, [additionalData]);

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
    
      const categories = ['Wallet', 'Balance', 'Number of Transactions', 'Total Received', 'Total Sent', 'Type'];

    return (
      <div styles={styles.container}>
      {
        data === null ? (
        <p className='text-white'>Loading...</p> 
        ) : (
        <TableContainer styles={styles.container} style = {{ maxHeight: '57vh'}}>
        <Typography variant="h6" style={styles.title}>
          Wallet Data
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
          {Object.keys(data).map((wallet, index) => (
              <TableRow key={`${wallet}-${index}`}>
                <TableCell style={{color: 'white'}}>{wallet.slice(0,10) + '...'}</TableCell>
                <TableCell style={{color: 'white'}}>{data[wallet][1] == "btc" ? "£" + (data[wallet][0].final_balance/1e8).toLocaleString() : "£" + (data[wallet][0].final_balance/1e18).toLocaleString()}</TableCell>
                <TableCell style={{color: 'white'}}>{data[wallet][0].n_tx}</TableCell>
                <TableCell style={{color: 'white'}}>{data[wallet][1] == "btc" ? (data[wallet][0].total_received/1e8).toLocaleString() : (data[wallet][0].total_received/1e18).toLocaleString()}</TableCell>
                <TableCell style={{color: 'white'}}>{data[wallet][1] == "btc" ? (data[wallet][0].total_sent/1e8).toLocaleString() : (data[wallet][0].total_sent/1e18).toLocaleString()}</TableCell>
                <TableCell style={{color: 'white'}}>{data[wallet][1]}</TableCell>
              </TableRow>
            )
          )}
        </TableBody>
        </Table>
        </TableContainer>
        )}
      </div>
    );
  };
  
  export default CAdditional;