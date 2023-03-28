import React from 'react';
import ApexCharts from 'apexcharts-react';

function BubbleChart () {
  const options = {
    chart: {
      type: 'bubble',
      height: 350,
    },
    series: [
      {
        name: 'Stocks',
        data: [
          { x: 'AAPL', y: 300, z: 50 },
          { x: 'AMZN', y: 600, z: 80 },
          { x: 'GOOG', y: 500, z: 60 },
        ],
      },
      {
        name: 'Bank Accounts',
        data: [
          { x: 'Savings', y: 150, z: 30 },
          { x: 'Checking', y: 200, z: 40 },
        ],
      },
      {
        name: 'Crypto',
        data: [
          { x: 'BTC', y: 1000, z: 70 },
          { x: 'ETH', y: 800, z: 50 },
        ],
      },
    ],
    dataLabels: {
      enabled: false,
    },
    fill: {
      opacity: 0.8,
    },
    title: {
      text: 'Bubble Chart for Stocks, Bank Accounts, and Crypto',
      align: 'center',
      style: {
        fontSize: '20px',
        fontWeight: 'bold',
      },
    },
    xaxis: {
      tickPlacement: 'on',
    },
    yaxis: {
      tickAmount: 5,
      labels: {
        formatter: function (val) {
          return val.toFixed(0) + ' USD';
        },
      },
    },
    tooltip: {
      y: {
        formatter: function (val) {
          return val.toFixed(0) + ' USD';
        },
      },
    },
  };

  return (
    <ApexCharts
      options={options}
      series={options.series}
      type="bubble"
      height={350}
    />
  );
};

export default BubbleChart;
