// InputElement.tsx
import React from 'react';
import * as Select from '@radix-ui/react-select';
import classnames from 'classnames';
import { CheckIcon, ChevronDownIcon, ChevronUpIcon } from '@radix-ui/react-icons';
import { useModelProfileConfig } from '@/components/shared/context/modelprofileconfig';
import * as Label from '@radix-ui/react-label';
import TooltipSimple from '@/components/shared/tooltip_simple';

interface InputElementProps {
  id: string;
  label: string;
  type: string;
  defaultVal: string;
  tooltipText: string;
}

const InputElement: React.FC<InputElementProps> = ({
  id,
  label,
  type,
  defaultVal,
  tooltipText,
}) => {
  const { modelProfileConfigs, setModelProfileConfig } = useModelProfileConfig();

  const setVal = (val: string) => {
    if (type === 'int') {
      setModelProfileConfig(id, parseInt(val));
    } else if (type == 'float') {
      setModelProfileConfig(id, parseFloat(val));
    } else { 
      setModelProfileConfig(id, val);
    }
  }

  // Initialize the values in the LanguageModelConfig
  React.useEffect(() => {
    if (defaultVal) {
      setVal(defaultVal);
    }
  }, []);

  // Handle value change and convert to the necessary format
  const handleValueChange: React.ChangeEventHandler<HTMLInputElement> = (event) => {
    setVal(event.currentTarget.value);
  };

  // Set input type for the form
  var inputType = 'text';
  if (type === 'int' || type === 'float') { 
    inputType = 'number';
  }
  return (
    <div className="flex flex-wrap items-center gap-[15px] px-5" key={ id }>
      <Label.Root className="text-[15px] f1ont-medium leading-[35px] text-white" htmlFor={id}>
        {label}
        {tooltipText !== undefined && tooltipText !== '' ? (
          <span className='ml-3'><TooltipSimple text={tooltipText} /></span>
        ) : (
          <></>
        )}
      </Label.Root>
      <input
          className="bg-blackA5 shadow-blackA9 inline-flex h-[35px] w-full appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-white shadow-[0_0_0_1px] outline-none focus:shadow-[0_0_0_2px_black]"
          type={inputType}
          id={id}
          value={modelProfileConfigs[id]}
          onChange={(event) => handleValueChange(event)}
      />
  </div>
  );
};

interface InputItemProps {
  children: React.ReactNode;
  className?: string;
  value: string;
}

const InputItem = React.forwardRef<HTMLDivElement, InputItemProps>(
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

InputItem.displayName = 'InputItem';
InputElement.displayName = 'InputElement';

export default InputElement;
