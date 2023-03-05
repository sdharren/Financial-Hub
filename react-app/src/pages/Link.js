import { usePlaidLink } from "react-plaid-link";
import { useContext } from "react";
import AuthContext from "../context/AuthContext";


function Link({ linkToken }) {  
    let {authTokens, logoutUser} = useContext(AuthContext);

    async function onSuccess(public_token, metadata) {
            // exchange public token
            fetch('http://127.0.0.1:8000/api/exchange_public_token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization':'Bearer ' + String(authTokens.access),
            },
            body: {
                public_token,
            },
            });
    }

    const config = {
        token: linkToken,
        onSuccess
    };
    const {open} = usePlaidLink(config);

    
    return (
        <div style={{margin: 'auto'}} onLoad={open()}>
            <h2>Taking you to Plaid. Hold on!</h2>
        </div>
    );
}

export default Link;