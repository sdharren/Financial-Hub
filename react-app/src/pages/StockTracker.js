import React, { useState, useEffect, useRef, useContext } from 'react';
import{ Chart as ChartJS, Tooltip, Legend, Colors } from 'chart.js';
import { Line } from "react-chartjs-2";

const StockTracker = ({endpoint, loadNext}) => {
    let {authTokens, logoutUser} = useContext(AuthContext);
    const [lineGraphData, setLineGraphData] = useState(null);

    let get_data = async() =>  {
        let url = 'http://127.0.0.1:8000/api/' + String(endpoint) + '/'
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
}
