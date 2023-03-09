import React, { useState, useEffect, useRef, useContext } from 'react';
import AuthContext from '../context/AuthContext';


import{ Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Colors
} from 'chart.js'
import { Bar, getElementsAtEvent } from 'react-chartjs-2';
ChartJS.register(
  BarElement,
  CategoryScale,
  Colors,
  LinearScale,
  Tooltip,
  Legend
);

function BarGraph({endpoint, endpoint_parameter, loadNext}) {
  let {authTokens, logoutUser} = useContext(AuthContext);
  const [barChartData, setBarChartData] = useState(null);

  let get_data = async() =>  {
    let url = 'http://127.0.0.1:8000/api/' + String(endpoint) + (endpoint_parameter != null ? '?param='+endpoint_parameter : '/')
    let response = await fetch(url, {
        method:'GET',
        headers:{
            'Content-Type':'application/json',
            'Authorization':'Bearer ' + String(authTokens.access)
        }
    });
    let data = await response.json();
    if (response.status === 200) {
        setBarChartData(data);
    }
}

useEffect(() => {
  get_data();
}, [endpoint]);

  let bar_data = [];
  let bar_labels = [];
  for (let key in barChartData) {
      bar_labels.push(barChartData[key].name);
      bar_data.push(barChartData[key].value);
  }
  console.log(bar_labels);
  console.log(bar_data);


  const options = {
      plugins: {
          colors: {
              forceOverride: true
          },
          legend: {
              labels: {
                  color: "white"
              }
          }
        }
  };

  const data = {
    labels : bar_labels,
    datasets : [{
      label : 'spending',
      data : bar_data,
      borderColor : 'black',
      link: bar_labels
    }]
  }

  const chartRef = useRef();
  const onClick = (event) => {
      if (getElementsAtEvent(chartRef.current, event).length > 0) {
          const datasetIndex = getElementsAtEvent(chartRef.current, event)[0].datasetIndex;
          const dataIndex = getElementsAtEvent(chartRef.current, event)[0].index;
          loadNext({
              'next': data.datasets[datasetIndex].link[dataIndex],
              'current': endpoint
          });
      }
  };

  return (
    <div>
      <Bar
      data = {data}
      options = {options}
      onClick = {onClick}
      ref = {chartRef}></Bar>
    </div>
  );
}

export default BarGraph;
