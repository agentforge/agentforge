import React from 'react';
import VideoComponent from '@/components/shared/video';
import MenuButton from '@/components/shared/menubutton';

interface SidebarProps {}

const Sidebar: React.FC<SidebarProps> = () => {
  return (
    <>
    <div className="flex flex-col h-screen justify-between">
        <VideoComponent />
        <footer>
        <MenuButton route="/forge/chat">
          Test
        </MenuButton>
        <MenuButton route="/forge/config">
          Configure
        </MenuButton>
        </footer>
    </div>
    </>
  );
};

export default Sidebar;