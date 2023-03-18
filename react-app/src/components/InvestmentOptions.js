import React, { useEffect, useState, useContext } from "react";
import AuthContext from '../context/AuthContext';

function InvestmentOptions ({ options, handleSelectionUpdate, selectedOption, optionType }) {
    let {authTokens, logoutUser} = useContext(AuthContext);
    const [selected, setSelected] = useState(selectedOption);
    const [selectOptions, setSelectOptions] = useState(
        null
    );

    let get_options = async() => {
        
        if (optionType === 'investment_category_breakdown') {
            let response = await fetch('http://127.0.0.1:8000/api/investment_category_names/',
                {
                    method:'GET',
                    headers:{
                        'Content-Type':'application/json',
                        'Authorization':'Bearer ' + String(authTokens.access)
                    }
                }
            );
            let data = await response.json();
            console.log(data)
            setSelectOptions(
                data['categories'].map(o => (
                    <option key={o} value={o}>{o}</option>
                ))
            )
        }
        else if (optionType === 'stock_history') {
            let response = await fetch('http://127.0.0.1:8000/api/supported_investments/',
                {
                    method:'GET',
                    headers:{
                        'Content-Type':'application/json',
                        'Authorization':'Bearer ' + String(authTokens.access)
                    }
                }
            );
            let data = await response.json();
            setSelectOptions(
                data['investments'].map(o => (
                    <option key={o} value={o}>{o}</option>
                ))
            )
        }
    }

    useEffect(() => {
        get_options();
    }, [optionType]);

    function handleClick(select) {
        setSelected(select);
        // setSelectOptions(
        //     options.map(o => (
        //         o === select ? 
        //         <option key={o} value={o} selected={true}>{o}</option> :
        //         <option key={o} value={o}>{o}</option>
        //     ))
        // );
        handleSelectionUpdate({
            'optionType': optionType,
            'nextSelect': select
        });
    }

    return (
        <select autoFocus={true} onChange={(event) => handleClick(event.target.value)}>
            {selectOptions}
        </select>
    )
}

export default InvestmentOptions;