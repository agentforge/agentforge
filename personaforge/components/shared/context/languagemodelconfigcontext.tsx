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
    console.log('Updating languageModelConfigs:', { id, value });
    
    setLanguageModelConfigs((prevConfigs) => {
      console.log('Previous languageModelConfigs:', prevConfigs);
      const updatedConfigs = { ...prevConfigs, [id]: value };
      console.log('Updated languageModelConfigs:', updatedConfigs);
      return updatedConfigs;
    });
  };

  return (
    <LanguageModelConfigContext.Provider value={{ languageModelConfigs, setLanguageModelConfig }}>
      {children}
    </LanguageModelConfigContext.Provider>
  );
};
