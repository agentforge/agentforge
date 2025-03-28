import React from 'react';
import * as Tooltip from '@radix-ui/react-tooltip';
import { PlusIcon, QuestionMarkIcon } from '@radix-ui/react-icons';

interface TooltipSimpleProps {
  text: string | undefined;
}

const TooltipSimple: React.FC<TooltipSimpleProps> = ({ text }) => {
  var val = '';
  if (text !== undefined) { 
    val = text;
  } 
  return (
    <Tooltip.Provider>
      <Tooltip.Root>
        <Tooltip.Trigger asChild>
          <button className="text-violet11 shadow-blackA7 hover:bg-black inline-flex h-[35px] w-[35px] items-center justify-center rounded-full bg-black shadow-[0_2px_10px] outline-none focus:shadow-[0_0_0_2px] focus:shadow-black">
            <QuestionMarkIcon />
          </button>
        </Tooltip.Trigger>
        <Tooltip.Portal>
          <Tooltip.Content
            className="max-w-md z-[99999] data-[state=delayed-open]:data-[side=top]:animate-slideDownAndFade data-[state=delayed-open]:data-[side=right]:animate-slideLeftAndFade data-[state=delayed-open]:data-[side=left]:animate-slideRightAndFade data-[state=delayed-open]:data-[side=bottom]:animate-slideUpAndFade text-violet11 select-none rounded-[4px] bg-white px-[15px] py-[10px] text-[15px] leading-none shadow-[hsl(206_22%_7%_/_35%)_0px_10px_38px_-10px,_hsl(206_22%_7%_/_20%)_0px_10px_20px_-15px] will-change-[transform,opacity]"
            sideOffset={5}
            side='top'
          >
            {val}
            <Tooltip.Arrow className="fill-white" />
          </Tooltip.Content>
        </Tooltip.Portal>
      </Tooltip.Root>
    </Tooltip.Provider>
  );
};

export default TooltipSimple;
