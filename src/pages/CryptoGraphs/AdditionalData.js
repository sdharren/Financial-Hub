import React, { useContext, useState } from "react";
import AuthContext from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";

const CAdditional = () => {
    let {authTokens, logoutUser} = useContext(AuthContext);
    const [AdditionalData, setAdditionalData] = useState([]);
    const navigate = useNavigate()    
    
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
      <div className='overflow-hidden rounded border-gray-200'>
      <table className="transaction-table w-full h-[60vh] bg-transparent">
      <thead className='bg-gray-800 flex-[0_0_auto] text-white'>
        <tr>
          <th>Wallet</th>
          <th>Balance</th>
          <th>Number of Transactions</th>
          <th>Total Received</th>
          <th>Total Sent</th>
          <th className="pr-2">Coin Type</th>
        </tr>
      </thead>
      <tbody className='text-violet-300 overflow-y-scroll'>
        {Object.keys(AdditionalData).map((wallet, index) => (
          
          <tr key={index}>
            <td className="text-center">{wallet}</td>
            <td className="text-center">{AdditionalData[wallet][1] == "btc" ? "£" + (AdditionalData[wallet][0].final_balance/1e8).toLocaleString() : "£" + (AdditionalData[wallet][0].final_balance/1e18).toLocaleString()}</td>
            <td className="text-center">{AdditionalData[wallet][0].n_tx}</td>
            <td className="text-center">{AdditionalData[wallet][1] == "btc" ? (AdditionalData[wallet][0].total_received/1e8).toLocaleString() : (AdditionalData[wallet][0].total_received/1e18).toLocaleString()}</td>
            <td className="text-center">{AdditionalData[wallet][1] == "btc" ? (AdditionalData[wallet][0].total_sent/1e8).toLocaleString() : (AdditionalData[wallet][0].total_sent/1e18).toLocaleString()}</td>
            <td className="text-center">{AdditionalData[wallet][1]}</td>
          </tr>
        ))}
      </tbody>
    </table>
    </div>
    );
  };
  
  export default CAdditional;