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
import { createTheme, NextUIProvider } from "@nextui-org/react"

const darkTheme = createTheme({
  type: "dark", // it could be "light" or "dark"
  theme: {
    colors: {
      primary: '#4ADE7B',
      secondary: '#F9CB80',
      error: '#FCC5D8',
    },
  }
})

import Forge from './app';

const ForgeComponent = () => {
  return (
    <NextUIProvider theme={darkTheme}>
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
    </NextUIProvider>
  );
};
// ReactDOM.render(<ForgeComponent />, document.getElementById('main'));

export default ForgeComponent;

