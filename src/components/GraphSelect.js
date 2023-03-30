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
        <select className="graph-selec bg-transparent text-black" onChange={(event) => handleSelectionUpdate(event.target.value) }>
            {options.map(o => (
                    o === selectedOption ? 
                    <option className="select-option" key={o} value={o} selected={true} disabled={true}>{o}</option> :
                    <option className="select-option" key={o} value={o}>{o}</option>
                ))}
        </select>
    )
}

export default GraphSelect;