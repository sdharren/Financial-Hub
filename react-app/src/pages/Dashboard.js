import React, { useState, useEffect } from 'react';


function Dashboard() {
  const [activeTabPie, setActiveTabPie] = useState('Overall');

  const [activeGraphPie, setActiveGraphPie] = useState('Graph 1');

  const [selectedPieAccount, setSelectedPieAccount] = useState("All Accounts");


  const handlePieTabClick = (tabName) => {
    setActiveTabPie(tabName);
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
              <div
                className={`piechart-tab ${activeTabPie === 'Overall' ? 'active' : ''}`}
                onClick={() => handlePieTabClick('Overall')}
              >
                Overall
              </div>
              <div
                className={`piechart-tab ${activeTabPie === 'Stocks' ? 'active' : ''}`}
                onClick={() => handlePieTabClick('Stocks')}
              >
                Stocks
              </div>
              <div
                className={`piechart-tab ${activeTabPie === 'Banks' ? 'active' : ''}`}
                onClick={() => handlePieTabClick('Banks')}
              >
                Banks
              </div>
              <div
                className={`piechart-tab ${activeTabPie === 'Crypto' ? 'active' : ''}`}
                onClick={() => handlePieTabClick('Crypto')}
              >
                Crypto
              </div>
            </div>
            <div className="piechart-container">
              <div className="piechart-graphs">
                <div
                  className={`piechart-graph ${activeGraphPie === 'Graph 1' ? 'active' : ''}`}
                  onClick={() => handlePieGraphClick('Graph 1')}
                >
                  Graph 1
                </div>
                <div
                  className={`piechart-graph ${activeGraphPie === 'Graph 2' ? 'active' : ''}`}
                  onClick={() => handlePieGraphClick('Graph 2')}
                >
                  Graph 2
                </div>
                <div
                  className={`piechart-graph ${activeGraphPie === 'Graph 3' ? 'active' : ''}`}
                  onClick={() => handlePieGraphClick('Graph 3')}
                >
                  Graph 3
                </div>
                <div
                  className={`piechart-graph ${activeGraphPie === 'Graph 4' ? 'active' : ''}`}
                  onClick={() => handlePieGraphClick('Graph 4')}
                >
                  Graph 4
                </div>
              </div>
              
              <div className="piegraph-content">
                {activeTabPie === 'Overall' && activeGraphPie === 'Graph 1' && (
                  <p>{`Content for ${activeGraphPie} in ${activeTabPie} tab goes here.`}</p>
                )}
                {activeTabPie === 'Overall' && activeGraphPie === 'Graph 2' && (
                  <p>{`Content for ${activeGraphPie} in ${activeTabPie} tab goes here.`}</p>
                )}
                {activeTabPie === 'Overall' && activeGraphPie === 'Graph 3' && (
                  <p>{`Content for ${activeGraphPie} in ${activeTabPie} tab goes here.`}</p>
                )}
                {activeTabPie === 'Overall' && activeGraphPie === 'Graph 4' && (
                  <p>{`Content for ${activeGraphPie} in ${activeTabPie} tab goes here.`}</p>
                )}
                {activeTabPie === 'Stocks' && activeGraphPie === 'Graph 1' && (
                  <p>{`Content for ${activeGraphPie} in ${activeTabPie} tab goes here.`}</p>
                )}
                {activeTabPie === 'Stocks' && activeGraphPie === 'Graph 2' && (
                  <p>{`Content for ${activeGraphPie} in ${activeTabPie} tab goes here.`}</p>
                )}
                {activeTabPie === 'Stocks' && activeGraphPie === 'Graph 3' && (
                  <p>{`Content for ${activeGraphPie} in ${activeTabPie} tab goes here.`}</p>
                )}
                {activeTabPie === 'Stocks' && activeGraphPie === 'Graph 4' && (
                  <p>{`Content for ${activeGraphPie} in ${activeTabPie} tab goes here.`}</p>
                )}
                {activeTabPie === 'Banks' && activeGraphPie === 'Graph 1' && (
                  <p>{`Content for ${activeGraphPie} in ${activeTabPie} tab goes here.`}</p>
                )}
                {activeTabPie === 'Banks' && activeGraphPie === 'Graph 2' && (
                  <p>{`Content for ${activeGraphPie} in ${activeTabPie} tab goes here.`}</p>
                )}
                {activeTabPie === 'Banks' && activeGraphPie === 'Graph 3' && (
                  <p>{`Content for ${activeGraphPie} in ${activeTabPie} tab goes here.`}</p>
                )}
                {activeTabPie === 'Banks' && activeGraphPie === 'Graph 4' && (
                  <p>{`Content for ${activeGraphPie} in ${activeTabPie} tab goes here.`}</p>
                )}
                {activeTabPie === 'Crypto' && activeGraphPie === 'Graph 1' && (
                  <p>{`Content for ${activeGraphPie} in ${activeTabPie} tab goes here.`}</p>
                )}
                {activeTabPie === 'Crypto' && activeGraphPie === 'Graph 2' && (
                  <p>{`Content for ${activeGraphPie} in ${activeTabPie} tab goes here.`}</p>
                )}
                {activeTabPie === 'Crypto' && activeGraphPie === 'Graph 3' && (
                  <p>{`Content for ${activeGraphPie} in ${activeTabPie} tab goes here.`}</p>
                )}
                {activeTabPie === 'Crypto' && activeGraphPie === 'Graph 4' && (
                  <p>{`Content for ${activeGraphPie} in ${activeTabPie} tab goes here.`}</p>
                )}
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
