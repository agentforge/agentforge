'use client';
import * as React from 'react';
import Button from '@/components/shared/button';
import ConfigForm from '@/components/shared/form/configform'

export interface ConfigProps {
  form: {[key: string]: string | number | boolean | undefined};
}

export const PROMPT_FIELDS = {
  prompt_template: { type: 'textarea', default: 'Prompt goes here...' },
}

const handleChangePrompt = () => {
  // Handle the form submission for default prompts
  // TODO: Grab some common prompts
};

export const PromptConfig: React.FC<ConfigProps> = ({ form }) =>  {
  return (
    <>
    <h1>Prompt Tinkering</h1>
    <p className="text-gray-600">Configure the instruction prompt that is hidden from the user. Usually specific to model based on training or fine-tuning.</p>
    <div className="flex flex-row mt-9">
      <div className="flex w-full">
        <ConfigForm fields={PROMPT_FIELDS} form={form} />
      </div>
      <div className="flex w-1/2 ml-4">
          <div className="flex w-full flex-col space-y-4">
            <Button type="button" onClick={ handleChangePrompt } extraClasses="w-full">instruct</Button>
            <Button type="button" onClick={ handleChangePrompt } extraClasses="w-full">instruct_w_memory</Button>
            <Button type="button" onClick={ handleChangePrompt } extraClasses="w-full">mpt</Button>
        </div>  
      </div>
    </div>
    </>
  )
}

export default PromptConfig;
