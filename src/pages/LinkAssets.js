import debitCard from "../images/asset-debit.png";
import bkbox from "../images/asset-background.png";
import cryptoimg from "../images/asset-crypto.png";
import bankimg from "../images/asset-bank.png";

import AuthContext from '../context/AuthContext';
import { useContext } from "react";
import { useNavigate } from 'react-router-dom';

export default function LinkAssets() {
    let {authTokens, logoutUser} = useContext(AuthContext);
    const navigate = useNavigate()

    async function get_link_token(product) {
        let url = 'http://127.0.0.1:8000/api/link_token?product=' + product
        let response = await fetch(url, {
            method:'GET',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer ' + String(authTokens.access)
            }
        });
        let data = await response.json();
        if (response.status === 200) {
            navigate('/plaid_link', {
                state: {link_token: data['link_token']},
                replace: true
            });
        }

        
    }

    const buttClick = () => {
        let route = '/crypto_addresses';
        navigate(route);

    }

    return <div>
        
        <div>
            <div class="assetLink_holder">
                <div class="background__box">
                <img class="background__image" src={bkbox} alt="#"></img>
                    <div class="asset__content">
                        <img class="debit__card__image" src={debitCard} alt="#"></img>
                        <p class="middle-text">Link your credit or debit card</p>
                        <button class="link-button" onClick={async () => {await get_link_token("transactions");} }>Link</button>
                    </div>
                </div>
            </div>

        </div>
        <div>
            <div class="assetLink_holder">
                <div class="background__box">
                <img class="background__image" src={bkbox} alt="#"></img>
                    <div class="asset__content">
                        <img class="bank__image" src={bankimg} alt="#"></img>
                        <p class="middle-text">Link your brokerage account</p>
                        <button class="link-button" onClick={async () => {await get_link_token("investments");} }>Link</button>
                    </div>
                </div>
            </div>

        </div>
        <div>
            <div class="assetLink_holder">
                <div class="background__box">
                <img class="background__image" src={bkbox} alt="#"></img>
                    <div class="asset__content">
                        <img class="crypto__image" src={cryptoimg} alt="#"></img>
                        <p class="middle-text">Link your crypto wallet</p>
                        <button class="link-button" onClick={buttClick}>Link</button>
                    </div>
                </div>
            </div>

        </div>

     
    </div>

}