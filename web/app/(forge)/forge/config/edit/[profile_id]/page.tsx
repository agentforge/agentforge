'use client';
import React from 'react';
import ModelConfigForm from '@/components/forge/config/form';

import { GENERATION_FIELDS } from '@/components/forge/config/genconfig';
import { MODEL_FIELDS } from '@/components/forge/config/modelconfig'
import { PROMPT_FIELDS } from '@/components/forge/config/promptconfig'
import { AVATAR_FIELDS } from '@/components/forge/config/avatarconfig'

import { flattenObj } from '@/lib/utils';

type DataObject = {
  metadata?: any; // Define the type of the metadata property
  generation_config?: any;
  model_config?: any;
  prompt_config?: any;
  persona?: any;
};

interface ConfigProps {
  params: Record<string, any>;
}

const initForm = (data: DataObject) => {
  // If this is not a new model profile we don't need to source all key values 
  let generation_config = data.generation_config;
  let model_config = data.model_config;
  let prompt_config = data.prompt_config;
  let persona = data.persona;
  // Else grab the defaults
  const flattenedData = flattenObj(data);
    generation_config = Object.fromEntries(Object.entries(GENERATION_FIELDS).map(([key, { default: defaultValue }]) => [key, flattenedData[key] || defaultValue]))
    model_config = Object.fromEntries(Object.entries(MODEL_FIELDS).map(([key, { default: defaultValue }]) => [key, flattenedData[key] || defaultValue]))
    prompt_config = Object.fromEntries(Object.entries(PROMPT_FIELDS).map(([key, { default: defaultValue }]) => [key, flattenedData[key] || defaultValue]))
    persona = Object.fromEntries(Object.entries(AVATAR_FIELDS).map(([key, { default: defaultValue }]) => [key, flattenedData[key] || defaultValue]))
  let metadata = data.metadata || {}; // Assuming metadata is a key in the original data object
  if (!metadata['user_id']) { 
    metadata['user_id'] = 'test_user';
  }
  // Merge config1 and config2
  let mergedObject = {
    generation_config: generation_config,
    model_config: model_config,
    prompt_config: prompt_config,
    persona: persona,
    metadata: metadata,
  };
  return mergedObject
}

const Page: React.FC<ConfigProps> = ({ params }) => {
  const id = params.profile_id;
  const [form, setForm] = React.useState<Record<string, any>>({});

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(`/api/modelprofiles/${id}`);
        const json = await res.json();
        setForm(initForm(json));
      } catch (error) {
        console.error("Error fetching data: ", error);
      }
    };
    fetchData();
  }, [id]); // Run only on id change


  return (
    <>
      <div className="md:block w-full h-full md:w-8/12">
        <ModelConfigForm form={form} id={id} />
    </div>
    </>
  )
};

export default Page;