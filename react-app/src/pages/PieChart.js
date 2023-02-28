import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend
} from 'chart.js'

import axios from 'axios';
import { Pie } from 'react-chartjs-2';
import React, { useState, useEffect } from 'react';

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
                backgroundColor: ['red', 'aqua', 'purple']
            }
        ]
    };
    const options = {};

    return <Pie data= {data} options = {options}></Pie>
}

export default PieChart;