import cards from '../images/home-cards.png';
import computer from '../images/home-comp.png';
import Navbar from '../components/Navbar';
import homebkbox from "../images/home-background.png";

export default function Home() {
    return (
        <div class = "home_page">
            
            <div class = "home_boxes">
                <div class= "home_text_holder">
                    <div class = "home__content__holder">
                        <div class = "home__box">
                            <img class="home__background__image" src={homebkbox} alt="#"></img>
                            <div class="home__content">
                                <p class="home-text">Welcome to the future of financial monitoring - track everything from bank cards, stocks, and crypto.</p>
                                <img class="home__first__image" src={cards} alt="#"></img>
                                
                                
                            </div>
                 
                        </div>
                    </div>
                    <div class = "home__content__holder">
                        <div class = "home__box">
                            <img class="home__background__image" src={homebkbox} alt="#"></img>
                                <div class="home__content">
                                    <p class="home-text">Our aggregate asset tracking and dynamic charts will provide you with the best understanding of your finances.</p>
                                    <img class="home__first__image" src={computer} alt="#"></img>
                                    
                                    
                                </div>
                            
                        </div>
                    </div>
                </div>

            </div>
        </div>

        
    );


}
