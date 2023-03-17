import React, { useEffect, useState, useContext } from "react";
import AuthContext from '../context/AuthContext';

function GraphSelect ({ options, handleSelectionUpdate, selectedOption }) {
    const [select, setSelect] = useState(
        options.map(o => (
                    o === selectedOption ? 
                    <option key={o} value={o} selected={true}>{o}</option> :
                    <option key={o} value={o}>{o}</option>
                ))
    );
    
    return (
        <select autoFocus={true} onChange={(event) => handleSelectionUpdate(event.target.value)}>
            {select}
        </select>
    )
}

export default GraphSelect;