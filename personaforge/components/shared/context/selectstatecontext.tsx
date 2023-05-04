// SelectStateContext.tsx
import React, { createContext, useContext, useState } from 'react';

interface SelectStateContextValue {
  selectedValue: string | null;
  setSelectedValue: (value: string | null) => void;
}

const SelectStateContext = createContext<SelectStateContextValue | undefined>(undefined);

export const useSelectState = () => {
  const context = useContext(SelectStateContext);
  if (!context) {
    throw new Error('useSelectState must be used within a SelectStateProvider');
  }
  return context;
};

interface SelectStateProviderProps {
  children: React.ReactNode;
}

export const SelectStateProvider: React.FC<SelectStateProviderProps> = ({ children }) => {
  const [selectedValue, setSelectedValue] = useState<string | null>(null);

  return (
    <SelectStateContext.Provider value={{ selectedValue, setSelectedValue }}>
      {children}
    </SelectStateContext.Provider>
  );
};
