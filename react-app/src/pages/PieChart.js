import React, { useState, useEffect, useRef } from 'react';

import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend
} from 'chart.js'

import axios from 'axios';
import { Pie, getElementsAtEvent } from 'react-chartjs-2';


ChartJS.register(
    ArcElement,
    Tooltip,
    Legend
)
function PieChart({endpoint}) {
    const [pieChartData, setPieChartData] = useState(null);
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/' + String(endpoint) + '/')
          .then(response => {
            setPieChartData(response.data);
          })
          .catch(error => {
            console.log(error);
          });
      }, []);

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
                backgroundColor: ['red', 'aqua', 'purple'],
                link: pie_labels
            }
        ]
    };
    const options = {};
    const chartRef = useRef();
    const onClick = (event) => {
        if (getElementsAtEvent(chartRef.current, event).length > 0) {
            const datasetIndex = getElementsAtEvent(chartRef.current, event)[0].datasetIndex;
            const dataIndex = getElementsAtEvent(chartRef.current, event)[0].index;
            console.log(data.datasets[datasetIndex].link[dataIndex])
        }
    };

    return <Pie data = {data} options = {options} ref = {chartRef} onClick = {onClick}></Pie>
}

export default PieChart;