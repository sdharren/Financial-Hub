import React, { useState, useEffect } from 'react';
import PieChart from './PieChart';
import Balances from './Balances';
import Transactions from './RecentTransactionsDisplay';
import Currency from './Currency';
import BarChart from './BarChartDisplay';


const tabGraphData = {
  Overall: [
    { name: 'Graph 1', content: `Content for Graph 1 in Overall tab goes here.` },
    { name: 'Graph 2', content: `Content for Graph 2 in Overall tab goes here.` },
    { name: 'Graph 3', content: `Content for Graph 3 in Overall tab goes here.` },
    { name: 'Graph 4', content: `Content for Graph 4 in Overall tab goes here.` },
  ],
  Stocks: [
    { name: 'Graph 1', content: `Content for Graph 1 in Overall tab goes here.`  },
    { name: 'Graph 2', content: `Content for Graph 2 in Stocks tab goes here.` },
  ],
  Banks: [
    { name: 'Balance', content: <Balances /> },
    { name: 'Transaction', content: <Transactions /> },
    { name: 'Currency', content: <Currency /> },
    { name: 'Bar Chart', content: <BarChart /> },
  ],
  Crypto: [
    { name: 'Graph 1', content: `Content for crypto 1 in Crypto tab goes here.` },
    { name: 'Graph 2', content: `Content for crypto 2 in Crypto tab goes here.` },
    { name: 'Graph 3', content: `Content for crypto 3 in Crypto tab goes here.` },
  ],
};

function Dashboard() {
  const [activeTabPie, setActiveTabPie] = useState('Overall');

  const [activeGraphPie, setActiveGraphPie] = useState('Graph 1');

  const [selectedPieAccount, setSelectedPieAccount] = useState("All Accounts");


  const handlePieTabClick = (tabName) => {
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
                    key={graph.name}
                    className={`piechart-graph ${activeGraphPie === graph.name ? 'active' : ''}`}
                    onClick={() => handlePieGraphClick(graph.name)}
                  >
                    {graph.name}
                  </div>
                ))}
              </div>
              
              <div className="piegraph-content">
                {tabGraphData[activeTabPie].map((graph) => (
                  activeGraphPie === graph.name && <p key={graph.name}>{graph.content}</p>
                ))}
              </div>

              <div className="right-menu">
                <select value={selectedPieAccount} onChange={handlePieAccountChange}>
                  <option value="All Accounts">All Accounts</option>
                  <option value="Account 1">Account 1</option>
                </select>
              </div>

            </div>
          </div>
        </div>
      </div>
    

    </div>
    
  );
}

export default Dashboard;
