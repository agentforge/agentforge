'use client';
import React from 'react';
import ModelProfilesTable from '@/components/forge/config/modelprofiles';

interface ConfigProps {}

const Config: React.FC<ConfigProps> = () => {

  return (
    <>
      <div className="md:block w-full h-full md:w-8/12">
        <ModelProfilesTable pageSize={20}/>
    </div>
    </>
)};

export default Config;