import group from '../images/about-background.png';
import ecommerce from '../images/about-bank.png';
import etherium from '../images/about-crypto.png';
import buy from '../images/about-stock.png';

export default function About() {
    return (
        <div>
            
        
            <div className="about-page">
            <h1 className='txt-about-us'>About Us</h1>
            <p className='txt-monitoring-finances'>Your go-to app for monitoring finances</p>
            <p className='txt-link-assets'>Just link any of your assets and let us do the magic ✨</p>

            <div className="about-container">
                <div className="about-box">
                    <h2>Stocks</h2>
                    <div className="about-background-box">
                        <img src={group} alt="#" />
                        <div className="about-image-box">
                            <img src={buy} alt="Stocks" />
                        </div>
                    </div>
                </div>
                <div className="about-box">
                    <h2>Banks</h2>
                    <div className="about-background-box">
                        <img src={group} alt="#" />
                        <div className="about-image-box">
                            <img src={ecommerce} alt="#" />
                        </div>
                    </div>
                </div>
                <div className="about-box">
                    <h2>Crypto</h2>
                    <div className="about-background-box">
                        <img src={group} alt="#" />
                        <div className="about-image-box">
                            <img src={etherium} alt="#" />
                        </div>
                    </div>
                </div>
            </div>
            </div>
        </div>
  );
}