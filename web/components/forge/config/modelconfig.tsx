'use client';
import * as React from 'react';
import SelectElement from '@/components/shared/form/select';
import * as Label from '@radix-ui/react-label';
import { ConfigForm } from '../../shared/form/configform';

//TODO GET FROM API
const models = [
  'alpaca-lora-7b',
  'alpaca-lora-13b',
  'dolly-v1-6b',
  'dolly-v2-12b',
  'pythia-6.9b-gpt4all-pretrain',
  'vicuna-7b',
];

interface ConfigField {
  type: string;
  default: number | string | boolean | undefined;
  max?: number;
  min?: number;
  step?: number;
  tooltip?: string;
  label?: string;
}

type ConfigFields = {
  [key: string]: ConfigField;
}

export const MODEL_FIELDS: ConfigFields = {
  model_name: { type: 'text', default: 'fragro/llama-7b-hf', tooltip: 'The model name used for generating completions.' },
  tokenizer_name: { type: 'text', default: 'fragro/llama-7b-hf', tooltip: 'The tokenizer name used for generating completions.' },
  peft_model: { type: 'text', default: 'tloen/alpaca-lora-7b', tooltip: 'The model used for post-edit fine-tuning.' },
  prompt_type: { type: 'text', default: 'instruct_w_memory', tooltip: 'The type of prompt used in the model.' },
  model_class: { type: 'text', default: 'AutoCasualModel', tooltip: 'The class of the model.' },
  tokenizer_class: { type: 'text', default: 'AutoTokenizer', tooltip: 'The class of the tokenizer.' },
  pad_token: { type: 'text', default: undefined, tooltip: "The padding token string. Padding tokens are used in batched generation when sequences of different lengths are generated, to make the output a rectangular tensor." },
  bos_token: { type: 'text', default: undefined, tooltip: "The beginning-of-sequence token string. This token is typically used to signal the start of a new sequence, and can be important for models that are designed to generate multiple sequences in a batch." },
  eos_token: { type: 'text', default: undefined, tooltip: "The end-of-sequence token string. This token is used to signal the end of a generated sequence. If the model generates this token, it will stop generating more tokens (unless min_length or min_new_tokens is set to a higher value)." },
  load_in_8bit: { type: 'boolean', default: false, tooltip: "Determines whether the model weights should be loaded in 8-bit. Loading the model in 8-bit can drastically reduce the model size in memory at the cost of a slight degradation in quality. This can be beneficial in resource-constrained environments." },
  load_in_4bit: { type: 'boolean', default: false, tooltip: "Determines whether the model weights should be loaded in 4-bit. Loading the model in 4-bit can drastically reduce the model size in memory at the cost of a slight degradation in quality. This can be beneficial in resource-constrained environments." },
  attn_impl: { type: 'text', default: undefined, tooltip: "Choose 'triton' for MPT based models." },
  speech: { type: 'boolean', default: false, label: 'Speech' },
  video: { type: 'boolean', default: false, label: 'Video' },
  streaming: { type: 'boolean', default: false, label: 'Streaming' },
};


export interface ModelConfigProps {
  form: {[key: string]: string | number | boolean | undefined};
}

export const ModelConfig: React.FC<ModelConfigProps> = ({ form }) =>  {
  return (
      <>
      <div className='flex flex-row w-full'>
      <div className='flex w-3/4'>
        <h1>Model Config</h1>
      </div>
      <div className='flex w-1/4'>
        <div className="flex flex-wrap items-center gap-[15px] px-5">
          <Label.Root className="text-[15px] font-medium leading-[35px] text-white" htmlFor="firstName">
            Model Presets
          </Label.Root>
          <SelectElement options={models} id="model_key" label="Model" defaultVal="alpaca-lora-7b" />
        </div>
      </div>
    </div>
    <p className="text-gray-600">Configure the model, tokenizer, and peft if needed. Be sure to set appropriate EOS tokens for expected behavior.</p>
    <ConfigForm fields={MODEL_FIELDS} form={form} />
    </>
  )
}

export default ModelConfig;
