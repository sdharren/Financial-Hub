import React, { useState, useEffect, useRef, useContext } from 'react';
import { Pie, getElementsAtEvent } from 'react-chartjs-2';
import GraphSelect from '../components/GraphSelect';
import usePlaid from '../custom_hooks/usePlaid';
import useHandleError from '../custom_hooks/useHandleError';
import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
    Colors
} from 'chart.js';


ChartJS.register(
    ArcElement,
    Tooltip,
    Legend,
    Colors
)
function PieChart({endpoint, endpoint_parameter, loadNext, updateGraph, selectOptions, currency }) {
    const [pieChartData, error] = usePlaid({ endpoint, endpoint_parameter });
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
        pie_labels.push(key);
        pie_data.push(pieChartData[key]);
    }

    const data = {
        labels: pie_labels,
        datasets: [
            {
                label: currency ? currency : '£',
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
    const chartRef = useRef();
    const onClick = (event) => {
        if (getElementsAtEvent(chartRef.current, event).length > 0) {
            const datasetIndex = getElementsAtEvent(chartRef.current, event)[0].datasetIndex;
            const dataIndex = getElementsAtEvent(chartRef.current, event)[0].index;
            // a section of pie chart has been clicked so tell parent to update the graph
            loadNext({
                'next': data.datasets[datasetIndex].link[dataIndex], // section that was clicked - this will be what the next graph is about
                'current': endpoint // current endpoint - to let the parent know what endpoint to query next
            });
        }
    };

    return (
        <div className='inline-block min-h-[60vh] w-full max-h-[60vh]'>
            {
                selectOptions !== undefined
                ? <GraphSelect options={selectOptions} handleSelectionUpdate={handleSelectionUpdate} selectedOption={endpoint_parameter} />
                : null
            }
            {
                pieChartData === null ?
                <p className='text-white'>Loading...</p> :
                <Pie className='investment-pie' height = "50vh" width = "50vh" data = {data} options = {options} ref = {chartRef} onClick = {onClick}></Pie>
            }
        </div>

    )

}

export default PieChart;
