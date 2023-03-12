
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
import GraphDisplay from './pages/GraphDisplay';
import PrivateRoutes from './utils/PrivateRoute';
import { AuthProvider } from './context/AuthContext';
import Link from './pages/Link';
import Currency from './pages/Currency';
import TransactionTable from './pages/RecentTransactionsDisplay';

function App() {
  return (
    <div>
      <Router>
        <AuthProvider>
          <Navbar />
          <div className="container">
            <Routes>
              <Route element={<PrivateRoutes/>}>
                <Route element={<HomePage/>} path = "/homepage" exact />
              </Route>
              <Route element={<Login/>} path="/login"/>
              <Route path="/" element={<Home />} />
              <Route path="/about" element={<About />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/graph_display" element={<GraphDisplay />} />
              <Route path="/plaid_link" element={<Link linkToken="link-development-6625c6ff-c671-4997-8923-550a7a26ed41"/>}/>
              <Route path="/balances" element={<BalancesDisplay />} />
              <Route path="/currency" element={<Currency />} />
              <Route path="/list" element={<TransactionTable />} />
            </Routes>
          </div>
        </AuthProvider>
      </Router>
    </div>
  );
}

export default App;
