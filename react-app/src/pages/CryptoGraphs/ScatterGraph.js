import React from 'react';
import ApexCharts from 'apexcharts';
import { useState, useContext } from 'react';
import { AuthContext } from '../..//context/AuthContext';
import { useNavigate } from 'react-router-dom';

const ScatterGraph = () => {
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
        let url = 'http://127.0.0.1:8000/api/crypto_select_data?param=txs/'
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
            if (data['error'] === 'Investments not linked.') {
                navigate('/crypto_wallets')
            }
        }
    }
  
    React.useEffect(() => {
        get_data();
        let transactions = new Array();
        for (let key in scatterChartData) {
            for(let i = 0; i < scatterChartData[key].inputs.length; i++) {
                transactions.push({
                    type: 'input',
                    date: scatterChartData[key].inputs[i]['sequence'],
                    amount: scatterChartData[key].inputs[i]['output_value']
                });
            }

            for(let i = 0; i < scatterChartData[key].outputs.length; i++) {
                transactions.push({
                    type: 'output',
                    date: scatterChartData[key].outputs[i]['spent_by'],
                    amount: scatterChartData[key].outputs[i]['value']
                })
        }

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
  
      const data = {
          labels: scatter_labels,
          datasets: [
              {
                  label: '$$$',
                  data: scatter_data,
                  borderColor: 'black',
                  link: pie_labels
              }
          ]
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
  
      return () => {
        chart.destroy();
      };
    }, [transactions]);
  
    return <div ref={chartRef} />;
  };
  
  export default ScatterGraph;
  