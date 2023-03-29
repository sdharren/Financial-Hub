import { usePlaidLink } from "react-plaid-link";
import { useContext } from "react";
import AuthContext from "../context/AuthContext";
import { useNavigate, useLocation } from "react-router-dom";


function Link() {  
    let {authTokens, logoutUser} = useContext(AuthContext);
    const location = useLocation();
    const navigate = useNavigate();

    async function onSuccess(public_token, metadata) {
        // exchange public token
        let response = await fetch('api/exchange_public_token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization':'Bearer ' + String(authTokens.access),
            },
            body: JSON.stringify({'public_token': public_token})
        });

        if (response.status === 200) {
            navigate('/dashboard');
        }
        else {
            alert('Something went wrong. Please try linking the asset again.');
            navigate('/link_assets');
        }
        // at this point the token is exchanged and the access token is saved
        // need to now redirect/ tell parent component to render next thing
    }

    const config = {
        token: location.state['link_token'],
        onSuccess
    };
    const {open} = usePlaidLink(config);

    
    return (
        <div style={{margin: 'auto'}} onLoad={open()}>
            <h2 className='text-white'>Taking you to Plaid. Hold on!</h2>
        </div>
    );
}

export default Link;