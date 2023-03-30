    import { useNavigate } from "react-router-dom";
    import React, { useContext } from 'react';
    import AuthContext from "../context/AuthContext";

    const useHandleError = (error) => {
        let {authTokens, logoutUser} = useContext(AuthContext);
        const navigate = useNavigate();

        if (error !== null) {
            if (error === 'Internal Server Error') {
                alert('Something went wrong. Please try again later.');
            }
            else {
                console.log(error)
                let errorMessage = error['error']
                if (errorMessage === 'Investments not linked.') {
                    redirectToLink('investments');
                }
                else if (errorMessage === 'Transactions Not Linked.') {
                    redirectToLink('transactions');
                }
                else if (errorMessage === 'Crypto not linked.') {
                    navigate('/crypto_wallets');
                }
            }
        }

        async function redirectToLink (assetType) {
            let response = await fetch('api/link_token/?product=' + assetType,
                    {
                        method:'GET',
                        headers:{
                            'Content-Type':'application/json',
                            'Authorization':'Bearer ' + String(authTokens.access)
                        }
                    }
                )
                let data = await response.json();
                if (response.status === 200) {
                    navigate('/plaid_link', {
                        state: {link_token: data['link_token']},
                        replace: true
                    });
                }
        }
    }

    export default useHandleError;
