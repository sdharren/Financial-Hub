import React, { useState, useEffect, useContext } from 'react';
import AuthContext from '../context/AuthContext';

const usePlaid = ({endpoint, endpoint_parameter, loadNext}) => {
    let {authTokens, logoutUser} = useContext(AuthContext);
    const [data, setData] = useState(null);

    useEffect(() => {
        let url = 'http://127.0.0.1:8000/api/' + String(endpoint) + (endpoint_parameter != null ? '?param='+endpoint_parameter : '/')
        fetch(url, {
                method:'GET',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':'Bearer ' + String(authTokens.access)
            }
        })
          .then(async (response) => {
          if (response.ok) setData(await response.json());
        });
      }, [endpoint]);

      return data;
};

export default usePlaid;