// NavMenu.tsx
import React, { useState, useRef } from 'react';
import { CSSTransition } from 'react-transition-group';
import { Link } from 'react-router-dom';

interface NavMenuItem {
  text: string;
  onClick: () => void;
}

interface NavMenuProps {
  isLoggedIn: boolean;
  handleLogout: () => void;
}

const NavMenu: React.FC<NavMenuProps> = ({ isLoggedIn, handleLogout }) => {
  const [menuOpen, setMenuOpen] = useState<boolean>(false);

  const navMenuItems: NavMenuItem[] = [
    { text: 'Register', onClick: () => {} },
    { text: 'Login', onClick: () => {} },
    { text: 'Logout', onClick: handleLogout },
    { text: 'New Chat', onClick: () => console.log('New Chat') },
    { text: 'Configure', onClick: () => console.log('Configure') },
  ];

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  
  return (
    <nav className="nav-menu">
      <div className="nav-header">
        <button onClick={toggleMenu}>Menu</button>
      </div>
      <CSSTransition
        in={menuOpen}
        timeout={200}
        classNames="slide-menu"
      >
         <ul className="menu-items">

          {navMenuItems.map((item, index) => (
            <li key={index} onClick={item.onClick}>
              {item.text}
            </li>
          ))}
        </ul>
      </CSSTransition>
    </nav>
  );
};

export default NavMenu;
