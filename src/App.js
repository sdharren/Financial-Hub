import './App.css';
import React from 'react';
import './styles.css'
import Navbar from './components/Navbar';
import About from './pages/About';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Home from './pages/Home';
import HomePage from './pages/HomePage';
import Dashboard from './pages/Dashboard';
import TotalAssetsDisplay from './pages/TotalAssets'
import BarGraph from './dahsboard_components/BarGraph';
import TransactionDisplay from './pages/TransactionDisplay';
import RecentTransactions from './dahsboard_components/RecentTransactionsDisplay';
import PieChart from './dahsboard_components/PieChart';
import BalancesDisplay from './pages/BalancesDisplay';
import BarChartDisplay from './pages/TransactionDisplay';
import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom"
import InvestmentGraphs from './pages/InvestmentGraphs';
import PrivateRoutes from './utils/PrivateRoute';
import { AuthProvider } from './context/AuthContext';
import Link from './pages/Link';
import Currency from './pages/Currency';
import RecentTransactions from './dahsboard_components/RecentTransactionsDisplay';
import LineIndexComparisonChart from './pages/LineIndexComparisonChart';

// ask matthew about how margins are lined
import CurrencyDisplay from './pages/CurrencyDisplay';
// import TransactionTable
import LineGraph from './dahsboard_components/LineGraph';

// ask matthew about how margins are lined
import SectorSpending from './pages/SectorSpendingDisplay';
import LinkAssets from './pages/LinkAssets';
import Accounts from './pages/Accounts';
import CryptoWalletAddresses from './pages/CryptoWalletAddresses';

// ask matthew about how margins are lined

function App() {
  return (
    <div className = "bg-[url('./images/background-image.png')]">
      <div className= 'mx-20 max-w-full min-h-screen font-["Outfit"]'>
      <Router>
        <AuthProvider>
          <Navbar />

            <Routes>
              <Route element={<PrivateRoutes/>}>
                <Route element={<HomePage/>} path = "/homepage" exact />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/transactions" element={<TransactionDisplay />} />
                <Route path="/sector_spending" element={<SectorSpending/>} />
                <Route path="/total_assets" element={<TotalAssetsDisplay/>} />
                {/* plaid link should throw an error if a user tries to access it (only accessible via link_assets component) */}
                <Route path="/plaid_link" element={<Link linkToken="link-development-6625c6ff-c671-4997-8923-550a7a26ed41"/>}/>

                <Route path="/balances" element={<BalancesDisplay />} />
                <Route path="/currency" element={<CurrencyDisplay />} />
                <Route path="/list" element={<TransactionDisplay />} />
                <Route path="/link_assets" element={<LinkAssets />} />
                <Route path="/accounts" element={<Accounts />} />
                <Route path="/portfolio_comparison" element={<LineIndexComparisonChart />} />
                {/* <Route path="/bankassets" element={<AssetBank />} /> */}
              </Route>
              <Route path="/login" element={<Login/>} />
              <Route path="/" element={<Home />} />
              <Route path="/about" element={<About />} />
              <Route path="/signup" element={<Signup />} />

              <Route path="/crypto_addresses" element={<CryptoWalletAddresses />} />
            </Routes>

        </AuthProvider>
      </Router>
      </div>
    </div>
  );
}

export default App;
