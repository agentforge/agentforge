'use client';
// TextareaElement.tsx
import React from 'react';
import * as Select from '@radix-ui/react-select';
import classnames from 'classnames';
import { CheckIcon, ChevronDownIcon, ChevronUpIcon } from '@radix-ui/react-icons';
import { useModelProfileConfig } from '@/components/shared/context/modelprofileconfig';
import * as Label from '@radix-ui/react-label';
import TooltipSimple from '@/components/shared/tooltip_simple';

interface TextareaElementProps {
  id: string;
  label: string;
  defaultVal: string;
}

const TextareaElement: React.FC<TextareaElementProps> = ({
  id,
  label,
  defaultVal,
}) => {
  const { modelProfileConfigs, setModelProfileConfig } = useModelProfileConfig();

  if (!modelProfileConfigs[id]) { 
    modelProfileConfigs[id] = defaultVal;
  }

  const setVal = (val: string) => {
      setModelProfileConfig(id, val);
  }

  // Initialize the values in the LanguageModelConfig
  React.useEffect(() => {
    if (defaultVal !== undefined) {
      setVal(defaultVal);
    }
  }, []);

  // Handle value change and convert to the necessary format
  const handleValueChange: React.ChangeEventHandler<HTMLTextAreaElement> = (event) => {
    setVal(event.currentTarget.value);
  };

  return (
    <>
    <Label.Root className="flex w-1/6 text-[15px] font-medium leading-[35px] text-white" htmlFor="firstName">
      {label}
    </Label.Root>
    <div className="flex w-4/6">
      <textarea
        id={ id }
        defaultValue={ modelProfileConfigs[id] }
        className="form-control bg-blackA5 shadow-blackA9 inline-flex w-full appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-white shadow-[0_0_0_1px] outline-none focus:shadow-[0_0_0_2px_black]"
        rows={4}
        style={{ width: '100%' }}
        onChange={handleValueChange}
      ></textarea>
      </div>
      </>
  );
};

interface TextareaItemProps {
  children: React.ReactNode;
  className?: string;
  value: string;
}

const TextareaItem = React.forwardRef<HTMLDivElement, TextareaItemProps>(
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

TextareaItem.displayName = 'TextareaItem';
TextareaElement.displayName = 'TextareaElement';

export default TextareaElement;
