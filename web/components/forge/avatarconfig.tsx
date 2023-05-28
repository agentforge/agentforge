'use client';
import * as React from 'react';
import CheckboxElement from '@/components/shared/checkbox';
import SelectElement from '@/components/shared/select';
import * as Label from '@radix-ui/react-label';

//TODO GET FROM API
const avatars = ['caretaker', 'default', 'makhno', 'fdr', 'sankara'];

export default function AvatarConfig() {
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
    <div className="container mx-auto mt-3">
      <div className="flex w-1/2">

        <div className="w-1/4">
          <CheckboxElement label={"Speech"} id="speech" defaultVal={false} />
        </div>
        <div className="w-1/4">
          <CheckboxElement label={"Video"} id="lipsync" defaultVal={false}  />
        </div>
        <div className="w-1/4">
          <CheckboxElement label={"Streaming"} id="streaming" defaultVal={false} />
        </div>
        </div>
      {/* <div className='flex w-full'>
        <SliderElement defaultValue={512} max={2048} step={1} ariaLabel="Max New Tokens" width="200px" sliderId="tokens" />
      </div> */}
      </div>
      <div className="flex flex-row w-1/2 mt-9">
        <div className="flex flex-wrap items-center gap-[15px]">
          <Label.Root className="text-[15px] font-medium leading-[35px] text-white" htmlFor="firstName">
            Name
          </Label.Root>
          <input
            className="bg-blackA5 shadow-blackA9 inline-flex h-[35px] w-[200px] appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-white shadow-[0_0_0_1px] outline-none focus:shadow-[0_0_0_2px_black] selection:color-white selection:bg-blackA9"
            type="text"
            id="name"
            defaultValue=""
          />
        </div>
      </div>
      <Label.Root className="flex mt-3 w-full text-[15px] font-medium leading-[35px] text-white" htmlFor="firstName">
        Biography/Context
      </Label.Root>
      <div className="flex w-1/2">
          <textarea
          id="user-input"
          defaultValue=""
          className="form-control"
          rows={4}
          style={{ width: '100%' }}
        ></textarea>
      </div>
    </>
  )
}
