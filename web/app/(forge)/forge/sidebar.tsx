import React from 'react';
import VideoComponent from '@/components/shared/video';

interface SidebarProps {}

const Sidebar: React.FC<SidebarProps> = () => {
  return (
    <div className="container mx-auto">
      <VideoComponent />
  </div>
  );
};

export default Sidebar;