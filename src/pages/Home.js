import cards from '../images/home-cards.png';
import computer from '../images/home-comp.png';
import homebkbox from "../images/home-background.png";

export default function Home() {
    
    let page2 = (
        <div className='home-container flex flex-col my-10px mx-20 p-10 gap-8'>
            <div className='welcome-box flex flex-row rounded-3xl shadow-lg bg-gradient-to-r from-violet-500 to-violet-600 py-5 px-10'>
                <p className='welcome-box-text my-auto text-4xl text-white'>Welcome to the future of financial monitoring - track everything from bank cards, stocks, and crypto.</p>
                <img className="welcome-box-image" src={cards} alt="welcome-box-image" />
            </div>
            <div className='aggregate-box flex flex-row rounded-3xl shadow-lg bg-gradient-to-r from-violet-500 to-violet-600 py-5 px-10'>
                <p className="aggregate-box-text my-auto text-4xl text-white">Our aggregate asset tracking and dynamic charts will provide you with the best understanding of your finances.</p>
                <img className="aggregate-box-image" src={computer} alt="aggregate-box-image"></img>
            </div>

        </div>
    )
    return page2

}
