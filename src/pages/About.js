import group from '../images/about-background.png';
import ecommerce from '../images/about-bank.png';
import etherium from '../images/about-crypto.png';
import buy from '../images/about-stock.png';

export default function About() {

    let page1 = (
        <div className='text-white'> 
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
                            <img src={ecommerce} alt="Banks" />
                        </div>
                    </div>
                </div>
                <div className="about-box">
                    <h2>Crypto</h2>
                    <div className="about-background-box">
                        <img src={group} alt="#" />
                        <div className="about-image-box">
                            <img src={etherium} alt="Crypto" />
                        </div>
                    </div>
                </div>
            </div>
            </div>
        </div>
  );
    
    let page2 = (
        <div className='about-container flex flex-col my-10 mx-20 gap-24'>
            <div className='about-text-box flex flex-col gap-8'>
                <div className='about-us text-white/75 text-center text-4xl'>About Us</div>
                <div className='about-caption text-white text-center text-5xl font-bold'>Your go-to app for monitoring your finances</div>
                <div className='link-message text-white text-center text-2xl font-light'>Just link any of your assets to the dashboard and let us do our magic ✨</div>
            </div>
            {/* <div className='about-us-cards flex flex-row justify-center gap-3 items-stretch'>
                <div className='crypto-card flex flex-col gap-2'>
                    <div className='crypto-label text-white text-center text-3xl font-medium'>Crypto</div>
                    <img className='rounded-3xl shadow-lg bg-gradient-to-r from-violet-500 to-violet-600' src={etherium} alt="Crypto" /> 
                </div>
                <div className='bank-card flex flex-col'>
                    <div className='bank-label text-white text-center text-3xl font-medium'>Bank</div>
                    <img className='rounded-3xl shadow-lg bg-gradient-to-r from-violet-500 to-violet-600' src={ecommerce} alt="Banks" /> 
                </div>
                <div className='stocks-card flex flex-col'>
                    <div className='stocks-label text-white text-center text-3xl font-medium'>Stocks</div>
                    <img className='rounded-3xl shadow-lg bg-gradient-to-r from-violet-500 to-violet-600' src={buy} alt="Stocks" /> 
                </div>
            </div> */}
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
                            <img src={ecommerce} alt="Banks" />
                        </div>
                    </div>
                </div>
                <div className="about-box">
                    <h2>Crypto</h2>
                    <div className="about-background-box">
                        <img src={group} alt="#" />
                        <div className="about-image-box">
                            <img src={etherium} alt="Crypto" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );

    return page1
}