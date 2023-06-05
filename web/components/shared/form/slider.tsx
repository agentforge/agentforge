// SliderElement.tsx
import React, { forwardRef } from 'react';
import * as Slider from '@radix-ui/react-slider';
import { useModelProfileConfig } from '@/components/shared/context/modelprofileconfig';
import { Text } from '@nextui-org/react';

interface SliderElementProps {
  defaultValue?: number;
  max?: number;
  step?: number;
  ariaLabel?: string;
  width?: string;
  sliderId: string;
}

const SliderElement = forwardRef<HTMLDivElement, SliderElementProps>(
  ({ defaultValue = 50, max = 100, step = 1, ariaLabel = 'Slider', width = '200px', sliderId }, ref) => {
    const { modelProfileConfigs, setModelProfileConfig } = useModelProfileConfig();

  // Initialize the values in the LanguageModelConfig
  React.useEffect(() => {
    if (defaultValue) {
      setModelProfileConfig(sliderId, defaultValue);
    }
  }, []);

    const handleValueChange = (value: number[]) => {
      console.log("setting slider value")
      setModelProfileConfig(sliderId, value[0]);
    };

    return (
      <>
      <div className="flex flex-row w-full mt-3"> 
        <Text h6>{ariaLabel}</Text>
        <div id="max_new_tokens_value" className="flex w-2/12">
          { modelProfileConfigs[sliderId] || defaultValue }
        </div>
      </div>
      <div className="flex flex-row w-full"> 

        <div className="float-left">
            <Slider.Root
              ref={ref}
              className="relative flex items-center select-none touch-none"
              style={{ width }}
              defaultValue={[defaultValue]}
              max={max}
              step={step}
              aria-label={ariaLabel}
              onValueChange={handleValueChange}
              value={[modelProfileConfigs[sliderId] ?? defaultValue]}
            >
              <Slider.Track className="bg-blackA10 relative grow rounded-full h-[3px]">
                <Slider.Range className="absolute bg-white rounded-full h-full" />
              </Slider.Track>
              <Slider.Thumb className="block w-5 h-5 bg-white shadow-[0_2px_10px] shadow-blackA7 rounded-[10px] hover:bg-violet3 focus:outline-none focus:shadow-[0_0_0_5px] focus:shadow-blackA8" />
            </Slider.Root>
          </div>
        </div>
      </>
    );
  }
);

// Add a display name to the component
SliderElement.displayName = 'SliderElement';

export default SliderElement;
