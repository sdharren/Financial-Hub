import './App.css';
import React from 'react';
import './styles.css'
import Navbar from './components/Navbar';
import About from './pages/About';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import PrivateRoutes from './utils/PrivateRoute';
import OnlyPublicRoutes from './utils/OnlyPublicRoute';
import { AuthProvider } from './context/AuthContext';
import Link from './pages/Link';
import RecentTransactions from './dashboard_components/RecentTransactionsDisplay';
import SectorSpending from './pages/SectorSpendingDisplay';
import LinkAssets from './pages/LinkAssets';
import Accounts from './pages/Accounts';
import CryptoWalletAddresses from './pages/CryptoWalletAddresses';

function App() {
  return (
    <div className = "bg-[url('./images/background-image.png')]">
      <div className= 'mx-20 max-w-full min-h-screen font-["Outfit"]'>
      <Router>
        <AuthProvider>
          <Navbar />

            <Routes>
              <Route element={<PrivateRoutes/>}>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/plaid_link" element={<Link linkToken="link-development-6625c6ff-c671-4997-8923-550a7a26ed41"/>}/>
                <Route path="/link_assets" element={<LinkAssets />} />
                <Route path="/accounts" element={<Accounts />} />
                <Route path="/crypto_addresses" element={<CryptoWalletAddresses />} />
              </Route>
              <Route element={<OnlyPublicRoutes />}>
                <Route path="/login" element={<Login/>} />
                <Route path="/signup" element={<Signup />} />
              </Route>
              <Route path="/" element={<Home />} />
              <Route path="/about" element={<About />} />
              <Route path='*' element={<Home />} />
            </Routes>

        </AuthProvider>
      </Router>
      </div>
    </div>
  );
}

export default App;
