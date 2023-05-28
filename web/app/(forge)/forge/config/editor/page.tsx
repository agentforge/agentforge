'use client';
import React from 'react';
import MainConfigForm from '@/components/forge/mainconfig';

interface ConfigProps {}

const Config: React.FC<ConfigProps> = () => {

  return (
    <>
      <div className="md:block w-full h-full md:w-8/12">
        <MainConfigForm/>
    </div>
    </>
)};

export default Config;