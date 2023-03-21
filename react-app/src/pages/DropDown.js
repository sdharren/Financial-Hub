import React, { useState, useEffect, useRef, useContext } from 'react';
import AuthContext from '../context/AuthContext';

function DropDown({endpoint, endpoint_parameter, loadNext}) {
  let {authTokens, logoutUser} = useContext(AuthContext);
  const [data, setData] = useState([]);

  async function getData() {
    let url = 'http://127.0.0.1:8000/api/select_bank_account'
    let response = await fetch(url, {
      method:'GET',
      headers:{
        'Content-Type':'application/json',
        'Authorization':'Bearer ' + String(authTokens.access)
      }
    });
    let data = await response.json();
    console.log(data)
    setData(data);
  }

  useEffect(() => {
    getData();
  }, [endpoint]);


  function handleMenuClick(event){
    let selectedOption = event.target.value;
    console.log("Clicked item:", selectedOption);
  
    let url = 'http://127.0.0.1:8000/api/set_bank_access_token/'
    let payload = {
      selectedOption: selectedOption,
    }
    fetch(url, {
      method: 'POST',
      headers:{
        'Content-Type':'application/json',
        'Authorization':'Bearer ' + String(authTokens.access)
      },
      body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log(error))
  }

  const options = data.map((item, index) => (
    <option key={index} value={item}>{item}</option>
  ));

  return (
    <div className="dropdown-content">
      <select onChange={handleMenuClick}>
        {options}
      </select>
    </div>
  );
}

export default DropDown;
