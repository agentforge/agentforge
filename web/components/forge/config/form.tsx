'use client';
import * as React from 'react';
import * as ScrollArea from '@radix-ui/react-scroll-area';
import * as ToggleGroup from '@radix-ui/react-toggle-group';
import { AvatarIcon, MixIcon, MixerHorizontalIcon, InputIcon } from '@radix-ui/react-icons';
import AvatarConfig from '@/components/forge/config/avatarconfig';
import ModelConfig from '@/components/forge/config/modelconfig';
import GenerationConfigForm from './genconfig';
import PromptConfig from './promptconfig';
import Button from '@/components/shared/button';
import { useModelProfileConfig } from '@/components/shared/context/modelprofileconfig';

export interface ModelConfigFormProps {
  form: { [key: string]: { [key: string]: string | number | boolean | undefined } };
  id: string | undefined;
}
  
const ModelConfigForm: React.FC<ModelConfigFormProps> = ({ form, id }) =>  {
  const [currentTab, setCurrentTab] = React.useState<string>('avatar'); //defaults to avatar tab
  const { modelProfileConfigs, setModelProfileConfig} = useModelProfileConfig();
  const config_types = ['avatar_config', 'model_config', 'generation_config', 'prompt_config', 'metadata'];
  const avatar_config = form['avatar_config'] ?? {};
  const model_config = form['model_config'] ?? {};
  const generation_config = form['generation_config'] ?? {};
  const prompt_config = form['prompt_config'] ?? {};

  const handleRender = (value: string) => {
    // Set current state of the tab to `value`
    setCurrentTab(value);
  };

  const processForm = (form: { [key: string]: { [key: string]: string | number | boolean | undefined } }) => { 
    // Grab the data from the modelprofile config context and populate changes
    // into the form -- iterate through `config_types` and for each key check
    // the subsequent object in `form` and replace the values with the same key with the updated
    // version in the modelprofile context modelProfileConfigs
    // Iterate through `config_types` and replace values in the `form`
    const updatedForm = { ...form };
    console.log(modelProfileConfigs);
    config_types.forEach((config) => {
      if (updatedForm[config] !== undefined) {
        Object.keys(updatedForm[config]).forEach((key) => {
          if (modelProfileConfigs[key] !== undefined && modelProfileConfigs[key] !== null) {
            updatedForm[config][key] = modelProfileConfigs[key];
          }
        });
      }
    })

    // Set updated_dt or other metadata
    console.log(updatedForm);
    updatedForm['metadata']['updated_dt'] = new Date().toISOString(); 
    return updatedForm;
  }

  const handleSubmit = () => {
    // Handle the form submission...
    console.log("handleSubmit");
    console.log(form);
    form = processForm(form);
    console.log("After...")
    console.log(form);
    if (!form) {
      console.log("FORM IS NULL!!?")
      return
    } else { 
      console.log("FORM!! EXIST")
      console.log(form);
    }id
    const postProfiles = async () => {
      try {
        console.log("ID");
        console.log(id);
        const user_id = "test_user";
        console.log(`/api/modelprofiles/${id}`);
        const res = await fetch(`/api/modelprofiles/${id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            // 'API-Key': process.env.DATA_API_KEY,
          },
          body: JSON.stringify(form), // stringify the form data
        });
        const data = await res.json();
        console.log(data);
      } catch (error) {
        console.error(error);
      }
    };
    postProfiles();
  };
  
  const toggleGroupItemClasses =
  'hover:bg-black color-mauve11 data-[state=on]:bg-slate-600 data-[state=on]:text-white flex p-3 h-[35px] w-max items-center justify-center bg-slate-800 text-base leading-4 first:rounded-l last:rounded-r focus:z-10 focus:shadow-[0_0_0_2px] focus:shadow-black focus:outline-none';
  
  return (
    <>
    <div className='flex w-full items-center justify-center m-3'>
      <ToggleGroup.Root
          className="inline-flex bg-black rounded shadow-[0_2px_10px] shadow-blackA7 space-x-px"
          type="single"
          defaultValue="avatar"
          aria-label="Select Config Menu"
          onValueChange={handleRender}
      >
      <ToggleGroup.Item className={toggleGroupItemClasses} value="avatar" aria-label="Left aligned">
        <AvatarIcon /> <span className='ml-3'>Avatar</span>
        </ToggleGroup.Item>
        <ToggleGroup.Item className={toggleGroupItemClasses} value="model" aria-label="Left aligned">
        <MixIcon /> <span className='ml-3'>Model Config</span>
      </ToggleGroup.Item>
      <ToggleGroup.Item className={toggleGroupItemClasses} value="generation" aria-label="Center aligned">
        <MixerHorizontalIcon /> <span className='ml-3'>Generation Config</span>
      </ToggleGroup.Item>
      <ToggleGroup.Item className={toggleGroupItemClasses} value="prompt" aria-label="Right aligned">
        <InputIcon /> <span className='ml-3'>Prompt Tinkering</span>
      </ToggleGroup.Item>
      </ToggleGroup.Root>
      <div className='float-right w-2/12'>
        <Button type="submit" onClick={ handleSubmit } extraClasses="float-right">Save</Button>
      </div>
    </div>
    <ScrollArea.Root className="w-full h-screen rounded overflow-hidden">
    <ScrollArea.Viewport className="w-full h-full rounded">
    <form className="pb-28 text-white">
      {currentTab == "avatar" ? ( <AvatarConfig form={ avatar_config } />) : (<></>) }
      {currentTab == "model" ? (<ModelConfig form={ model_config } />) : (<></>) }
      {currentTab == "generation" ? (<GenerationConfigForm form={ generation_config } />) : (<></>) }
      {currentTab == "prompt" ? (<PromptConfig form={ prompt_config } />) : (<></>) }
    </form>
    </ScrollArea.Viewport>
    <ScrollArea.Scrollbar
      className="flex select-none touch-none p-0.5 bg-blackA6 transition-colors duration-[160ms] ease-out hover:bg-blackA8 data-[orientation=vertical]:w-2.5 data-[orientation=horizontal]:flex-col data-[orientation=horizontal]:h-2.5"
      orientation="vertical"
    >
      <ScrollArea.Thumb className="flex-1 bg-mauve10 rounded-[10px] relative before:content-[''] before:absolute before:top-1/2 before:left-1/2 before:-translate-x-1/2 before:-translate-y-1/2 before:w-full before:h-full before:min-w-[44px] before:min-h-[44px]" />
    </ScrollArea.Scrollbar>
    <ScrollArea.Scrollbar
      className="flex select-none touch-none p-0.5 bg-blackA6 transition-colors duration-[160ms] ease-out hover:bg-blackA8 data-[orientation=vertical]:w-2.5 data-[orientation=horizontal]:flex-col data-[orientation=horizontal]:h-2.5"
      orientation="horizontal"
    >
      <ScrollArea.Thumb className="flex-1 bg-mauve10 rounded-[10px] relative before:content-[''] before:absolute before:top-1/2 before:left-1/2 before:-translate-x-1/2 before:-translate-y-1/2 before:w-full before:h-full before:min-w-[44px] before:min-h-[44px]" />
    </ScrollArea.Scrollbar>
    <ScrollArea.Corner className="bg-blackA8" />
    </ScrollArea.Root>
    </>
  );
}

export default ModelConfigForm;