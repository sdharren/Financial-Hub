import React, { useState, useEffect, useRef, useContext } from 'react';
import AuthContext from '../context/AuthContext';

function DropDown({endpoint, endpoint_parameter, loadNext}) {
  let {authTokens, logoutUser} = useContext(AuthContext);
  const [data, setData] = useState([]);

  async function getData() {
    let url = 'api/select_bank_account'
    let response = await fetch(url, {
      method:'GET',
      headers:{
        'Content-Type':'application/json',
        'Authorization':'Bearer ' + String(authTokens.access)
      }
    });
    let data = await response.json();
    setData(data);
  }

  useEffect(() => {
    getData();
  }, [endpoint]);


  async function handleMenuClick(event){
    let selectedOption = event.target.value;
  
    let url = 'api/set_bank_access_token/'
    let payload = {
      selectedOption: selectedOption,
    }
    await fetch(url, {
      method: 'POST',
      headers:{
        'Content-Type':'application/json',
        'Authorization':'Bearer ' + String(authTokens.access)
      },
      body: JSON.stringify(payload)
    }
    )
    .then(response => response.json())
    .catch(error => console.log(error));

    let parameter = {
        'endpoint': endpoint,
        'param': endpoint_parameter,
        'name': selectedOption
    };
    console.log(parameter)
    loadNext(parameter)
  }

  const options = data.map((item, index) => (
    <option className='bg-transparent' key={item.id} value={item.id}>{item.name}</option>
  ));

  return (
    <div className="dropdown-content">
      <select className='bg-transparent text-black' onChange={handleMenuClick}>
        {options}
      </select>
    </div>
  );
}

export default DropDown;
