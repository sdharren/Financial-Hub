
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
import BarGraph from './pages/BarGraph';
import BarChartDisplay from './pages/BarChartDisplay';
import PieChart from './pages/PieChart';
import BalancesDisplay from './pages/Balances';
import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom"
import InvestmentGraphs from './pages/InvestmentGraphs';
import PrivateRoutes from './utils/PrivateRoute';
import { AuthProvider } from './context/AuthContext';
import Link from './pages/Link';
import Currency from './pages/Currency';
import TransactionTable from './pages/RecentTransactionsDisplay';
import SectorSpending from './pages/SectorSpending';
import LinkAssets from './pages/LinkAssets';
import Accounts from './pages/Accounts';
import CryptoWalletAddresses from './pages/CryptoWalletAddresses';

// ask matthew about how margins are lined

function App() {
  return (
    <div>
      <Router>
        <AuthProvider>
          <Navbar />

            <Routes>
              <Route element={<PrivateRoutes/>}>
                <Route element={<HomePage/>} path = "/homepage" exact />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/bar_graph_display" element={<BarChartDisplay />} />
                <Route path="/sector_spending" element={<SectorSpending/>} />

                {/* plaid link should throw an error if a user tries to access it (only accessible via link_assets component) */}
                <Route path="/plaid_link" element={<Link linkToken="link-development-6625c6ff-c671-4997-8923-550a7a26ed41"/>}/>

                <Route path="/balances" element={<BalancesDisplay />} />
                <Route path="/currency" element={<Currency />} />
                <Route path="/list" element={<TransactionTable />} />
                <Route path="/link_assets" element={<LinkAssets />} />
                <Route path="/accounts" element={<Accounts />} />
                {/* <Route path="/bankassets" element={<AssetBank />} /> */}
              </Route>
              <Route path="/login" element={<Login/>} />
              <Route path="/" element={<Home />} />
              <Route path="/about" element={<About />} />
              <Route path="/signup" element={<Signup />} />

<<<<<<< HEAD
              <Route path="/plaid_link" element={<Link />}/>
              {/* plaid link should throw an error if a user tries to access it (only accessible via link_assets component) */}

              <Route path="/bar_graph_display" element={<BarChartDisplay />} />
              <Route path="/plaid_link" element={<Link linkToken="link-development-6625c6ff-c671-4997-8923-550a7a26ed41"/>}/>

              <Route path="/plaid_link" element={<Link />}/>
              {/* plaid link should throw an error if a user tries to access it (only accessible via link_assets component) */}
              <Route path="/bar_graph_display" element={<BarChartDisplay />} />
              <Route path="/plaid_link" element={<Link linkToken="link-development-6625c6ff-c671-4997-8923-550a7a26ed41"/>}/>
              <Route path="/balances" element={<BalancesDisplay />} />
              <Route path="/currency" element={<Currency />} />
              <Route path="/list" element={<TransactionTable />} />
              <Route path="/link_assets" element={<LinkAssets />} />
              <Route path="/accounts" element={<Accounts />} />
              <Route path="/crypto_addresses" element={<CryptoWalletAddresses />} />
=======
>>>>>>> main
            </Routes>

        </AuthProvider>
      </Router>
    </div>
  );
}

export default App;
