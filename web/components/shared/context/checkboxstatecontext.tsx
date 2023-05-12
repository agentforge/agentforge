// CheckboxStateContext.tsx
import React, { createContext, useContext, useState } from 'react';

interface CheckboxState {
  [key: string]: boolean;
}

interface CheckboxStateContextValue {
  checkboxStates: CheckboxState;
  setCheckboxState: (id: string, state: boolean) => void;
}

const CheckboxStateContext = createContext<CheckboxStateContextValue | undefined>(undefined);

export const useCheckboxState = () => {
  const context = useContext(CheckboxStateContext);
  if (!context) {
    throw new Error('useCheckboxState must be used within a CheckboxStateProvider');
  }
  return context;
};

interface CheckboxStateProviderProps {
  children: React.ReactNode;
}

export const CheckboxStateProvider: React.FunctionComponent<CheckboxStateProviderProps> = ({ children }) => {
  const [checkboxStates, setCheckboxStates] = useState<CheckboxState>({});

  const setCheckboxState = (id: string, state: boolean) => {
    setCheckboxStates((prevStates) => ({ ...prevStates, [id]: state }));
  };

  return (
    <CheckboxStateContext.Provider value={{ checkboxStates, setCheckboxState }}>
      {children}
    </CheckboxStateContext.Provider>
  );
};
