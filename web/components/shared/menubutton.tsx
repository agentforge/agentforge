import React from 'react';
import Link from 'next/link';

interface MenuButtonProps {
  route: string;
  children: React.ReactNode;
}

const MenuButton: React.FC<MenuButtonProps> = ({ route, children }) => {
  return (
    <Link
        href={route}
        className="w-full h-9 mb-3 flex justify-center items-center border border-gray-200 bg-transparent hover:bg-slate-500 transition-all text-white"
      >
        {children}
    </Link>
  );
}

export default MenuButton;