import React, { useState, useEffect, useRef, useContext } from 'react';
import AuthContext from '../context/AuthContext';
import {useNavigate} from 'react-router-dom';


function DebitAccounts({endpoint, endpoint_parameter, loadNext}) {
    let {authTokens, logoutUser} = useContext(AuthContext);
    const [debitList, setDebitList] = useState([]);
    const navigate = useNavigate()

    let get_data = async() =>  {
        let url = 'api/' + String(endpoint) + (endpoint_parameter != null ? '?param='+endpoint_parameter : '/')
        let response = await fetch(url, {
            method:'GET',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer ' + String(authTokens.access)
            }
        });
        let data = await response.json();
        if (response.status === 200) {
            setDebitList(data);
        }
    }

    useEffect(() => {
        get_data();
      }, [endpoint, endpoint_parameter]);
}