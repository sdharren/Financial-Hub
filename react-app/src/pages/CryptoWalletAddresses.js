import React, { useContext } from "react";
import { useState } from "react";

const SaveWalletAddresses = () => {
    const [options, setOptions] = useState([
      { id: 1, value: '' },
    ]);
  
    const handleAddOption = () => {
      const newOptionId = options.length + 1;
      setOptions([...options, { id: newOptionId, value: '' }]);
    };
  
    const handleRemoveOption = (id) => {
      const newOptions = options.filter((option) => option.id !== id);
      setOptions(newOptions);
    };
  
    const handleOptionChange = (id, value) => {
      const updatedOptions = options.map((option) => {
        if (option.id === id) {
          return { ...option, value };
        }
        return option;
      });
      setOptions(updatedOptions);
    };

    let form0 = (
        <div class="address-form">
        {options.map((option) => (
          <div class="address-form-content" key={option.id}>
            <label htmlFor={`option-${option.id}`}>{`Wallet Address ${option.id}:`}</label>
            <input type="text" id={`option-${option.id}`} name={`option-${option.id}`} value={option.value} onChange={(e) => handleOptionChange(option.id, e.target.value)} />
            
            <div class="inline-wallet-address-container">
                <label htmlFor="multiple-choice-1">Bitcoin: </label>
                <input type="radio" id="btc-choice-1" name="multiple-choice" />    
                <label htmlFor="multiple-choice-1">Ethereum: </label>
                <input type="radio" id="eth-choice-1" name="multiple-choice" />
            </div>

            <button type="button" onClick={() => handleRemoveOption(option.id)}>Remove</button>
            <button type="button" onClick={handleAddOption}>Add Option</button>
          </div>
        ))}
      </div>
    )
  
    return (form0);
  }

export default SaveWalletAddresses

