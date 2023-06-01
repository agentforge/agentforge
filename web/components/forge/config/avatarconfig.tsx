'use client';
import * as React from 'react';
import CheckboxElement from '@/components/shared/form/checkbox';
import SelectElement from '@/components/shared/form/select';
import * as Label from '@radix-ui/react-label';
import ConfigForm from '@/components/shared/form/configform';

//TODO GET FROM API
const avatars = ['caretaker', 'default', 'makhno', 'fdr', 'sankara'];

export const AVATAR_FIELDS = {
  speech: { type: 'boolean', default: false, label: 'Speech' },
  video: { type: 'boolean', default: false, label: 'Video' },
  streaming: { type: 'boolean', default: false, label: 'Streaming' },
  spacer1: {type: 'spacer', default: '', label: ''}, // for enforcing spacing between above and below content
  name: { type: 'text', default: '', label: 'Name' },
  biography: { type: 'textarea', default: '', label: 'Biography/Context' },
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
      <div className='flex flex-wrap items-center gap-[15px] px-5 w-1/4'>
          <Label.Root className="text-[15px] font-medium leading-[35px] text-white" htmlFor="firstName">
            Avatar Presets      
          </Label.Root>
          <SelectElement options={avatars} id="avatar" label="Avatar" defaultVal="caretaker" />
        </div>
    </div>
    <ConfigForm fields={AVATAR_FIELDS} form={form} />
    </>
  )
}

export default AvatarConfig;