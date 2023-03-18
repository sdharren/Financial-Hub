import React, { useState, useEffect, useRef, useContext } from 'react';
import 'chart.js/auto';
import { Line } from "react-chartjs-2";
import AuthContext from '../context/AuthContext';


const LineGraph = ({endpoint, endpoint_parameter, loadNext}) => {
    let {authTokens, logoutUser} = useContext(AuthContext);
    const [lineGraphData, setLineGraphData] = useState(null);

    let get_data = async() =>  {
        console.log("getting data")
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
    }, [endpoint, endpoint_parameter]);

    let line_data = new Array();
    let line_labels = new Array();
    for (let key in lineGraphData) {
        line_labels.push(key);
        line_data.push(lineGraphData[key]);
    }

    const data = {
        labels: line_labels,
        datasets: [{
          label: endpoint_parameter + " " + 'Stock Price',
          data: line_data,
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        }]
      };
    
      return <Line data = {data}></Line>
    }

    export default LineGraph;
