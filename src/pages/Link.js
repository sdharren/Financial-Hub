import { usePlaidLink } from "react-plaid-link";
import { useContext } from "react";
import AuthContext from "../context/AuthContext";
import { useNavigate, useLocation } from "react-router-dom";


function Link() {  
    let {authTokens, logoutUser} = useContext(AuthContext);
    const location = useLocation();
    const navigate = useNavigate();

    async function onSuccess(public_token, metadata) {
        let response = await fetch('api/exchange_public_token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization':'Bearer ' + String(authTokens.access),
            },
            body: JSON.stringify({'public_token': public_token})
        });

        if (response.ok) {
            navigate('/dashboard');
        }
        else if (response.status === 400){
            alert('Something went wrong. Please try linking the asset again.');
            navigate('/link_assets');
        }
        navigate('/dashboard');
    }

    const config = {
        token: location.state['link_token'],
        onSuccess
    };
    const {open} = usePlaidLink(config);

    
    return (
        <div data-testid='linkplaid' style={{margin: 'auto'}} onLoad={open()}>
            <h2 className='text-white'>Taking you to Plaid. Hold on!</h2>
        </div>
    );
}

export default Link;