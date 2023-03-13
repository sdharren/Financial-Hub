
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
import PieChart from './pages/PieChart';
import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom"
import GraphDisplay from './pages/GraphDisplay';
import PrivateRoutes from './utils/PrivateRoute';
import { AuthProvider } from './context/AuthContext';

// ask matthew about how margins are lined

function App() {
  return (
    <div>
      <Router>
        <AuthProvider>
          <Navbar />
          <div className="min-h-full  flex items-center justify-center py-36 px-4 sm:px-6 lg:px-8">
          <div className="max-w-md w-full space-y-8">
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
            </Routes>
          </div>
          </div>
          </div>
        </AuthProvider>
      </Router>
    </div>
  );
}

export default App;
