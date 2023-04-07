import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import axios from "axios";
import config from "./config/config";

import Login from "./components/Login";
import Register from "./components/Register";
import Home from "./components/Home";
import NavMenu from "./components/Nav";

import './dist/css/bootstrap.min.css';

interface AppProps {}

const App: React.FC<AppProps> = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      setIsLoggedIn(true);
    }
  }, []);


  const handleLogout = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('No token found');
      return;
    }
    try {
      const response = await fetch(`${config.host}:${config.port}/logout`, {
        method: 'POST',
        credentials: 'include', // Include cookies in the request
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });
      console.log(response);
      if (response.ok) {
        localStorage.removeItem("token");
      setIsLoggedIn(false);
        delete axios.defaults.headers.common["Authorization"];
      } else {
        throw new Error('Logout failed');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };


  return (
    <BrowserRouter>
      <NavMenu isLoggedIn={isLoggedIn} handleLogout={handleLogout} />
      <Routes>
        <Route path="/" element={isLoggedIn ? <Home /> : <Navigate to="/login" />} />
        <Route path="/login" element={isLoggedIn ? <Navigate to="/" /> : <Login setIsLoggedIn={setIsLoggedIn} />} />
        <Route path="/register" element={isLoggedIn ? <Navigate to="/" /> : <Register />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
