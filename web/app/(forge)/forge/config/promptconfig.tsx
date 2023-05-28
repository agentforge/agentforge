'use client';
import * as React from 'react';
import Button from '@/components/shared/button';

export interface ConfigProps {
  form: {[key: string]: string | number | boolean | undefined};
}

const handleChangePrompt = () => {
  // Handle the form su bmission...
  console.log("handleChangePrompt");
};

export const PromptConfig: React.FC<ConfigProps> = ({ form }) =>  {
  return (
    <>
    <h1>Prompt Tinkering</h1>
    <p className="text-gray-600">Configure the instruction prompt that is hidden from the user. Usually specific to model based on training or fine-tuning.</p>
    <div className="flex flex-row mt-9">
      <div className="flex w-1/2">
          <textarea
          id="user-input"
          defaultValue="Prompt goes here..."
          className="form-control"
          rows={4}
          style={{ width: '100%' }}
        ></textarea>
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
