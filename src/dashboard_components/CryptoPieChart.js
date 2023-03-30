import React from 'react';
import usePlaid from '../custom_hooks/usePlaid';

import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
    Colors
} from 'chart.js'

import { Pie } from 'react-chartjs-2';
import useHandleError from '../custom_hooks/useHandleError';


ChartJS.register(
    ArcElement,
    Tooltip,
    Legend,
    Colors
)
function CPie({updateGraph}) {
    const endpoint = "crypto_select_data";
    const endpoint_parameter = "balance";
    const [pieChartData, error] = usePlaid({endpoint, endpoint_parameter});
    useHandleError(error);

    // if a user selects a different option from select dropdown - tell parent to update this graph
    let handleSelectionUpdate = async(nextParam) => {
        updateGraph({
            'endpoint': endpoint,
            'param': nextParam
        });
    }

    let pie_data = new Array();
    let pie_labels = new Array();
    for (let key in pieChartData) {
        let pieLabel = key.slice(0,10) + "..." + ' - ' + pieChartData[key][1]; 
        pie_labels.push(pieLabel);
        var currVal = pieChartData[key][0];
        pie_data.push(currVal);
    }

    const data = {
        labels: pie_labels,
        datasets: [
            {
                label: '£',
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
        },
        responsive : true,
        maintainAspectRatio : false,
    };

    return (
        <div className='inline-block min-h-[60vh] w-full max-h-[60vh]'>
            {
                pieChartData === null ?
                <p className='text-white'>Loading...</p> :
                <Pie className='crypto-pie' height = "50vh" width = "50vh" data = {data} options = {options} ></Pie>
            }
        </div>
        
    ) 
    
}

export default CPie;