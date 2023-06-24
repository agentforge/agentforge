'use client';
import * as React from 'react';
import CheckboxElement from '@/components/shared/form/checkbox';
import SelectElement from '@/components/shared/form/select';
import * as Label from '@radix-ui/react-label';
import ConfigForm from '@/components/shared/form/configform';

//TODO GET FROM API
const avatars = ['caretaker', 'default', 'makhno', 'fdr', 'sankara'];

export const AVATAR_FIELDS = {
  name: { type: 'text', default: '', label: 'Avatar Name' },
  display_name: { type: 'text', default: '', label: 'ModelProfile Name' },
  biography: { type: 'textarea', default: '', label: 'Biography' },
  speaker_idx: { type: 'int', default: '', label: 'coqAI Speaker IDX' },
}

export interface AvatarConfigProps {
  form: {[key: string]: string | number | boolean | undefined};
}

export const AvatarConfig: React.FC<AvatarConfigProps> = ({ form }) =>  {
  return (
      <>
      <div className="flex w-full">
      <div className="w-3/4">
        <h1>Avatar Config</h1>
        <p className="text-gray-600">Configure the instruction prompt that is hidden from the user. Usually specific to model based on training or fine-tuning.</p>
      </div>
      </div>
      <div className="flex flex-row mt-9">  
        <ConfigForm fields={AVATAR_FIELDS} form={form} />
      </div>
    </>
  )
}

export default AvatarConfig;