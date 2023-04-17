// NavMenu.tsx
import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

interface NavMenuItem {
  text: string;
  onClick: () => void;
}

interface NavMenuProps {
  isLoggedIn: boolean;
  handleLogout: () => void;
}

const NavMenu: React.FC<NavMenuProps> = ({ isLoggedIn, handleLogout }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const isConfigurePage = location.pathname === '/configure';

  const navMenuItems: NavMenuItem[] = isLoggedIn
    ? [
        {
          text: isConfigurePage ? 'Forum' : 'Configure',
          onClick: () => navigate(isConfigurePage ? '/' : '/configure'),
        },
        { text: 'Logout', onClick: handleLogout },
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
