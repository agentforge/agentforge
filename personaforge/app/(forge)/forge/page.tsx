'use client';
// ForgeComponent.tsx
// Expose Store Providers to the Child Components
import React from 'react';
import { CheckboxStateProvider } from '@/components/shared/context/checkboxstatecontext';
import { SelectStateProvider } from '@/components/shared/context/selectstatecontext';
import { SliderStateProvider } from '@/components/shared/context/sliderstatecontext';
import Forge from './app';

const ForgeComponent = () => {
  return (
    <SliderStateProvider>
      <SelectStateProvider>
        <CheckboxStateProvider>
          <Forge />
        </CheckboxStateProvider>
      </SelectStateProvider>
    </SliderStateProvider>
    
  );
};

export default ForgeComponent;
