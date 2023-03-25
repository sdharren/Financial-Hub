import React, { useState } from 'react';
import InvestmentGraphs from './InvestmentGraphs';
import Balances from './Balances';
import Transactions from './RecentTransactionsDisplay';
import Currency from './Currency';
import BarChart from './TransactionDisplay';
import BarChartDisplay from './SectorSpending';


const tabGraphData = {
  Overall: [
    { name: 'Graph 1', content: `Content for Graph 1 in Overall tab goes here.` },
    { name: 'Graph 2', content: `Content for Graph 2 in Overall tab goes here.` },
    { name: 'Graph 3', content: `Content for Graph 3 in Overall tab goes here.` },
    { name: 'Graph 4', content: `Content for Graph 4 in Overall tab goes here.` },
  ],
  Banks: [
    { name: 'Balance', content: <Balances /> },
    { name: 'Recent Transactions', content: <Transactions /> },
    { name: 'Currency', content: <Currency /> },
    { name: 'Bar Chart', content: <BarChart /> },
    { name: 'Sector Spending', content: <BarChartDisplay /> }
  ],
  Stocks: [
    { name: 'Graph 1', content: <InvestmentGraphs/>}
  ],
  
  Crypto: [
    { name: 'Graph 1', content: `Content for crypto 1 in Crypto tab goes here.` },
    { name: 'Graph 2', content: `Content for crypto 2 in Crypto tab goes here.` },
    { name: 'Graph 3', content: `Content for crypto 3 in Crypto tab goes here.` },
  ],
};

const lastGraphBorder = (tabName) => {
    // if (tabName === '')
}

function Dashboard() {
  const [activeTabPie, setActiveTabPie] = useState('Overall');
  const [stocksActive, setStocksActive] = useState(false);

  const [activeGraphPie, setActiveGraphPie] = useState('Graph 1');

  const [selectedPieAccount, setSelectedPieAccount] = useState("All Accounts");


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

  



  const handlePieAccountChange = (event) => {
    setSelectedPieAccount(event.target.value);
  };

    let page1 = (
        <div>
          
          <div className="dashboard-container">
            <div className="piechart-box">
              <div className ="piechart-section">
                <div className="piechart-tabs">
                  {Object.keys(tabGraphData).map((tabName) => (
                    <div
                      key={tabName}
                      className={`piechart-tab ${activeTabPie === tabName ? 'active' : ''}`}
                      onClick={() => handlePieTabClick(tabName)}
                    >
                      {tabName}
                    </div>
                  ))}
                </div>
                <div className="piechart-container">
                  <div className="piechart-graphs">
                    {tabGraphData[activeTabPie].map((graph) => (
                      <div
                        hidden={stocksActive}
                        key={graph.name}
                        className={`piechart-graph ${activeGraphPie === graph.name ? 'active' : ''}`}
                        onClick={() => handlePieGraphClick(graph.name)}
                      >
                        {graph.name}
                      </div>
                    ))}
                  </div>
                  
                  <div className="piegraph-content" style={stocksActive ? {border:'0px solid white'} : {}}>
                    {tabGraphData[activeTabPie].map((graph) => (
                      activeGraphPie === graph.name && <p key={graph.name}>{graph.content}</p>
                    ))}
                  </div>
    
                  <div className="right-menu" hidden={stocksActive}>
                    <select value={selectedPieAccount} onChange={handlePieAccountChange}>
                      <option value="All Accounts">All Accounts</option>
                      <option value="Account 1">Account 1</option>
                    </select>
                  </div>
    
                </div>
              </div>
              
              <div className="piegraph-content" style={stocksActive ? {border:'0px solid white'} : {}}>
                {tabGraphData[activeTabPie].map((graph) => (
                  activeGraphPie === graph.name && <p key={graph.name}>{graph.content}</p>
                ))}
              </div>

              

            </div>
          </div>
        
    
        </div>
        
      );

    let page2 = (
        <div className='dashboard-container my-10px py-10 px-5'>
            <div className='dashboard-catagories flex flex-row justify-between mb-10'>
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
            <div className='graph-container flex flex-row'>
                <div className='graph-names flex flex-col mr-2 w-40'>
                    {tabGraphData[activeTabPie].map((graph) => (
                      <div
                        hidden={stocksActive}
                        key={graph.name}
                        className={`piechart-graph ${activeGraphPie === graph.name ? 'active bg-gradient-to-l from-violet-500 to-transparent' : ''} text-white text-center text-base cursor-pointer border-r-2 px-3 py-[4.25rem] align-center ${graph == tabGraphData[activeTabPie][tabGraphData[activeTabPie].length - 1] ? '' : 'border-b-2'}`}
                        onClick={() => handlePieGraphClick(graph.name)}
                      >
                        {graph.name}
                      </div>
                    ))}
                </div>
                <div className='graph ml-2 w-full bg-gradient-to-r from-violet-500 to-violet-600 rounded-3xl shadow-lg p-10'>
                    {tabGraphData[activeTabPie].map((graph) => (
                      activeGraphPie === graph.name && <div key={graph.name}>{graph.content}</div>
                    ))}
                </div>

            </div>

        </div>
    )  

    return page2
}

// keep the main dashboard element the same size, calculate the rem, make the table scroll, make eveyr other graph fit in
export default Dashboard;
