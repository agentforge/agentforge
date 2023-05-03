'use client';
// ForgeComponent.tsx
// Expose Store Providers to the Child Components
import React from 'react';
import { CheckboxStateProvider } from '@/components/shared/context/checkboxcontext';
import Forge from './app';

const ForgeComponent = () => {
  return (
    <CheckboxStateProvider>
      <Forge />
    </CheckboxStateProvider>
  );
};

export default ForgeComponent;
