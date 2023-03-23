import React, { useState, useEffect, useRef, useContext } from 'react';
import 'chart.js/auto';
import { Line } from "react-chartjs-2";
import AuthContext from '../context/AuthContext';
import GraphSelect from '../components/GraphSelect';
import { useNavigate } from 'react-router-dom';

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
            {
                selectOptions === undefined || selectOptions === null
                ? null
                : <GraphSelect options={selectOptions} handleSelectionUpdate={handleSelectionUpdate} selectedOption={endpoint_parameter}/>
            }
            <Line data = {data}></Line>
        </div>
      )
    }

    export default LineGraph;
