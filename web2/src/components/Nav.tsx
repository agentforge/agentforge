// NavMenu.tsx
import React from 'react';
import { useNavigate } from 'react-router-dom';

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
  const navMenuItems: NavMenuItem[] = isLoggedIn
    ? [
        { text: 'Configure', onClick: () => navigate('/configure') },
        { text: 'Logout', onClick: handleLogout },
      ]
    : [
        { text: 'Register', onClick: () => navigate('/register') },
        { text: 'Login', onClick: () => navigate('/login') },
      ];

  return (
    <nav className="nav-menu">
      <div className="nav-header">Logo</div>
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
