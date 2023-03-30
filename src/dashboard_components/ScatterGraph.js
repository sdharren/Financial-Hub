import React, { useState, useEffect } from "react";
import ApexCharts from "react-apexcharts";
import usePlaid from "../custom_hooks/usePlaid";
import useHandleError from "../custom_hooks/useHandleError";

const CScatter = () => {
  const endpoint = "crypto_select_data";
  const endpoint_parameter = "txs";
  const [walletData, error] = usePlaid({endpoint, endpoint_parameter})
  useHandleError(error);

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
        text: "Date",
        style: {
          color: '#fff'
        }
      },
      labels: {
        style: {
          colors: '#fff'
        }
      }
    },
    yaxis: {
      title: {
        text: "Transaction Amount",
        style: {
          color: '#fff'
        }
      },
      labels: {
        formatter: function (value) {
          return value.toFixed(2);
      },
        style: {
          colors: '#fff'
        }
      }
    },
    legend: {
      position: "top",
      horizontalAlign: "left",
      labels: {
        colors: '#fff'
      }
    },
  };
  
  let series = [];

  if( walletData != null) {
    series = Object.keys(walletData).map((wallet) => {
      const data = Object.keys(walletData[wallet][0]).map((transaction) => {
          const isBtc = walletData[wallet][1] === "btc";
          return {
            y: isBtc ? walletData[wallet][0][transaction].total / 1e8 : walletData[wallet][0][transaction].total / 1e18,
            x: new Date(walletData[wallet][0][transaction].confirmed),
          };
        });
      return {
        name: wallet.slice(0,10) + "...",
        data: data,
      };
    });
  }

  return (
    <div id="chart" className='flex flex-col w-full max-h-[30vh]'>
        {
            walletData === null ?
            <p className='text-white'>Loading...</p> :
            <ApexCharts options={options} series={series} type="scatter" height= '450vh' />
        }
    </div>
  );
};

export default CScatter;