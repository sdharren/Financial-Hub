/**
 * Creates the Home component that renders if the user is not logged in,
 * showing basic overview of the site
 */
import cards from '../images/home-cards.png';
import computer from '../images/home-comp.png';
import { backgroundBox } from '../static/styling';

export default function Home() {
    
    const pStyling = 'my-auto text-4xl text-white'
    let page2 = (
        <div className='home-container flex flex-col my-10px mx-20 p-10 gap-8'>
            <div className={'welcome-box flex flex-row py-5 px-10 ' + backgroundBox}>
                <p className={'welcome-box-text ' + pStyling}>Welcome to the future of financial monitoring - track everything from bank cards, stocks, and crypto.</p>
                <img className="welcome-box-image" src={cards} alt="welcome-box-image" />
            </div>
            <div className={'aggregate-box flex flex-row py-5 px-10 ' + backgroundBox}>
                <p className={"aggregate-box-text " + pStyling}>Our aggregate asset tracking and dynamic charts will provide you with the best understanding of your finances.</p>
                <img className="aggregate-box-image" src={computer} alt="aggregate-box-image"></img>
            </div>

        </div>
    )
    return page2

}
