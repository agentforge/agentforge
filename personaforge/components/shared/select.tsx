// SelectElement.tsx
import React from 'react';
import * as Select from '@radix-ui/react-select';
import classnames from 'classnames';
import { CheckIcon, ChevronDownIcon, ChevronUpIcon } from '@radix-ui/react-icons';
import { useSelectState } from '@/components/shared/context/selectstatecontext';
import { useLanguageModelConfig } from '@/components/shared/context/languagemodelconfigcontext';

interface SelectElementProps {
  options: string[];
  id: string;
  label: string;
  defaultVal: string;
  storeInConfig?: boolean; // Add this prop to conditionally store in LanguageModelConfig
}

const SelectElement: React.FC<SelectElementProps> = ({
  options,
  id,
  label,
  defaultVal,
  storeInConfig = false, // Default value is false
}) => {
  const { selectedValues, setSelectedValue } = useSelectState();
  const { languageModelConfigs, setLanguageModelConfig } = useLanguageModelConfig();

  const handleValueChange = (id: string, value: string) => {
    setSelectedValue(id, value);
    if (storeInConfig) {
      setLanguageModelConfig(id, value);
    }
  };

  return (
    <Select.Root onValueChange={(value) => handleValueChange(id, value)}
    value={selectedValues[id] || defaultVal}
  >
    <Select.Trigger
      className="inline-flex items-center justify-center rounded px-[15px] text-[13px] leading-none h-[35px] gap-[5px] bg-white text-violet11 shadow-[0_2px_10px] shadow-black/10 hover:bg-mauve3 focus:shadow-[0_0_0_2px] focus:shadow-black data-[placeholder]:text-violet9 outline-none"
      aria-label="Options"
      id={id}
    >
      <Select.Value placeholder={defaultVal} />
      <Select.Icon className="text-violet11">
        <ChevronDownIcon />
      </Select.Icon>
    </Select.Trigger>
    <Select.Portal>
      <Select.Content className="z-1000 overflow-hidden bg-white rounded-md shadow-[0px_10px_38px_-10px_rgba(22,_23,_24,_0.35),0px_10px_20px_-15px_rgba(22,_23,_24,_0.2)]">
        <Select.ScrollUpButton className="flex items-center justify-center h-[25px] bg-white text-violet11 cursor-default">
          <ChevronUpIcon />
        </Select.ScrollUpButton>
        <Select.Viewport className="p-[5px]">
          <Select.Group>
            <Select.Label className="px-[25px] text-xs leading-[25px] text-mauve11">
              { label }
            </Select.Label>
            {options.map((option) => (
              <SelectItem key={option} value={option}>
                {option}
              </SelectItem>
            ))}
          </Select.Group>
        </Select.Viewport>
        <Select.ScrollDownButton className="flex items-center justify-center h-[25px] bg-white text-violet11 cursor-default">
          <ChevronDownIcon />
        </Select.ScrollDownButton>
      </Select.Content>
    </Select.Portal>
  </Select.Root>
  );
};

interface SelectItemProps {
  children: React.ReactNode;
  className?: string;
  value: string;
}

const SelectItem = React.forwardRef<HTMLDivElement, SelectItemProps>(
  ({ children, className, ...props }, forwardedRef) => {
    return (
      <Select.Item
        className={classnames(
          'text-[13px] leading-none text-violet11 rounded-[3px] flex items-center h-[25px] pr-[35px] pl-[25px] relative select-none data-[disabled]:text-mauve8 data-[disabled]:pointer-events-none data-[highlighted]:outline-none data-[highlighted]:bg-violet9 data-[highlighted]:text-violet1',
          className
        )}
        {...props}
        ref={forwardedRef}
      >
        <Select.ItemText>{children}</Select.ItemText>
        <Select.ItemIndicator className="absolute left-0 w-[25px] inline-flex items-center justify-center">
          <CheckIcon />
        </Select.ItemIndicator>
      </Select.Item>
    );
  }
);

SelectItem.displayName = 'SelectItem';
SelectElement.displayName = 'SelectElement';

export default SelectElement;
