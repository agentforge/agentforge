'use client';
// ModelProfileConfigContext.tsx
import React, { createContext, useContext, useState } from 'react';

interface ModelProfileConfig {
  [key: string]: any;
}

interface ModelProfileConfigContextValue {
  modelProfileConfigs: ModelProfileConfig;
  setModelProfileConfig: (id: string, value: any) => void;
}

const ModelProfileConfigContext = createContext<ModelProfileConfigContextValue | undefined>(
  undefined
);

export const useModelProfileConfig = () => {
  const context = useContext(ModelProfileConfigContext);
  if (!context) {
    throw new Error('useModelProfileConfig must be used within a ModelProfileConfigProvider');
  }
  return context;
};

interface ModelProfileConfigProviderProps {
  children: React.ReactNode;
}

export const ModelProfileConfigProvider: React.FC<ModelProfileConfigProviderProps> = ({
  children,
}) => {
  const [modelProfileConfigs, setModelProfileConfigs] = useState<ModelProfileConfig>({});

  const setModelProfileConfig = (id: string, value: any) => {
    
    setModelProfileConfigs((prevConfigs) => {
      const updatedConfigs = { ...prevConfigs, [id]: value };
      return updatedConfigs;
    });
  };

  return (
    <ModelProfileConfigContext.Provider value={{ modelProfileConfigs, setModelProfileConfig }}>
      {children}
    </ModelProfileConfigContext.Provider>
  );
};
