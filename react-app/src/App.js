
import './App.css';
import React from 'react';
import './styles.css';
import Navbar from './Navbar';
import About from './pages/About';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Graphs from './pages/Graphs';
import BarChartDisplay from './pages/BarChartDisplay';
import { Route, Routes } from "react-router-dom";
import PieChart from './pages/PieChart';
// import { Route, Routes, useNavigate } from "react-router-dom";
import GraphDisplay from './pages/GraphDisplay';


function App() {
  return (
    <>
      <Navbar />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/bar_graph" element={<BarChartDisplay />} />
          <Route path="/graph_display" element={<GraphDisplay />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
