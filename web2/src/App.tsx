import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Link, Outlet, Navigate } from "react-router-dom";
import axios from "axios";

import Login from "./components/Login";
import Register from "./components/Register";
import Home from "./components/Home";

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

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
    delete axios.defaults.headers.common["Authorization"];
  };

  return (
    <BrowserRouter>
      <nav>
        {isLoggedIn ? (
          <>
            <Link to="/">Home</Link>
            <button onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </nav>
      <Routes>
        <Route path="/" element={isLoggedIn ? <Home /> : <Navigate to="/login" />} />
        <Route path="/login" element={isLoggedIn ? <Navigate to="/" /> : <Login setIsLoggedIn={setIsLoggedIn}/>} />
        <Route path="/register" element={isLoggedIn ? <Navigate to="/" /> : <Register />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
