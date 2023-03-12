import React, { useState, useEffect, useRef, useContext } from 'react';
import AuthContext from '../context/AuthContext';
import axios from 'axios';

function TransactionsList({endpoint, endpoint_parameter, loadNext}) {
    let {authTokens, logoutUser} = useContext(AuthContext);
    const [listData, setListData] = useState(null);

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
            setPieChartData(data);
        }
        else if (response.status === 303) {
            //TODO: redirect to plaid link investments
            if (data['error'] === 'Transactions not linked.') {
                console.log('investments not linked');
            }
        }
    }
