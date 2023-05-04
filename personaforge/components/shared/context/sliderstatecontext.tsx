// SliderStateContext.tsx
import React, { createContext, useContext, useState } from 'react';

interface SliderStateContextValue {
  sliderValues: Record<string, number>;
  setSliderValue: (sliderId: string, value: number) => Promise<void>;
}

const SliderStateContext = createContext<SliderStateContextValue | undefined>(undefined);

export const useSliderState = () => {
  const context = useContext(SliderStateContext);
  if (!context) {
    throw new Error('useSliderState must be used within a SliderStateProvider');
  }
  return context;
};

interface SliderStateProviderProps {
  children: React.ReactNode;
}

export const SliderStateProvider: React.FC<SliderStateProviderProps> = ({ children }) => {
  const [sliderValues, setSliderValues] = useState<Record<string, number>>({});

  const setSliderValue = async (sliderId: string, value: number) => {
    await new Promise((resolve) => setTimeout(resolve, 0));
    setSliderValues((prevSliderValues) => ({ ...prevSliderValues, [sliderId]: value }));
  };

  return (
    <SliderStateContext.Provider value={{ sliderValues, setSliderValue }}>
      {children}
    </SliderStateContext.Provider>
  );
};
