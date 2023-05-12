'use client';
// ForgeComponent.tsx
// Expose Store Providers to the Child Components
import React from 'react';
import ReactDOM from 'react-dom';
import { CheckboxStateProvider } from '@/components/shared/context/checkboxstatecontext';
import { SelectStateProvider } from '@/components/shared/context/selectstatecontext';
import { SliderStateProvider } from '@/components/shared/context/sliderstatecontext';
import { LanguageModelConfigProvider } from '@/components/shared/context/languagemodelconfigcontext';
import { ChatWidgetStateProvider } from '@/components/shared/context/chatwidgetstatecontext';
import { AvatarProvider } from '@/components/shared/context/avatarcontextprovider';
import { VideoProvider } from '@/components/shared/context/videoprovider';
import { AudioProvider } from '@/components/shared/context/audioprovider';
import Forge from './app';

const ForgeComponent = () => {
  return (
    <VideoProvider>
    <AudioProvider>
    <ChatWidgetStateProvider>
    <LanguageModelConfigProvider>
    <SliderStateProvider>
    <SelectStateProvider>
    <CheckboxStateProvider>
    <AvatarProvider>
      <Forge />
    </AvatarProvider>
    </CheckboxStateProvider>
    </SelectStateProvider>
    </SliderStateProvider>
    </LanguageModelConfigProvider>
    </ChatWidgetStateProvider>
    </AudioProvider>
    </VideoProvider>
  );
};
// ReactDOM.render(<ForgeComponent />, document.getElementById('main'));

export default ForgeComponent;

