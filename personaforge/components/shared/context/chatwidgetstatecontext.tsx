// ChatWidgetStateContext.tsx
import React, { createContext, useContext, useState } from 'react';

interface ChatWidgetStateContextValue {
  messages: Message[];
  setMessages: (messages: Message[]) => void;
  textAreaValue: string;
  setTextAreaValue: (value: string) => void;
}

const ChatWidgetStateContext = createContext<ChatWidgetStateContextValue | undefined>(undefined);

export const useChatWidgetState = () => {
  const context = useContext(ChatWidgetStateContext);
  if (!context) {
    throw new Error('useChatWidgetState must be used within a ChatWidgetStateProvider');
  }
  return context;
};

interface ChatWidgetStateProviderProps {
  children: React.ReactNode;
}

export const ChatWidgetStateProvider: React.FC<ChatWidgetStateProviderProps> = ({ children }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [textAreaValue, setTextAreaValue] = useState('');

  return (
    <ChatWidgetStateContext.Provider value={{ messages, setMessages, textAreaValue, setTextAreaValue }}>
      {children}
    </ChatWidgetStateContext.Provider>
  );
};

interface Message {
  id: string;
  author: string;
  text: string;
  author_type: string;
}
