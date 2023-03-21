import React, { useState, useContext } from 'react';
import AuthContext from '../context/AuthContext';
import DebitAccounts from './DebitAccounts';

function Accounts() {
  const [selectedInstitution, setSelectedInstitution] = useState(null);
  let {authTokens, logoutUser} = useContext(AuthContext);

  async function handleDeleteBank(institution)  {
    let url = `http://127.0.0.1:8000/api/delete_linked_bank/${institution}/`
    try {
        let response = await fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization':'Bearer ' + String(authTokens.access)
        },
        })
        if (response.ok) {
            setSelectedInstitution(null); // Clear the selected institution
        } else {
            throw new Error('Failed to delete linked bank account');
        }
    } catch (error) {
      console.error(error);
    }
  }

  const linkedBanks = <DebitAccounts setSelectedInstitution={setSelectedInstitution} />; // Render the list of linked banks

  return (
    <div>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Unlink</th>
          </tr>
        </thead>
        <tbody>
          {linkedBanks.map((institution, index) => (
            <tr key={index}>
              <td>{institution}</td>
              <td>Bank</td>
              <td>
                <button onClick={() => handleDeleteBank(institution)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Accounts;
