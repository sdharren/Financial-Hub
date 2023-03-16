import cards from '../images/home-cards.png';
import computer from '../images/home-comp.png';
import Navbar from '../components/Navbar';
import homebkbox from "../images/home-background.png";

export default function Home() {
    return (
        <div className = "home_page">
            
            <div className = "home_boxes">
                <div className= "home_text_holder">
                    <div className = "home__content__holder">
                        <div className = "home__box">
                            <img className="home__background__image" src={homebkbox} alt="#"></img>
                            <div className="home__content">
                                <p className="home-text">Welcome to the future of financial monitoring - track everything from bank cards, stocks, and crypto.</p>
                                <img className="home__first__image" src={cards} alt="#"></img>
                                
                                
                            </div>
                 
                        </div>
                    </div>
                    <div className = "home__content__holder">
                        <div className = "home__box">
                            <img className="home__background__image" src={homebkbox} alt="#"></img>
                                <div className="home__content">
                                    <p className="home-text">Our aggregate asset tracking and dynamic charts will provide you with the best understanding of your finances.</p>
                                    <img className="home__first__image" src={computer} alt="#"></img>
                                    
                                    
                                </div>
                            
                        </div>
                    </div>
                </div>

            </div>
        </div>

        
    );


}
