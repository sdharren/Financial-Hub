import React from 'react';
import ApexCharts from 'apexcharts';
import { useState, useContext } from 'react';
import  AuthContext  from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

const CScatter = () => {
    const chartRef = React.useRef(null);
    let {authTokens, logoutUser} = useContext(AuthContext);
    const [scatterChartData, setScatterChartData] = useState(null);
    const navigate = useNavigate()
    
    /*
    const transactions = [
        { type: 'buy', date: '2022-01-01', amount: 10 },
        { type: 'sell', date: '2022-01-02', amount: 5 },
        { type: 'buy', date: '2022-01-03', amount: 20 },
        { type: 'sell', date: '2022-01-04', amount: 15 },
      ];
    */

    let get_data = async() =>  {
        let url = 'http://127.0.0.1:8000/api/crypto_select_data/?param=txs'
        let response = await fetch(url, {
            method:'GET',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer ' + String(authTokens.access)
            }
        });
        let data = await response.json();
        if (response.status === 200) {
            setScatterChartData(data);
        }
        else if (response.status === 303) {
            navigate('/link_assets')
        }
    }
  
    useEffect(() => {
        get_data();
    }, []);

    let transactions = new Array();

    for (let key in scatterChartData) {
        console.log(scatterChartData[key]);
        for(let i = 0; i < scatterChartData[key].inputs.length; i++) {
            transactions.push({
                type: 'input',
                date: scatterChartData[key].inputs[i]['receieved'],
                amount: scatterChartData[key].inputs[i]['total']
            });
        }

        for(let i = 0; i < scatterChartData[key].outputs.length; i++) {
            transactions.push({
                type: 'output',
                date: scatterChartData[key].outputs[i]['receieved'],
                amount: scatterChartData[key].outputs[i]['total']
            })
            
        }
    }
    console.log(transactions);
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
          data: transactions.filter((t) => t.type === 'input').map((t) => ({ x: t.date, y: t.amount })),
        },
        {
          name: 'Sell',
          data: transactions.filter((t) => t.type === 'output').map((t) => ({ x: t.date, y: t.amount })),
        },
      ];
  
      const chart = new ApexCharts(chartRef.current, {
        options,
        series,
      });
  
      chart.render();
  
      return <div ref={chartRef} />;
    };
  
  export default CScatter;
  