// NavMenu.tsx
import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import api from './api';
import axios from 'axios';

interface NavMenuItem {
  text: string;
  onClick: () => void;
}

interface NavMenuProps {
  isLoggedIn: boolean;
  setIsLoggedIn?: React.Dispatch<React.SetStateAction<boolean>>;
}

const NavMenu: React.FC<NavMenuProps> = ({ isLoggedIn, setIsLoggedIn }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const isConfigurePage = location.pathname === '/configure';

  const handleLogout = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('No token found');
      return;
    }
    if (!setIsLoggedIn) {
      console.error('Malformed handleLogout call');
      return;
    }
    // Functionally log user out of the app
    function bye() {
      console.log('bye');
      localStorage.removeItem('token');
      if (setIsLoggedIn) {
        setIsLoggedIn(false);
      }
      delete axios.defaults.headers.common['Authorization'];
      navigate('/login');
    }
    try {
      const response = await api.post(`/logout`, {
        method: 'POST',
        credentials: 'include', // Include cookies in the request
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      });
      console.log(response.status);
      if (response.status == 200) {
        bye();
      } else {
        throw new Error('Logout failed');
      }
    } catch (error: any) {
      if (error.response.status == 401) {
        bye();
      } else {
        console.error('Error:', error);
      }
    }
  };

  const navMenuItems: NavMenuItem[] = isLoggedIn
    ? [
        {
          text: isConfigurePage ? 'Forum' : 'Configure',
          onClick: () => navigate(isConfigurePage ? '/' : '/configure'),
        },
        { text: 'Logout', onClick: () => handleLogout() },
      ]
    : [
        { text: 'Register', onClick: () => navigate('/register') },
        { text: 'Login', onClick: () => navigate('/login') },
      ];

  return (
    <nav className="nav-menu">
      <div className="nav-header">
        <a href="/">
          <img className="logo" src="/logo.png" alt="Logo" />
        </a>
      </div>
      <ul className="menu-items">
        {navMenuItems.map((item, index) => (
          <li key={index} onClick={item.onClick}>
            {item.text}
          </li>
        ))}
      </ul>
    </nav>
  );
};
export default NavMenu;
