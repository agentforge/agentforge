'use client';
import React from 'react';
import ModelConfigForm from '@/components/forge/config/form';

import { GENERATION_FIELDS } from '@/components/forge/config/genconfig';
import { MODEL_FIELDS } from '@/components/forge/config/modelconfig'
import { PROMPT_FIELDS } from '@/components/forge/config/promptconfig'
import { AVATAR_FIELDS } from '@/components/forge/config/avatarconfig'

import { flattenObj } from '@/lib/utils';

interface ConfigProps {
  params: Record<string, any>;
}

const initForm = (data: {}) => {
  const flattenedData = flattenObj(data);

  let generation_config = Object.fromEntries(Object.entries(GENERATION_FIELDS).map(([key, { default: defaultValue }]) => [key, flattenedData[key] || defaultValue]))
  let model_config = Object.fromEntries(Object.entries(MODEL_FIELDS).map(([key, { default: defaultValue }]) => [key, flattenedData[key] || defaultValue]))
  let prompt_config = Object.fromEntries(Object.entries(PROMPT_FIELDS).map(([key, { default: defaultValue }]) => [key, flattenedData[key] || defaultValue]))
  let avatar_config = Object.fromEntries(Object.entries(AVATAR_FIELDS).map(([key, { default: defaultValue }]) => [key, flattenedData[key] || defaultValue]))

  // Merge config1 and config2  
  let mergedObject = {
    generation_config: generation_config,
    model_config: model_config,
    prompt_config: prompt_config,
    avatar_config: avatar_config,
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
        console.log("json", json);
        setForm(initForm(json.data[0]));
        console.log(form);
      } catch (error) {
        console.error("Error fetching data: ", error);
      }id
    };
    fetchData();
  }, []); // Run once


  return (
    <>
      <div className="md:block w-full h-full md:w-8/12">
        <ModelConfigForm form={form} id={id} />
    </div>
    </>
  )
};

export default Page;