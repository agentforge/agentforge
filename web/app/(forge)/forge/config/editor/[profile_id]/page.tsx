'use client';
import React from 'react';
import MainConfigForm from '@/components/forge/mainconfig';

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
  let mergedObject = { ...config1, ...config2 };
  return mergedObject

}

const Page: React.FC<ConfigProps> = ({ params }) => {
  const id = params.id;
  const [data, setData] = React.useState<Record<string, any>>({});
  const [form, setForm] = React.useState({});

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(`/api/model-profiles/${id}`);
        const json = await res.json();
        setData(json);
      } catch (error) {
        console.error("Error fetching data: ", error);
      }
    };
    fetchData();
  }, [id]); // This will re-run the effect when the id changes

  const initData = initForm(data);
  setForm(initData);

  return (
    <>
      <div className="md:block w-full h-full md:w-8/12">
        <MainConfigForm form={form} id={id} />
    </div>
    </>
)};