import React, { useEffect, useState } from "react";

function InvestmentOptions ({ options, handleSelectionUpdate, selectedOption, optionType }) {
    const [selected, setSelected] = useState(selectedOption);
    const [selectOptions, setSelectOptions] = useState(
        options.map(o => (
            <option key={o} value={o}>{o}</option>
        ))
    );

    // useEffect((selected) => {
    //     setSelectOptions(
    //         options.map(o => (
    //             o === selected ? 
    //             <option key={o} value={o} selected={true}>{o}</option> :
    //             <option key={o} value={o}>{o}</option>
    //         ))
    //     );
    // }, [selected])

    function handleClick(select) {
        setSelected(select);
        setSelectOptions(
            options.map(o => (
                o === select ? 
                <option key={o} value={o} selected={true}>{o}</option> :
                <option key={o} value={o}>{o}</option>
            ))
        );
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