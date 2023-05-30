'use client';
import React from 'react';
import ModelConfigForm from '@/components/forge/modelconfigform';

import { GENERATION_FIELDS } from '@/components/forge/genconfig';
import { MODEL_FIELDS } from '@/components/forge/modelconfig'

import { flattenObj } from '@/lib/utils';

interface ConfigProps {
  params: Record<string, any>;
}

const initForm = (data: {}) => {
  const flattenedData = flattenObj(data);

  let config1 = Object.fromEntries(Object.entries(GENERATION_FIELDS).map(([key, { default: defaultValue }]) => [key, flattenedData[key] || defaultValue]))
  let config2 = Object.fromEntries(Object.entries(MODEL_FIELDS).map(([key, { default: defaultValue }]) => [key, flattenedData[key] || defaultValue]))
  
  // Merge config1 and config2  
  let mergedObject = { ...config1, ...config2, ...data };
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