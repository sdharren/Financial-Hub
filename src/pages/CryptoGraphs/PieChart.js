import React, { useState, useEffect, useRef, useContext } from 'react';
import AuthContext from '../../context/AuthContext';
import {useNavigate} from 'react-router-dom';

import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
    Colors
} from 'chart.js'

import { Pie, getElementsAtEvent } from 'react-chartjs-2';


ChartJS.register(
    ArcElement,
    Tooltip,
    Legend,
    Colors
)
function CPie({endpoint, endpoint_parameter, loadNext, updateGraph, selectOptions}) {
    let {authTokens, logoutUser} = useContext(AuthContext);
    const [pieChartData, setPieChartData] = useState(null);
    const navigate = useNavigate()

    let get_data = async() =>  {
        let url = 'http://127.0.0.1:8000/api/crypto_select_data/?param=balance'
        let response = await fetch(url, {
            method:'GET',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer ' + String(authTokens.access)
            }
        });
        let data = await response.json();
        if (response.status === 200) {
            setPieChartData(data);
        }
        else if (response.status === 303) {
            if (data['error'] === 'Investments not linked.') {
                navigate('/crypto_wallets')
            }
        }
        else if (response.status == 429) {
            console.log("429 - Blockcypher token call limit")
        }
    }

    // if a user selects a different option from select dropdown - tell parent to update this graph
    let handleSelectionUpdate = async(nextParam) => {
        updateGraph({
            'endpoint': endpoint,
            'param': nextParam
        });
    }

    useEffect(() => {
        get_data();
    }, [endpoint, endpoint_parameter]);

    let pie_data = new Array();
    let pie_labels = new Array();
    for (let key in pieChartData) {
        let pieLabel = key + ' - ' + pieChartData[key][1]; 
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
            <Pie className='crypto-pie' height = "50vh" width = "50vh" data = {data} options = {options} ref = {chartRef} onClick = {onClick}></Pie>
        </div>
        
    ) 
    
}

export default CPie;