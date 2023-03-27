import React from "react";

const AdditionalData = () => {
    let {authTokens, logoutUser} = useContext(AuthContext);
    const [AdditionalData, setAdditionalData] = useState(null);
    const navigate = useNavigate()
    /*
    const data = {
        name: 'John Doe',
        age: 30,
        email: 'johndoe@example.com',
      };
    */
    
    
    let get_data = async() =>  {
        let url = 'http://127.0.0.1:8000/api/crypto_all_data/'
        let response = await fetch(url, {
            method:'GET',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer ' + String(authTokens.access)
            }
        });
        let data = await response.json();
        if (response.status === 200) {
            setAdditionalData(data);
        }
        else if (response.status === 303) {
            if (data['error'] === 'Investments not linked.') {
                navigate('/crypto_wallets')
            }
        }
    }
  
    React.useEffect(() => {
        get_data();
        let data = new Object();
        for (let key in AdditionalData) {
            data[key] = AdditionalData[key][1];

        }

        }, [data]);
    


    return (
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(data).map(([key, value]) => (
            <tr key={key}>
              <td>{key}</td>
              <td>{value}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };
  
  export default AdditionalData;