import PieChart from "./PieChart";
import LineGraph from "./LineGraph";
import { useState, useContext } from "react";
import AuthContext from '../context/AuthContext';

function GraphDisplay() {
    const [graph, setGraph] = useState(<PieChart endpoint={"investment_categories"} loadNext={handleLoadNext}/>);
    let {authTokens, logoutUser} = useContext(AuthContext);

    const [overviewActive, setOverviewActive] = useState(true);
    const [categoryActive, setCategoryActive] = useState(false);
    const [stocksActive, setStocksActive] = useState(false);

    let link_sandbox = async() => {
        let response = await fetch('http://127.0.0.1:8000/api/sandbox_investments/',
            {
                method:'GET',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':'Bearer ' + String(authTokens.access)
                }
            }
        )
        if (response.status === 200) {
            alert("Linked sandbox investments successfuly.");
        }
    }

    

    // JSON to know which API endpoint to query next
    const nextRoute = {
        'investment_categories': 'investment_category_breakdown',
        'investment_category_breakdown': 'stock_history'
    }

    // passed as a parameter to the pie chart to update this page once a section of the pie chart is clicked
    function handleLoadNext(event) {
        let next = nextRoute[event.current];

        if (next == 'stock_history') {
            setCategoryActive(false);
            setStocksActive(true);
            
            setGraph(
                <LineGraph endpoint={next} endpoint_parameter={event.next} />
            );
        }
        else {
            let nextEndpoint = nextRoute[event.current];
            if (nextEndpoint === 'investment_category_breakdown') {
                setOverviewActive(false);
                setCategoryActive(true);
            }
            setGraph(
                <PieChart endpoint={nextEndpoint} endpoint_parameter={event.next} loadNext={handleLoadNext} />
            );
        }
    }


    return (
        <div>
            <div class="tab">
                <button className={"tablinks" + (overviewActive ? " active" : "") } onclick="openCity(event, 'London')">Overview</button>
                <button className={"tablinks" + (categoryActive ? " active" : "") } onclick="openCity(event, 'Paris')">Category</button>
                <button className={"tablinks" + (stocksActive ? " active" : "") } onclick="openCity(event, 'Tokyo')">Stocks?</button>
            </div>

            <div className="tabcontent" onLoad={link_sandbox()}>
                {graph}
            </div>
        </div>
    );
}

export default GraphDisplay;
