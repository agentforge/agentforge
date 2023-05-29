'use client';
import React from 'react';
import ModelProfilesTable from '@/components/forge/modelprofiles';

interface ConfigProps {}

const Config: React.FC<ConfigProps> = () => {

  return (
    <>
      <div className="md:block w-full h-full md:w-8/12">
        <ModelProfilesTable pageSize={20}/>
        {/* <MainConfigForm/> */}
    </div>
    </>
)};

export default Config;