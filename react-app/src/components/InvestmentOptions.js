import React, { useState } from "react";

function InvestmentOptions ({ options, handleClick, selectedOption }) {
    const [selected, setSelected] = useState(selectedOption);
    const [selectOptions, setSelectOptions] = useState(
        options.map(o => (
            <option key={o} value={o}>{o}</option>
        ))
    );

    return (
        <select value={selected} onChange={(event) => setSelected(event.target.value)}>
            {selectOptions}
        </select>
    )
}

export default InvestmentOptions;