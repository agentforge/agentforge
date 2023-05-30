'use client';
import { Analytics } from "@vercel/analytics/react";
import cx from "classnames";
import { sfPro, inter } from "../../fonts";
import "../../styles/globals.css";
import "../../styles/style.scss";
import Sidebar from "./sidebar";
import { CheckboxStateProvider } from '@/components/shared/context/checkboxstatecontext';
import { SelectStateProvider } from '@/components/shared/context/selectstatecontext';
import { SliderStateProvider } from '@/components/shared/context/sliderstatecontext';
import { LanguageModelConfigProvider } from '@/components/shared/context/languagemodelconfigcontext';
import { ChatWidgetStateProvider } from '@/components/shared/context/chatwidgetstatecontext';
import { AvatarProvider } from '@/components/shared/context/avatarcontextprovider';
import { VideoProvider } from '@/components/shared/context/videoprovider';
import { AudioProvider } from '@/components/shared/context/audioprovider';

export default function ForgeLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={cx(sfPro.variable, inter.variable)}>
        <VideoProvider>
        <AudioProvider>
        <ChatWidgetStateProvider>
        <LanguageModelConfigProvider>
        <SliderStateProvider>
        <SelectStateProvider>
        <CheckboxStateProvider>
        <AvatarProvider>
        <div className="fixed h-screen w-full bg-gradient-to-br from-black via-black to-black" />
        <main className="flex min-h-screen w-full flex-col py-32">
          <div className="flex fixed top-0 w-full z-30 transition-all">
            <div className="md:block h-full md:w-2/12">
              <Sidebar />
            </div>
            {children}
          </div>
        </main >
        </AvatarProvider>
        </CheckboxStateProvider>
        </SelectStateProvider>
        </SliderStateProvider>
        </LanguageModelConfigProvider>
        </ChatWidgetStateProvider>
        </AudioProvider>
        </VideoProvider>
        <Analytics />
      </body>
    </html>
  )
}
