import React from 'react';
import ApexCharts from 'apexcharts';

const CryptoScatterGraph = () => {
    const chartRef = React.useRef(null);

    const transactions = [
        { type: 'buy', date: '2022-01-01', amount: 10 },
        { type: 'sell', date: '2022-01-02', amount: 5 },
        { type: 'buy', date: '2022-01-03', amount: 20 },
        { type: 'sell', date: '2022-01-04', amount: 15 },
      ];
  
    React.useEffect(() => {
      const options = {
        chart: {
          type: 'scatter',
          zoom: {
            enabled: true,
            type: 'xy',
          },
        },
        xaxis: {
          title: {
            text: 'Date',
          },
        },
        yaxis: {
          title: {
            text: 'Amount',
          },
        },
      };
  
      const series = [
        {
          name: 'Buy',
          data: transactions.filter((t) => t.type === 'buy').map((t) => ({ x: t.date, y: t.amount })),
        },
        {
          name: 'Sell',
          data: transactions.filter((t) => t.type === 'sell').map((t) => ({ x: t.date, y: t.amount })),
        },
      ];
  
      const chart = new ApexCharts(chartRef.current, {
        options,
        series,
      });
  
      chart.render();
  
      return () => {
        chart.destroy();
      };
    }, [transactions]);
  
    return <div ref={chartRef} />;
  };
  
  <CryptoScatterGraph />
  