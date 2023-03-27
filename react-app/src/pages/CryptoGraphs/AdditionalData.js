import React, { useContext, useState } from "react";
import AuthContext from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";

const CAdditional = () => {
    let {authTokens, logoutUser} = useContext(AuthContext);
    const [AdditionalData, setAdditionalData] = useState(null);
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
      console.log("hello");  
      get_data();
        
        let data = new Array();
        for (let key in AdditionalData) {
            data.push ({
                title: AdditionalData[key],
                value: AdditionalData[key][1]
            })

            setAdditionalData(data);
        }

        }, [AdditionalData]);
    


    return (
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(AdditionalData).map(([key, value]) => (
            <tr key={key}>
              <td>{key}</td>
              <td>{value}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };
  
  export default CAdditional;