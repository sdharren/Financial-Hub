import PieChart from "./PieChart";
import LineGraph from "./LineGraph";
import { useState, useContext, useEffect } from "react";
import AuthContext from '../context/AuthContext';
import ReturnDisplay from "../components/ReturnDisplay";

function InvestmentGraphs() {
    // first graph to display - investments overview
    const [graph, setGraph] = useState(<PieChart endpoint={"investment_categories"} loadNext={handleLoadNext} />);
    let {authTokens, logoutUser} = useContext(AuthContext);

    // options for each graph tab so user can select asset to show in graph
    const [categoryOptions, setCategoryOptions] = useState([]);
    const [investmentOptions, setInvestmentOptions] = useState([]);

    // keep track of which graph is currently being displayed
    const [overviewActive, setOverviewActive] = useState(true);
    const [categoryActive, setCategoryActive] = useState(false);
    const [stocksActive, setStocksActive] = useState(false);

    // keep track of last displayed graphs so we know what to display if user switches tabs manually
    const [lastCategory, setLastCategory] = useState(null);
    const [lastStock, setLastStock] = useState(null);

    // FOR DEVELOPMENT PURPOSES (use this if investments aren't linked - put onLoad={link_sandbox()} in the top div at the very bottom)
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
    
    // update the GraphSelect options (called every time a graph is rendered/re-rendered)
    async function updateOptions() {
        let options = {
            'investments': [],
            'categories': []
        }
        // on the first render investmentOptions and categoryOptions are not set
        // if we are in first render - fetch them from the API and return a JSON at the same time as the useState variables would only be usable on next render
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

    // change the active tab (called each time a graph is rendered/re-rendered)
    function changeTabActive(graph) {
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
    
    // render a graph based on the endpoint supplied
    // endpoint_parameter is optional and is a parameter for the API request
    async function changeGraph(endpoint, endpoint_parameter) {
        const options = await updateOptions(); 
        changeTabActive(endpoint);

        switch(endpoint) {
            case 'investment_categories':
                let overall_returns = await getReturns('overall_returns');
                setGraph(
                    <div className="inline-block min-h-[60vh] max-h-[60vh] w-full">
                        <ReturnDisplay returns={overall_returns}/>
                        <PieChart 
                            endpoint={endpoint} 
                            endpoint_parameter={endpoint_parameter} 
                            loadNext={handleLoadNext} 
                            updateGraph={handleGraphUpdate}
                        />
                    </div>
                );
                break;

            case 'investment_category_breakdown':
                let category_returns = await getReturns('category_returns', endpoint_parameter);
                setLastCategory(endpoint_parameter);
                setGraph(
                    <div className="inline-block min-h-[60vh] max-h-[60vh] w-full">
                        <ReturnDisplay returns={category_returns}/>
                        <PieChart 
                            endpoint={endpoint} 
                            endpoint_parameter={endpoint_parameter} 
                            loadNext={handleLoadNext} 
                            updateGraph={handleGraphUpdate} 
                            selectOptions={ categoryOptions.length === 0 ? options['categories'] : categoryOptions}
                        />
                    </div>
                );
                break;

            case 'stock_history':
                let returns = await getReturns('returns', endpoint_parameter);
                setLastStock(endpoint_parameter);
                setGraph(
                        <div className="inline-block min-h-[60vh] max-h-[60vh] w-full">
                            <ReturnDisplay returns={returns}/>
                            <LineGraph 
                                endpoint={endpoint} 
                                updateGraph={handleGraphUpdate} 
                                endpoint_parameter={endpoint_parameter} 
                                selectOptions={investmentOptions.length === 0 ? options['investments'] : investmentOptions } 
                            />
                        </div>
                );
                break;
        }
    }

    // JSON to know which API endpoint to query next
    const nextRoute = {
        'investment_categories': 'investment_category_breakdown',
        'investment_category_breakdown': 'stock_history'
    }

    // passed as a parameter to the graph to update this page once a section of the graph is clicked
    function handleLoadNext(event) {
        let next = nextRoute[event.current];
        changeGraph(next, event.next);
    }

    // passed as a parameter to the graph to update the graph the user selects another one in GraphSelect
    function handleGraphUpdate(event) {
        let endpoint = event['endpoint'];
        let param = event['param'];
        changeGraph(endpoint, param)
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

    async function getReturns(endpoint, param) {
        let response = await fetch('http://127.0.0.1:8000/api/' + endpoint + (endpoint==='overall_returns'?'/':'/?param='+param),
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
                // if there is no last stock get our options and choose the first one
                const options = await updateOptions(); 
                changeGraph(
                    endpoint, 
                    investmentOptions.length === 0 ? options['investments'][0] : investmentOptions[0]
                );
            }
        }
        else if (endpoint === 'investment_category_breakdown') {
            if (lastCategory !== null) {
                changeGraph(endpoint, lastCategory);
            }
            else {
                // if there is no last category get our options and choose the first one
                const options = await updateOptions(); 
                changeGraph(
                    endpoint, 
                    categoryOptions.length === 0 ? options['categories'][0] : categoryOptions[0]
                );
            }    
        }
        else if (endpoint === 'investment_categories') {
            changeGraph(endpoint);
        }
    }


    return (
        <div className="investment-graphs flex flex-row min-h-[70vh] max-h-[70vh]">
            <div className="tab graph-names flex flex-col mr-2 w-40">
                <button className={"tablinks text-white text-center text-base cursor-pointer border-r-2 px-3 py-[2rem] align-center border-b-2" + (overviewActive ? " active bg-gradient-to-l from-violet-500 to-transparent" : "") } onClick={() => handleTabClick('investment_categories')}>
                    Overview
                </button>
                <button className={"tablinks text-white text-center text-base cursor-pointer border-r-2 px-3 py-[2rem] align-center border-b-2" + (categoryActive ? " active bg-gradient-to-l from-violet-500 to-transparent" : "") } onClick={() => handleTabClick('investment_category_breakdown')}>
                    Category
                    </button>
                <button className={"tablinks text-white text-center text-base cursor-pointer border-r-2 px-3 py-[2rem] align-center" + (stocksActive ? " active bg-gradient-to-l from-violet-500 to-transparent" : "") } onClick={() => handleTabClick('stock_history')}>
                    Stocks?
                </button>
            </div>

            <div className="tabcontent ml-2 w-full bg-gradient-to-r from-violet-500 to-violet-600 rounded-3xl shadow-lg p-4">
                {graph}
            </div>
        </div>
    );
}

export default InvestmentGraphs;
