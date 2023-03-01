import React, { useState, useEffect, useRef } from 'react';

import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
    Colors
} from 'chart.js'

import axios from 'axios';
import { Pie, getElementsAtEvent } from 'react-chartjs-2';


ChartJS.register(
    ArcElement,
    Tooltip,
    Legend,
    Colors
)
function PieChart({endpoint, endpoint_parameter, loadNext}) {
    const [pieChartData, setPieChartData] = useState(null);

    useEffect(() => {
        axios.get(
            'http://127.0.0.1:8000/api/' + String(endpoint) + '/',
            { params: {
                param: endpoint_parameter
            }}
        )
          .then(response => {
            setPieChartData(response.data);
          })
          .catch(error => {
            console.log(error);
          });
      }, [endpoint]);

    let pie_data = new Array();
    let pie_labels = new Array();
    for (let key in pieChartData) {
        pie_labels.push(key);
        pie_data.push(pieChartData[key]);
    }

    const data = {
        labels: pie_labels,
        datasets: [
            {
                label: '$$$',
                data: pie_data,
                borderColor: 'black',
                link: pie_labels
            }
        ]
    };
    // using built-in colors for now as otherwise they need to be hardcoded
    // make a selection of colors that match the UI theme later and replace
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

    return <Pie data = {data} options = {options} ref = {chartRef} onClick = {onClick}></Pie>
}

export default PieChart;