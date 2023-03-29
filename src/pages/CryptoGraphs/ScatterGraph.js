import React, { useState, useEffect } from "react";
import { useContext } from 'react';
import AuthContext from '../../context/AuthContext';
import ApexCharts from "react-apexcharts";


const CScatter = () => {
  const [walletData, setWalletData] = useState([]);
  let {authTokens, logoutUser} = useContext(AuthContext);

    let get_data = async () => {
        let transactionURL = 'http://127.0.0.1:8000/api/crypto_select_data/?param=txs';
        let response = await fetch(transactionURL, {
        method: 'GET',
        headers: {
            'Content-Type':'application/json',
            'Authorization':'Bearer ' + String(authTokens.access)
        },
        });
        let data = await response.json();
        if (response.status === 200) {
            setWalletData(data);
        }
        else {
        console.error(`Failed to fetch recent transactions: ${response.status} ${response.statusText}`);
        }
    };

  useEffect(() => {
    get_data();
  }, []);

  const options = {
    chart: {
      // height: 100,
      type: "scatter",
      zoom: {
        enabled: true,
        type: "xy"
      },
    },
    xaxis: {
      type: "datetime",
      title: {
        text: "Date"
      }
    },
    yaxis: {
      title: {
        text: "Transaction Amount",
      },
    },
    legend: {
      position: "top",
      horizontalAlign: "left",
    },
  };

  const series = Object.keys(walletData).map((wallet) => {
    const data = Object.keys(walletData[wallet][0]).map((transaction) => {
        const isBtc = walletData[wallet][1] === "btc";
        return {
          y: isBtc ? walletData[wallet][0][transaction].total / 1e8 : walletData[wallet][0][transaction].total / 1e18,
          x: new Date(walletData[wallet][0][transaction].confirmed),
        };
      });      
    console.log(data);
    return {
      name: wallet,
      data: data,
    };
  });

  return (
    <div id="chart" className='flex flex-col w-full max-h-[30vh]'>
      <ApexCharts options={options} series={series} type="scatter" height= '450vh' />
    </div>
  );
};

export default CScatter;