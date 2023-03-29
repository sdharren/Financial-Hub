// import { all } from 'axios';
import { useState, useContext} from 'react';
import AuthContext from '../context/AuthContext';

function CryptoWalletAddresses() {
  const [addresses, setAddresses] = useState([{address: '', type: ''}]);
  let {authTokens, logoutUser} = useContext(AuthContext);

  function handleAddressChange(index, key, value) {
    const newAddresses = [...addresses];
    newAddresses[index][key] = value;
    setAddresses(newAddresses);
  }

  function handleAddAddress() {
    setAddresses([...addresses, {address: '', type: ''}]);
  }

  function handleRemoveAddress(index) {
    const newAddresses = [...addresses];
    newAddresses.splice(index, 1);
    setAddresses(newAddresses);
  }

  function handleSubmit(event) {
    event.preventDefault();
    const allAddresses = [...addresses];

    for(let i = 0; i < allAddresses.length; i++) {
        if(/(\b0x[a-f0-9]{40}\b)$/.test(allAddresses[i].address) || /^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$/.test(allAddresses[i].address)) {  // Test regex matches eth or btc format
            let saveUrl = 'api/link_crypto_wallet/?param=' + allAddresses[i].address;
            fetch(saveUrl, {
                method:'GET',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':'Bearer ' + String(authTokens.access)
                }
            });
        }
    };
    
  }

  return (
    <form className="crypto-wallet-addresses" onSubmit={handleSubmit}>
      {addresses.map((address, index) => (
        <div key={index}>
          <label>
            Address {index + 1}:
            <input
              type="text"
              pattern=  "(\b0x[a-f0-9]{40}\b)|(^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$)"
              value={address.address}
              onChange={(event) => handleAddressChange(index, 'address', event.target.value)}
            />
          </label>
          <button type="button" className="remove-button" onClick={() => handleRemoveAddress(index)}>
            Remove
          </button>
        </div>
      ))}
      <button type="button" className="add-button" onClick={handleAddAddress}>
        Add Address
      </button>
      <button type="submit" className="submit-button">Submit</button>
    </form>
  );
}

export default CryptoWalletAddresses