// CheckboxElement.tsx
import React, { forwardRef } from 'react';
import * as Checkbox from '@radix-ui/react-checkbox';
import { CheckIcon } from '@radix-ui/react-icons';
import { useModelProfileConfig } from '@/components/shared/context/modelprofileconfig';
import TooltipSimple from '@/components/shared/tooltip_simple';

interface CheckboxElementProps {
  label: string;
  id: string;
  defaultVal: boolean | undefined;
  tooltipText: string;
}

const CheckboxElement = forwardRef<HTMLButtonElement, CheckboxElementProps>(({
  label,
  id,
  defaultVal,
  tooltipText,
}, ref) => {
  const { modelProfileConfigs, setModelProfileConfig } = useModelProfileConfig();
  const checked = modelProfileConfigs[id] || false;

  // Initialize the values in the LanguageModelConfig
  React.useEffect(() => {
    if (defaultVal) {
      setModelProfileConfig(id, defaultVal);
    }
  }, []);

  const handleCheckboxChange = () => {
    setModelProfileConfig(id, !checked);
  };

  return (
    <div className="ml-6 mt-12 flex items-center">
      <Checkbox.Root
        className="shadow-CheckboxblackA7 hover:bg-violet3 flex h-[25px] w-[25px] appearance-none items-center justify-center rounded-[4px] bg-white shadow-[0_2px_10px] outline-none focus:shadow-[0_0_0_2px_black]"
        checked={checked}
        onCheckedChange={handleCheckboxChange}
        id={id}
        ref={ref}
      >
        <Checkbox.Indicator className="text-violet11">
          <CheckIcon />
        </Checkbox.Indicator>
      </Checkbox.Root>
      <label className="pl-[15px] text-[15px] leading-none text-white" htmlFor={id}>
        {label}
      </label>
      {tooltipText !== undefined ? (
        <TooltipSimple text={tooltipText} />
      ) : (
        <></>
      )}
    </div>
  );modelProfileConfigs
});

// Add a display name to the component
CheckboxElement.displayName = 'CheckboxElement';

export default CheckboxElement;
