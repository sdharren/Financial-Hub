import React, { useContext, useState } from "react";
import AuthContext from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";

const CAdditional = () => {
    let {authTokens, logoutUser} = useContext(AuthContext);
    const [AdditionalData, setAdditionalData] = useState([]);
    const navigate = useNavigate()
    /*
    const data = {
        name: 'John Doe',
        age: 30,
        email: 'johndoe@example.com',
      };
    */
    
    
    let get_data = async() =>  {
        let url = 'http://127.0.0.1:8000/api/crypto_all_data/'
        let response = await fetch(url, {
            method:'GET',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer ' + String(authTokens.access)
            }
        });
        let respData = await response.json();
        if (response.status === 200) {
            setAdditionalData(respData);
        }
        else if (response.status === 303) {
            if (respData['error'] === 'Investments not linked.') {
                navigate('/crypto_wallets')
            }
        }
    }
  
    useEffect(() => {
      get_data();
      }, []);


    return (
      <table>
      <thead>
        <tr>
          <th>Wallet</th>
          <th>Balance</th>
          <th>Number of Transactions</th>
          <th>Total Received</th>
          <th>Total Sent</th>
          <th>Coin Type</th>
        </tr>
      </thead>
      <tbody>
        {Object.keys(AdditionalData).map((wallet, index) => (
          
          <tr key={index}>
            <td>{wallet}</td>
            <td>{AdditionalData[wallet][1] == "btc" ? AdditionalData[wallet][0].final_balance/1e8 : AdditionalData[wallet][0].final_balance/1e18}</td>
            <td>{AdditionalData[wallet][0].n_tx}</td>
            <td>{AdditionalData[wallet][0].total_received}</td>
            <td>{AdditionalData[wallet][0].total_sent}</td>
            <td>{AdditionalData[wallet][1]}</td>
          </tr>
        ))}
      </tbody>
    </table>

    );
  };
  
  export default CAdditional;