'use client';
import React from 'react';
import ModelProfilesTable from '@/components/forge/config/modelprofiles';
import ModelConfigForm from '@/components/forge/config/form';

interface ConfigProps {}

const Config: React.FC<ConfigProps> = () => {

  return (
    <>
      <div className="md:block w-full h-full md:w-8/12">
        <ModelProfilesTable pageSize={20}/>
        <ModelConfigForm form={{}} id={undefined} />
    </div>
    </>
)};

export default Config;