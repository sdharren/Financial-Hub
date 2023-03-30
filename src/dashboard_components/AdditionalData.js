import React, { useContext, useState } from "react";
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
    
      const categories = ['Wallet', 'Balance', 'Number of Transactions', 'Total Received', 'Total Sent'];

    // return (
    //   <div className='overflow-hidden rounded border-gray-200'>
    //   <table className="transaction-table w-full h-[60vh] bg-transparent">
    //   <thead className='bg-gray-800 flex-[0_0_auto] text-white'>
    //     <tr>
    //       <th>Wallet</th>
    //       <th>Balance</th>
    //       <th>Number of Transactions</th>
    //       <th>Total Received</th>
    //       <th>Total Sent</th>
    //       <th className="pr-2">Coin Type</th>
    //     </tr>
    //   </thead>
    //   <tbody className='text-violet-300 overflow-y-scroll'>
    //     {Object.keys(AdditionalData).map((wallet, index) => (
          
    //       <tr key={index}>
    //         <td className="text-center">{wallet}</td>
    //         <td className="text-center">{AdditionalData[wallet][1] == "btc" ? "£" + (AdditionalData[wallet][0].final_balance/1e8).toLocaleString() : "£" + (AdditionalData[wallet][0].final_balance/1e18).toLocaleString()}</td>
    //         <td className="text-center">{AdditionalData[wallet][0].n_tx}</td>
    //         <td className="text-center">{AdditionalData[wallet][1] == "btc" ? (AdditionalData[wallet][0].total_received/1e8).toLocaleString() : (AdditionalData[wallet][0].total_received/1e18).toLocaleString()}</td>
    //         <td className="text-center">{AdditionalData[wallet][1] == "btc" ? (AdditionalData[wallet][0].total_sent/1e8).toLocaleString() : (AdditionalData[wallet][0].total_sent/1e18).toLocaleString()}</td>
    //         <td className="text-center">{AdditionalData[wallet][1]}</td>
    //       </tr>
    //     ))}
    //   </tbody>
    // </table>
    // </div>
    // );

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
          {Object.entries(data).map((wallet, index) => (
              <TableRow key={`${wallet}-${index}`}>
                <TableCell style={{color: 'white'}}>{wallet}</TableCell>
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