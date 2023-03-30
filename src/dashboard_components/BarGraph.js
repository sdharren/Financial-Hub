import React, { useRef, useContext } from 'react';
import usePlaid from '../custom_hooks/usePlaid';
import { Bar, getElementsAtEvent } from 'react-chartjs-2';
import{ Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Colors
} from 'chart.js';


ChartJS.register(
  BarElement,
  CategoryScale,
  Colors,
  LinearScale,
  Tooltip,
  Legend
);

function BarGraph({endpoint, endpoint_parameter, loadNext}) {
  
  const [barChartData, error] = usePlaid({endpoint, endpoint_parameter, loadNext});

  let bar_data = [];
  let bar_labels = [];
  for (let key in barChartData) {
      bar_labels.push(barChartData[key].name);
      bar_data.push(barChartData[key].value);
  }

  const options = {
    plugins: {
      colors: {
        forceOverride: false
      },
      legend: {
        labels: {
          color: "white"
        }
      }
    },
    scales : {
      x : {
        grid : {
          color : 'black',
          display : false
        },
        ticks : {
          color : "white"
        }
      },
      y : {
        grid : {
          color : "black"
        },
        ticks : {
          color : "white"
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
      link: bar_labels,
      backgroundColor : ['#5fe35f']
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
    <div className='inline-block w-full max-h-[55vh]'>
      <Bar
      data = {data ? data : {}}
      options = {options ? options : {}}
      onClick = {onClick}
      width = '400vw'
      ref = {chartRef}></Bar>
    </div>
  );
}

export default BarGraph;
