import PieChart from "../dashboard_components/PieChart";
import LineGraph from "../dashboard_components/LineGraph";
import { useState, useContext, useEffect } from "react";
import AuthContext from '../context/AuthContext';
import ReturnDisplay from "../components/ReturnDisplay";
import LineIndexComparisonChart from "../dashboard_components/LineIndexComparisonChart";
import { backgroundBox, dashboardGraphContainer } from "../static/styling";

function InvestmentGraphs() {
    // first graph to display - investments overview
    const [graph, setGraph] = useState(<PieChart endpoint={"investment_categories"} loadNext={handleLoadNext} currency={'$'} />);
    let {authTokens, logoutUser} = useContext(AuthContext);

    // options for each graph tab so user can select asset to show in graph
    const [categoryOptions, setCategoryOptions] = useState([]);
    const [investmentOptions, setInvestmentOptions] = useState([]);

    // keep track of which graph is currently being displayed
    const [overviewActive, setOverviewActive] = useState(true);
    const [categoryActive, setCategoryActive] = useState(false);
    const [stocksActive, setStocksActive] = useState(false);
    const [comparisonActive, setComparisonActive] = useState(false);

    // keep track of last displayed graphs so we know what to display if user switches tabs manually
    const [lastCategory, setLastCategory] = useState(null);
    const [lastStock, setLastStock] = useState(null);

    const tabStyling = "text-white text-center text-base cursor-pointer border-r-2 px-3 py-[1.5rem] align-center"
    const highlightedTabStyling = " active bg-gradient-to-l from-violet-500 to-transparent"

    // FOR DEVELOPMENT PURPOSES (use this if investments aren't linked - put onLoad={link_sandbox()} in the top div at the very bottom)
    let link_sandbox = async() => {
        let response = await fetch('api/sandbox_investments/',
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
            'investments': investmentOptions,
            'categories': categoryOptions
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
            setComparisonActive(false);
        }
        else if (graph === 'investment_category_breakdown') {
            setCategoryActive(true);
            setStocksActive(false);
            setOverviewActive(false);
            setComparisonActive(false);
        }
        else if (graph === 'stock_history') {
            setCategoryActive(false);
            setStocksActive(true);
            setOverviewActive(false);
            setComparisonActive(false);
        }
        else if (graph === 'portfolio_comparison') {
            setCategoryActive(false);
            setStocksActive(false);
            setOverviewActive(false);
            setComparisonActive(true);
        }
    }

    // render a graph based on the endpoint supplied
    // endpoint_parameter is optional and is a parameter for the API request
    async function changeGraph(endpoint, endpoint_parameter) {
        const options = await updateOptions();

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
                            currency={'$'}
                        />
                    </div>
                );
                changeTabActive(endpoint);
                break;

            case 'investment_category_breakdown':
                if (!options['categories'].includes(endpoint_parameter)) {
                    break;
                }
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
                            currency={'$'}
                        />
                    </div>
                );
                changeTabActive(endpoint);
                break;

            case 'stock_history':
                if (!options['investments'].includes(endpoint_parameter)) {
                    break;
                }
                let returns = await getReturns('returns', endpoint_parameter);
                setLastStock(endpoint_parameter);
                setGraph(
                        <div className="inline-block min-h-[60vh] max-h-[60vh] w-full">
                            <ReturnDisplay returns={returns}/>
                            <LineGraph 
                                endpoint={endpoint} 
                                updateGraph={handleGraphUpdate} 
                                endpoint_parameter={endpoint_parameter} 
                                selectOptions={ options['investments'] } 
                                currency={'$'}
                            />
                            </div>
                    );
                changeTabActive(endpoint);
                break;
            
            case 'portfolio_comparison':
                const comparisonOptions = ["^GSPC","^FTSE", "^DJI", "^STOXX50E", "^GDAXI"];
                if (endpoint_parameter === null || endpoint_parameter === undefined) {
                    var endpoint_parameter = comparisonOptions[0];
                }
                setGraph(
                    <div className="inline-block min-h-[60vh] max-h-[60vh] w-full">
                        <LineIndexComparisonChart
                            endpoint={endpoint}
                            updateGraph={handleGraphUpdate}
                            endpoint_parameter={endpoint_parameter}
                            selectOptions={comparisonOptions}
                        />        
                    </div>
                );
                changeTabActive(endpoint);
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
        let response = await fetch('api/' + endpoint + '/',
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
        let response = await fetch('api/' + endpoint + (endpoint==='overall_returns'?'/':'/?param='+param),
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
        else if (endpoint === 'portfolio_comparison') {
            changeGraph(endpoint);
        }
    }


    return (
        <div className={"investment-graphs " + dashboardGraphContainer}>
            <div data-testid='graph-names' className="tab graph-names flex flex-col mr-2 w-40 justify-start">
                <button className={'tablinks border-b-2 ' + tabStyling + (overviewActive ? highlightedTabStyling : "") } onClick={() => handleTabClick('investment_categories')}>
                    Overview
                </button>
                <button className={'tablinks border-b-2 ' + tabStyling + (categoryActive ? highlightedTabStyling : "") } onClick={() => handleTabClick('investment_category_breakdown')}>
                    Category
                    </button>
                <button className={'tablinks border-b-2 ' + tabStyling + (stocksActive ? highlightedTabStyling : "") } onClick={() => handleTabClick('stock_history')}>
                    Stock Breakdown
                </button>
                <button className={'tablinks ' + tabStyling + (comparisonActive ? highlightedTabStyling : "") } onClick={() => handleTabClick('portfolio_comparison')}>
                    Portfolio Comparison
                </button>
            </div>

            <div className={"tabcontent ml-2 w-full p-4 " + backgroundBox}>
                {graph}
            </div>
        </div>
    );

};

export default InvestmentGraphs;
