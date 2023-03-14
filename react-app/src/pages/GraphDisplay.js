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

    const [lastCategory, setLastCategory] = useState(null);
    const [lastStock, setLastStock] = useState(null);

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
            setLastStock(event.next);

            setGraph(
                <LineGraph endpoint={next} endpoint_parameter={event.next} />
            );
        }
        else {
            let nextEndpoint = nextRoute[event.current];
            if (nextEndpoint === 'investment_category_breakdown') {
                setOverviewActive(false);
                setCategoryActive(true);
                setLastCategory(event.next);
            }
            setGraph(
                <PieChart endpoint={nextEndpoint} endpoint_parameter={event.next} loadNext={handleLoadNext} />
            );
        }
    }

    async function callApi(endpoint) {
        let response = await fetch('http://127.0.0.1:8000/api/' + endpoint + '/',
            {
                method:'GET',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':'Bearer ' + String(authTokens.access)
                }
            }
        );
        let data = await response.json();
        return data;
    }

    async function handleTabClick(endpoint) {
        if (endpoint === 'stock_history') {
            if (lastStock !== null) {
                setGraph(
                    <LineGraph endpoint={endpoint} endpoint_parameter={lastStock} />
                );
            }
            else {
                let data = await callApi('first_stock')
                let stock = data['stock'];

                setLastStock(stock);

                setCategoryActive(false);
                setStocksActive(true);
                setOverviewActive(false);

                setGraph(
                    <LineGraph endpoint={endpoint} endpoint_parameter={stock} />
                );
            }
        }
        else if (endpoint === 'investment_category_breakdown') {
            if (lastCategory !== null) {
                setGraph(
                    <PieChart endpoint={endpoint} endpoint_parameter={lastCategory} loadNext={handleLoadNext} />
                );
            }
            else {
                let data = await callApi('first_investment_category')
                let category = data['category'];

                setLastCategory(category);

                setCategoryActive(true);
                setStocksActive(false);
                setOverviewActive(false);

                setGraph(
                    <PieChart endpoint={endpoint} endpoint_parameter={category} loadNext={handleLoadNext} />
                );
            }    
        }
        else if (endpoint === 'investment_categories') {
            setCategoryActive(false);
            setStocksActive(false);
            setOverviewActive(true);
            
            setGraph(
                <PieChart endpoint={endpoint} loadNext={handleLoadNext} />
            );
        }
    }


    return (
        <div>
            <div class="tab">
                <button className={"tablinks" + (overviewActive ? " active" : "") } onClick={() => handleTabClick('investment_categories')}>
                    Overview
                </button>
                <button className={"tablinks" + (categoryActive ? " active" : "") } onClick={() => handleTabClick('investment_category_breakdown')}>
                    Category
                    </button>
                <button className={"tablinks" + (stocksActive ? " active" : "") } onClick={() => handleTabClick('stock_history')}>
                    Stocks?
                </button>
            </div>

            <div className="tabcontent" onLoad={link_sandbox()}>
                {graph}
            </div>
        </div>
    );
}

export default GraphDisplay;
