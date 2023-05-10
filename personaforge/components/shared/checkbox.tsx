// CheckboxElement.tsx
import React, { forwardRef } from 'react';
import * as Checkbox from '@radix-ui/react-checkbox';
import { CheckIcon } from '@radix-ui/react-icons';
import { useCheckboxState } from '@/components/shared/context/checkboxstatecontext';
import { useLanguageModelConfig } from '@/components/shared/context/languagemodelconfigcontext';

interface CheckboxElementProps {
  label: string;
  id: string;
  defaultVal: boolean;
}

const CheckboxElement = forwardRef<HTMLButtonElement, CheckboxElementProps>(({
  label,
  id,
  defaultVal,
}, ref) => {
  const { checkboxStates, setCheckboxState } = useCheckboxState();
  const checked = checkboxStates[id] || false;
  const { languageModelConfigs, setLanguageModelConfig } = useLanguageModelConfig();

  // Initialize the values in the LanguageModelConfig
  React.useEffect(() => {
    if (defaultVal) {
      setLanguageModelConfig(id, defaultVal);
    }
  }, []);

  const handleCheckboxChange = () => {
    setCheckboxState(id, !checked);
    setLanguageModelConfig(id, !checked);
  };

  return (
    <form>
      <div className="flex items-center">
        <Checkbox.Root
          className="shadow-blackA7 hover:bg-violet3 flex h-[25px] w-[25px] appearance-none items-center justify-center rounded-[4px] bg-white shadow-[0_2px_10px] outline-none focus:shadow-[0_0_0_2px_black]"
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
      </div>
    </form>
  );
});

// Add a display name to the component
CheckboxElement.displayName = 'CheckboxElement';

export default CheckboxElement;
