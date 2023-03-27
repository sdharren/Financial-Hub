import React, { useState } from 'react';
import InvestmentGraphs from './InvestmentGraphs';
import Balances from './Balances';
import Transactions from './RecentTransactionsDisplay';
import Currency from './Currency';
import BarChart from './TransactionDisplay';

import { PieChart as cPie } from './CryptoGraphs/PieChart'
import { ScatterGraph as cScatter } from './CryptoGraphs/ScatterGraph'
import { RecentTransactionsDisplay as cRecentTransactionsDisplay } from './CryptoGraphs/RecentTransactionsDisplay'
import { AdditionalData as cAdditional } from './CryptoGraphs/AdditionalData'


const tabGraphData = {
  Overall: [
    { name: 'Graph 1', content: `Content for Graph 1 in Overall tab goes here.` },
    { name: 'Graph 2', content: `Content for Graph 2 in Overall tab goes here.` },
    { name: 'Graph 3', content: `Content for Graph 3 in Overall tab goes here.` },
    { name: 'Graph 4', content: `Content for Graph 4 in Overall tab goes here.` },
  ],
  Stocks: [
    { name: 'Graph 1', content: <InvestmentGraphs/>}
  ],
  Banks: [
    { name: 'Balance', content: <Balances /> },
    { name: 'Transaction', content: <Transactions /> },
    { name: 'Currency', content: <Currency /> },
    { name: 'Bar Chart', content: <BarChart /> },
  ],
  Crypto: [
    { name: 'Pie Chart', content: <cPie /> },
    { name: 'Time Scatter Graph', content: <cScatter /> },
    { name: 'Transactions Table', content: <cRecentTransactionsDisplay /> },
    { name: 'Additional Data', content: <cAdditional /> },
  ],
};

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




  return (
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

              

            </div>
          </div>
        </div>
      </div>
    

    </div>
    
  );
}

export default Dashboard;
