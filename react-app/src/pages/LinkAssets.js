import debitCard from "../images/asset-debit.png";
import bkbox from "../images/asset-background.png";
import cryptoimg from "../images/asset-crypto.png";
import bankimg from "../images/asset-bank.png";


export default function LinkAssets() {
    return <div>
        
        <div>
            <div class="assetLink_holder">
                <div class="background__box">
                <img class="background__image" src={bkbox} alt="#"></img>
                    <div class="asset__content">
                        <img class="debit__card__image" src={debitCard} alt="#"></img>
                        <p class="middle-text">Link your credit or debit card</p>
                        <button class="link-button">Link</button>
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
                        <button class="link-button">Link</button>
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
                        <button class="link-button">Link</button>
                    </div>
                </div>
            </div>

        </div>

     
    </div>

}