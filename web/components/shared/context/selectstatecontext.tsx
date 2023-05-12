// SelectStateContext.tsx
import React, { createContext, useContext, useState } from 'react';

interface SelectStateContextValue {
  selectedValues: { [key: string]: string | null };
  setSelectedValue: (id: string, value: string | null) => void;
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
  const [selectedValues, setSelectedValues] = useState<{ [key: string]: string | null }>({});

  const setSelectedValue = (id: string, value: string | null) => {
    setSelectedValues((prevSelectedValues) => ({
      ...prevSelectedValues,
      [id]: value,
    }));
  };

  return (
    <SelectStateContext.Provider value={{ selectedValues, setSelectedValue }}>
      {children}
    </SelectStateContext.Provider>
  );
};
