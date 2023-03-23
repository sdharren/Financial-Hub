import { useState } from 'react';

function CryptoWalletAddresses() {
  const [addresses, setAddresses] = useState([{address: '', type: 'btc'}]);

  function handleAddressChange(index, key, value) {
    const newAddresses = [...addresses];
    newAddresses[index][key] = value;
    setAddresses(newAddresses);
  }

  function handleAddAddress() {
    setAddresses([...addresses, {address: '', type: 'btc'}]);
  }

  function handleRemoveAddress(index) {
    const newAddresses = [...addresses];
    newAddresses.splice(index, 1);
    setAddresses(newAddresses);
  }

  function handleSubmit(event) {
    event.preventDefault();
    
    
  }

  return (
    <form className="crypto-wallet-addresses" onSubmit={handleSubmit}>
      {addresses.map((address, index) => (
        <div key={index}>
          <label>
            Address {index + 1}:
            <input
              type="text"
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