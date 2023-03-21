import React, { useState, useEffect, useRef, useContext } from 'react';
import AuthContext from '../context/AuthContext';

function DropDown({endpoint, endpoint_parameter, loadNext}) {
  let {authTokens, logoutUser} = useContext(AuthContext);

  function handleMenuClick(event){
    console.log("Clicked item:", event.target.value);
  }

  const data = ["access_token_1","access_token_2","access_token_3","access_token_4","access_token_5"]

  const options = data.map((item, index) =>
    <option key={index} value={item}>{item}</option>
  );

  return (
    <div className="dropdown-content">
        <select onChange={handleMenuClick}>
            {options}
        </select>
    </div>
  );
}

export default DropDown;
