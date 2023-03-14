import cards from '../static/images/Ecommerce_13.png';
import computer from '../Other 07.png'

export default function Home() {
    return (
        <section class = "home_boxes">
            <div class= "home_text_holder">
                <div class = "home__box">
                    <div class = "image-container">
                        <img class= "box__image"
                            src = {cards} alt = "#"
                            ></img>
                    </div>
                    <div class = "home__wrapper">
                        <p class="home__text">Welcome to the future of financial monitoring - track everything from bank cards, stocks, and crypto.</p>
                    </div>
                </div>

                <div class = "home__box">
                    <div class = "image-container">
                        <img class= "box__image"
                            src = {computer}
                            alt = "#"></img>

                    </div>
                    <div class = "home__wrapper">
                        <p class="home__text">Our aggregate asset tracking and dynamic charts will provide you with the best understanding of your finances.</p>
                    </div>
                </div>

            </div>

        </section>

    );


}
