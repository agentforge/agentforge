import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import axios from 'axios';
import config from './config/config';

import Login from './components/Login';
import Register from './components/Register';
import Home from './components/Home';
import Configure from './components/Configure';
import NavMenu from './components/Nav';

import './dist/css/bootstrap.min.css';
import api from './components/api';

interface AppProps {}

const App: React.FC<AppProps> = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      setIsLoggedIn(true);
    }
  }, []);

  return (
    <BrowserRouter>
      <NavMenu isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
      <Routes>
        <Route path="/" element={isLoggedIn ? <Home /> : <Navigate to="/login" />} />
        <Route path="/login" element={isLoggedIn ? <Navigate to="/" /> : <Login setIsLoggedIn={setIsLoggedIn} />} />
        <Route path="/register" element={isLoggedIn ? <Navigate to="/" /> : <Register />} />
        <Route path="/configure" element={isLoggedIn ? <Configure /> : <Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
