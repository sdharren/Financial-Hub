
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
import LineGraph from './pages/LineGraph';
import BarChartDisplay from './pages/BarChartDisplay';
import PieChart from './pages/PieChart';
import BalancesDisplay from './pages/Balances';
import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom"
import GraphDisplay from './pages/GraphDisplay';
import PrivateRoutes from './utils/PrivateRoute';
import { AuthProvider } from './context/AuthContext';
import Link from './pages/Link';

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
              <Route path="/bar_graph_display" element={<BarChartDisplay />} />
              <Route path="/line_graph" element={<LineGraph />} />
              <Route path="/plaid_link" element={<Link linkToken="link-development-414e1884-f61c-43bb-a782-b23145f9f3c5"/>}/>
              <Route path="/balances" element={<BalancesDisplay />} />
            </Routes>
          </div>
        </AuthProvider>
      </Router>
    </div>
  );
}

export default App;
