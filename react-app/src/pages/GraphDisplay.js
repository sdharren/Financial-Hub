import PieChart from "./PieChart";
import LineGraph from "./LineGraph";
import { useState, useContext, useEffect } from "react";
import AuthContext from '../context/AuthContext';
import InvestmentOptions from "../components/InvestmentOptions";

function GraphDisplay() {
    const [graph, setGraph] = useState(<div><PieChart endpoint={"investment_categories"} loadNext={handleLoadNext}/></div>);
    let {authTokens, logoutUser} = useContext(AuthContext);

    const [categoryOptions, setCategoryOptions] = useState([]);
    const [investmentOptions, setInvestmentOptions] = useState([]);

    const [overviewActive, setOverviewActive] = useState(true);
    const [categoryActive, setCategoryActive] = useState(false);
    const [stocksActive, setStocksActive] = useState(false);

    const [lastCategory, setLastCategory] = useState(null);
    const [lastStock, setLastStock] = useState(null);

    useEffect(() => {

    }, [investmentOptions])

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
    
    async function updateOptions() {
        let options = {
            'investments': [],
            'categories': []
        }
        if (investmentOptions.length === 0) {
            let data = await callApi('supported_investments');
            options['investments'] = data['investments'];
            setInvestmentOptions(data['investments'])
        }
        if (categoryOptions.length === 0) {
            let data = await callApi('investment_category_names');
            options['categories'] = data['categories'];
            setCategoryOptions(data['categories'])
        }
        return options;
    }

    function changeGraphState(graph) {
        if (graph === 'investment_categories') {
            setCategoryActive(false);
            setStocksActive(false);
            setOverviewActive(true);
        }
        else if (graph === 'investment_category_breakdown') {
            setCategoryActive(true);
            setStocksActive(false);
            setOverviewActive(false);
        }
        else if (graph === 'stock_history') {
            setCategoryActive(false);
            setStocksActive(true);
            setOverviewActive(false);
        }
    }
    
    async function changeGraph(endpoint, endpoint_parameter) {
        const options = await updateOptions();
        switch(endpoint) {
            case 'investment_categories':
                setGraph(
                    <div>
                        <PieChart endpoint={endpoint} endpoint_parameter={endpoint_parameter} loadNext={handleLoadNext} />
                    </div>
                );
                break;

            case 'investment_category_breakdown':
                setLastCategory(endpoint_parameter);
                setGraph(
                    <div>
                        <InvestmentOptions 
                            options={categoryOptions.length === 0 ? options['categories'] : categoryOptions} 
                            selectedOption={endpoint_parameter}
                        />
                        <PieChart endpoint={endpoint} endpoint_parameter={endpoint_parameter} loadNext={handleLoadNext} />
                    </div>
                );
                break;

            case 'stock_history':
                setLastStock(endpoint_parameter);
                setGraph(
                    <div>
                        <InvestmentOptions options={investmentOptions.length === 0 ? options['investments'] : investmentOptions} />
                        <LineGraph endpoint={endpoint} endpoint_parameter={endpoint_parameter} />
                    </div>
                    
                );
                break;
        }
        changeGraphState(endpoint);
    }

    // JSON to know which API endpoint to query next
    const nextRoute = {
        'investment_categories': 'investment_category_breakdown',
        'investment_category_breakdown': 'stock_history'
    }

    // passed as a parameter to the pie chart to update this page once a section of the pie chart is clicked
    function handleLoadNext(event) {
        let next = nextRoute[event.current];
        changeGraph(next, event.next);
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
                changeGraph(endpoint, lastStock);
            }
            else {
                let data = await callApi('supported_investments')
                let stock = data['investments'][0];

                changeGraph(endpoint, stock);
            }
        }
        else if (endpoint === 'investment_category_breakdown') {
            if (lastCategory !== null) {
                changeGraph(endpoint, lastCategory);
            }
            else {
                let data = await callApi('investment_category_names')
                let category = data['categories'][0];

                changeGraph(endpoint, category);
            }    
        }
        else if (endpoint === 'investment_categories') {
            changeGraph(endpoint);
        }
    }


    return (
        <div className="investment-graphs">
            <div className="tab">
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

            <div className="tabcontent">
                {graph}
            </div>
        </div>
    );
}

export default GraphDisplay;
