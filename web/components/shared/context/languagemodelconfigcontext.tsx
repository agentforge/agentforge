// LanguageModelConfigContext.tsx
import React, { createContext, useContext, useState } from 'react';

interface LanguageModelConfig {
  [key: string]: any;
}

interface LanguageModelConfigContextValue {
  languageModelConfigs: LanguageModelConfig;
  setLanguageModelConfig: (id: string, value: any) => void;
}

const LanguageModelConfigContext = createContext<LanguageModelConfigContextValue | undefined>(
  undefined
);

export const useLanguageModelConfig = () => {
  const context = useContext(LanguageModelConfigContext);
  if (!context) {
    throw new Error('useLanguageModelConfig must be used within a LanguageModelConfigProvider');
  }
  return context;
};

interface LanguageModelConfigProviderProps {
  children: React.ReactNode;
}

export const LanguageModelConfigProvider: React.FC<LanguageModelConfigProviderProps> = ({
  children,
}) => {
  const [languageModelConfigs, setLanguageModelConfigs] = useState<LanguageModelConfig>({});

  const setLanguageModelConfig = (id: string, value: any) => {
    
    setLanguageModelConfigs((prevConfigs) => {
      const updatedConfigs = { ...prevConfigs, [id]: value };
      return updatedConfigs;
    });
  };

  return (
    <LanguageModelConfigContext.Provider value={{ languageModelConfigs, setLanguageModelConfig }}>
      {children}
    </LanguageModelConfigContext.Provider>
  );
};
