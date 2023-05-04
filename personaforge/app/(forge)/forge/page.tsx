'use client';
// ForgeComponent.tsx
// Expose Store Providers to the Child Components
import React from 'react';
import { CheckboxStateProvider } from '@/components/shared/context/checkboxcontext';
import { SelectStateProvider } from '@/components/shared/context/selectstatecontext';
import Forge from './app';

const ForgeComponent = () => {
  return (
    <SelectStateProvider>
      <CheckboxStateProvider>
        <Forge />
      </CheckboxStateProvider>
    </SelectStateProvider>
    
  );
};

export default ForgeComponent;
