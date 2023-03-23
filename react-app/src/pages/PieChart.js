import React, { useState, useEffect, useRef, useContext } from 'react';
import AuthContext from '../context/AuthContext';
import {useNavigate} from 'react-router-dom';

import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
    Colors
} from 'chart.js'

import { Pie, getElementsAtEvent } from 'react-chartjs-2';
import GraphSelect from '../components/GraphSelect';
import usePlaid from '../custom_hooks/usePlaid';


ChartJS.register(
    ArcElement,
    Tooltip,
    Legend,
    Colors
)
function PieChart({endpoint, endpoint_parameter, loadNext, updateGraph, selectOptions}) {
    let {authTokens, logoutUser} = useContext(AuthContext);
    const [pieChartData, error] = usePlaid({ endpoint, endpoint_parameter });
    const navigate = useNavigate()

    let redirectToLink = async(assetType) => {
        console.log("here")
        let response = await fetch('http://127.0.0.1:8000/api/link_token/?product=' + assetType,
            {
                method:'GET',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':'Bearer ' + String(authTokens.access)
                }
            }
        )
        let data = await response.json();
        if (response.status === 200) {
            navigate('/plaid_link', {
                state: {link_token: data['link_token']},
                replace: true
            });
        }
    }

    if (error !== null) {
        let errorMessage = JSON.parse(error)['error'];
        if (errorMessage === 'Investments not linked.') {
            redirectToLink('investments');
        }
        else if (errorMessage === 'Transactions Not Linked.') {
            redirectToLink('transactions');
        }
    }

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
            // a section of pie chart has been clicked so tell parent to update the graph
            loadNext({
                'next': data.datasets[datasetIndex].link[dataIndex], // section that was clicked - this will be what the next graph is about
                'current': endpoint // current endpoint - to let the parent know what endpoint to query next
            });
        }
    };

    return (
        <div>
            {
                selectOptions !== undefined 
                ? <GraphSelect options={selectOptions} handleSelectionUpdate={handleSelectionUpdate} selectedOption={endpoint_parameter} />
                : null
            }
            {
                pieChartData === null ? 
                <p>Loading...</p> :  
                <Pie className='investment-pie' data = {data} options = {options} ref = {chartRef} onClick = {onClick}></Pie>
            }
        </div>
        
    ) 
    
}

export default PieChart;