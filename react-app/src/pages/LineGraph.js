import React, { useState, useEffect, useRef, useContext } from 'react';
import Chart from "react-apexcharts";
import usePlaid from '../custom_hooks/usePlaid';
import 'chart.js/auto';
import { Line } from "react-chartjs-2";
import AuthContext from '../context/AuthContext';
import GraphSelect from '../components/GraphSelect';
import { useNavigate } from 'react-router-dom';

function LineGraph({endpoint, endpoint_parameter, updateGraph, selectOptions}) {
    const [lineChartData, error] = usePlaid({endpoint, endpoint_parameter})

    var chartCategories = [], chartSeries = [];
    for (var key in lineChartData) {
        if ( ! lineChartData.hasOwnProperty(key)) {
            continue;
        }
        chartSeries.push(lineChartData[key].toFixed(2));
        chartCategories.push(key.slice(0, 10));
    }

    // Set the options for the chart
    const options = {
        chart: {
            id: 'area-datetime',
            height: 350,
            zoom: {
                autoScaleYaxis: true
            },
        },
        title: {
            text: endpoint_parameter + " " + "Stock Price",
            offsetX: 0,
            offsetY: 0,
            style: {
                color: '#fff',
                fontSize: '12px',
                fontFamily: 'Helvetica, Arial, sans-serif',
                fontWeight: 600,
                cssClass: 'apexcharts-xaxis-title',
            },
        },
        yaxis: {
            show: true,
            showAlways: true,
            tickAmount: 6,
            labels: {
                show: true,
                align: 'right',
                minWidth: 0,
                maxWidth: 160,
                style: {
                    colors: ['#fff'],
                    fontSize: '12px',
                    fontFamily: 'Helvetica, Arial, sans-serif',
                    fontWeight: 400,
                    cssClass: 'apexcharts-yaxis-label',
                },
                offsetX: 0,
                offsetY: 0,
                rotate: 0,
            },
            axisBorder: {
                show: true,
                color: '#fff',
                offsetX: 0,
                offsetY: 0
            },
        },
            colors: ['#FDD36A'],
            stroke: {
            curve: 'straight',
            },
            xaxis: {
                categories: chartCategories,
            },
            dataLabels: {
                enabled: false
            },
            fill: {
                type: 'gradient',
                gradient: {
                    type: 'vertical',
                    shadeIntensity: 0.3,
                    opacityFrom: 0.7,
                    opacityTo: 0.9,
                    stops: [0, 100]
                }
            },
    };

const LineGraph = ({endpoint, endpoint_parameter, updateGraph, selectOptions}) => {
    let {authTokens, logoutUser} = useContext(AuthContext);
    const [lineGraphData, setLineGraphData] = useState(null);
    const navigate = useNavigate();

    let handleSelectionUpdate = async(nextParam) => {
        updateGraph({
            'endpoint': endpoint,
            'param': nextParam
        });
    }

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
            setLineGraphData(data);
        }
        else if (response.status === 303) {
            //TODO: redirect to plaid link investments
            if (data['error'] === 'Investments not linked.') {
                redirectToLink('investments');
            }
            else if (data['error'] === 'Transactions Not Linked.') {
                redirectToLink('transactions');
            }
        }
    }

    let redirectToLink = async(assetType) => {
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
    
        // Set the series data for the chart
        const series = [{
            name: 'Price',
            data: chartSeries,
        }];


      return (
        <div>
            {
                selectOptions === undefined || selectOptions === null
                ? null
                : <GraphSelect options={selectOptions} handleSelectionUpdate={handleSelectionUpdate} selectedOption={endpoint_parameter}/>
            }
            lineChartData == null ? <p>Loading...</p> :
            <Chart options={options} series={series} type = "area" />
        </div>
      )
    }
}

export default LineGraph;
