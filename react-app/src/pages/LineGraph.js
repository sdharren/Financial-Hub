import React, { useState, useEffect, useRef, useContext } from 'react';
import 'chart.js/auto';
import Chart from "react-apexcharts";
import AuthContext from '../context/AuthContext';

function LineGraph({endpoint, endpoint_parameter, loadNext}) {
    let {authTokens, logoutUser} = useContext(AuthContext);
    const [lineGraphData, setLineGraphData] = useState(null);

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
    }

    useEffect(() => {
        get_data();
      }, [endpoint]); 

    // using built-in colors for now as otherwise they need to be hardcoded
    // make a selection of colors that match the UI theme later and replace
    var options = {
        series: [{
            data: lineGraphData
          }],
        chart: {
            id: 'area-datetime',
            type: 'line',
            height: 350,
            zoom: {
              autoScaleYaxis: true
            }
          },
        xaxis: {
            type: 'datetime',
            min: new Date('01 Mar 2012').getTime(),
            tickAmount: 6,
        },
        tooltip: {
            x: {
              format: 'dd MMM yyyy'
            }
        },
        fill: {
            type: 'gradient',
            gradient: {
              shadeIntensity: 1,
              opacityFrom: 0.7,
              opacityTo: 0.9,
              stops: [0, 100]
            }
          },
    };

    return <Chart options = {options}></Chart>
}

export default LineGraph;
