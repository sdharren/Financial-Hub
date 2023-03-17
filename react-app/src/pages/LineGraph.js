import React, { useState, useEffect, useRef, useContext } from 'react';
import 'chart.js/auto';
import { Line } from "react-chartjs-2";
import AuthContext from '../context/AuthContext';
import InvestmentOptions from '../components/InvestmentOptions';

const LineGraph = ({endpoint, endpoint_parameter, loadNext, updateGraph, selectOptions}) => {
    let {authTokens, logoutUser} = useContext(AuthContext);
    const [lineGraphData, setLineGraphData] = useState(null);

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
    
      return (
        <div>
            {selectOptions===undefined||selectOptions===null?null:<InvestmentOptions options={selectOptions} handleSelectionUpdate={handleSelectionUpdate} selectedOption={endpoint_parameter}></InvestmentOptions>}
            <Line data = {data}></Line>
        </div>
      )
    }

    export default LineGraph;
