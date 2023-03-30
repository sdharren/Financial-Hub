/**
 * Creates the main dashboard component. Dashboard contains the category tabs
 * and renders the graph names and the graphs for each category of Overall, 
 * Stocks, Banks and Crypto
 */
import React, { useState } from 'react';
import InvestmentGraphs from './InvestmentGraphs';
import BalancesDisplay from './BalancesDisplay';
import RecentTransactions from '../dashboard_components/RecentTransactionsDisplay';
import CurrencyDisplay from './CurrencyDisplay';
import BarChart from './TransactionDisplay';
import BarChartDisplay from './SectorSpendingDisplay';
import TotalAssetsDisplay from './TotalAssets';
import CPie from '../dashboard_components/CryptoPieChart';
import CScatter from '../dashboard_components/ScatterGraph';
import CRecentTransactionsDisplay from '../dashboard_components/CryptoRecentTransactionsDisplay';
import CAdditional from '../dashboard_components/AdditionalData';
import { backgroundBox, dashboardGraphContainer } from '../static/styling';


function Dashboard() {
  const [activeTabPie, setActiveTabPie] = useState('Overall');
  const [stocksActive, setStocksActive] = useState(false);

  const [activeGraphPie, setActiveGraphPie] = useState('Total Asset Breakdown');

  const [selectedPieAccount, setSelectedPieAccount] = useState("All Accounts");

  // tailwind.css styling for tabs, highlight tab and graph tab styling
  const tabStyling = ' text-white text-center text-lg w-full cursor-pointer border-b-2 pb-2 '
  const highlightedTabStyling = 'active bg-gradient-to-t from-violet-500 to-transparent'
  const graphtabStyling = 'text-white text-center text-base cursor-pointer border-r-2 px-3 py-[1.5rem] align-center'

  function handleClicked(event){
    console.log(event.next)
    if (event.next==="Bank Assets"){
      handlePieTabClick('Banks')
    }
    else if (event.next==="Crypto Assets"){
      handlePieTabClick('Crypto')
    }
    else{
      handlePieTabClick('Stocks')
    }
  }
  
  const tabGraphData = {
    Overall: [
      { name: 'Total Asset Breakdown', content:<TotalAssetsDisplay handleClicked={handleClicked}/> },
    ],
    Stocks: [
      { name: 'Graph 1', content: <InvestmentGraphs/>}
    ],
    Banks: [
      { name: 'Balance Breakdown', content: <BalancesDisplay /> },
      { name: 'Recent Transactions', content: <RecentTransactions /> },
      { name: 'Currency Breakdown', content: <CurrencyDisplay /> },
      { name: 'Spending Habits', content: <BarChart /> },
      { name: 'Sector Spending', content: <BarChartDisplay /> }
    ],
    Crypto: [
      { name: 'Pie Chart', content: <CPie /> },
      { name: 'Scatter Graph', content: <CScatter /> },
      { name: 'Wallet Data', content: <CAdditional /> },
      { name: 'Transactions Table', content: <CRecentTransactionsDisplay /> },
    ]
  };

  const handlePieTabClick = (tabName) => {
    if (tabName === 'Stocks') {
        setStocksActive(true);
    }
    else {
        setStocksActive(false);
    }
    setActiveTabPie(tabName);
    setActiveGraphPie(tabGraphData[tabName][0].name);
  };

  const handlePieGraphClick = (graphName) => {
    setActiveGraphPie(graphName);
  };

    let page2 = (
        <div className='dashboard-container my-10px py-10 px-5'>
            <div data-testid='graph-tabs' className='dashboard-catagories flex flex-row justify-between mb-10'>
                {Object.keys(tabGraphData).map((tabName) => (
                    <div
                      key={tabName}
                      className={`piechart-tab ${activeTabPie === tabName ? 'active bg-gradient-to-t from-violet-500 to-transparent' : ''} text-white text-center text-lg w-full cursor-pointer border-b-2 pb-2 ${tabName == Object.keys(tabGraphData)[Object.keys(tabGraphData).length - 1] ? '' : 'border-r-2'}`}
                      onClick={() => handlePieTabClick(tabName)}
                    >
                      {tabName}
                    </div>
                ))}
            </div>
            {activeTabPie === 'Stocks' ? <InvestmentGraphs /> : 
            (<div className={'graph-container ' + dashboardGraphContainer}>
                <div data-testid = 'graph-names' className='graph-names flex flex-col mr-2 w-40 justify-start'>
                    {tabGraphData[activeTabPie].map((graph) => (
                      <div
                        hidden={stocksActive}
                        key={graph.name}
                        className={`piechart-graph ${activeGraphPie === graph.name ? 'active bg-gradient-to-l from-violet-500 to-transparent' : ''} text-white text-center text-base cursor-pointer border-r-2 px-3 py-[1.5rem] align-center ${graph == tabGraphData[activeTabPie][tabGraphData[activeTabPie].length - 1] ? '' : 'border-b-2'}`}
                        onClick={() => handlePieGraphClick(graph.name)}
                      >
                        {graph.name}
                      </div>
                    ))}
                </div>
                <div className={'graph ml-2 w-full p-10 ' + backgroundBox}>
                    {tabGraphData[activeTabPie].map((graph) => (
                      activeGraphPie === graph.name && <div key={graph.name} className=''>{graph.content}</div>
                    ))}
                </div>
            </div>)}

        </div>
    )  

    return page2
}

export default Dashboard;