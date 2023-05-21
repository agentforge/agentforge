'use client';
import * as React from 'react';
import SelectElement from '@/components/shared/select';
import * as Label from '@radix-ui/react-label';
import { ConfigForm } from './configform';

//TODO GET FROM API
const modelConfigs = ['logical', 'creative', 'moderate'];

interface ConfigField {
  type: string;
  default: number | string | boolean | undefined;
  max?: number;
  min?: number;
  step?: number;
  tooltip?: string;
}

type ConfigFields = {
  [key: string]: ConfigField;
}

export const GENERATION_FIELDS: ConfigFields = {
  max_new_tokens: { type: 'number', default: 512, max: 2048, min: 0, step: 1, tooltip: "The maximum number of new tokens to generate. \n This limits the number of tokens that the model will generate, potentially stopping the generation process before reaching the natural end." },
  top_k: { type: 'number', default: 50, tooltip: "The number of highest probability vocabulary tokens to keep for top-k-filtering. This can limit the options the model considers, preventing it from choosing very low-probability tokens and increasing the overall quality of the output." },
  top_p: { type: 'number', default: 1.0, tooltip:  "The cumulative probability cutoff for token selection (also known as nucleus sampling). If set to less than 1, the model only considers a subset of tokens whose combined probability exceeds the top_p value. This can lead to more focused outputs and prevents very low-probability tokens from being chosen." },
  temperature: { type: 'number', default: 1.0, tooltip: "The value used to modulate the next token probabilities. Higher values make the outputs more random, while smaller values make the output more focused on high-probability tokens." },
  repetition_penalty: { type: 'number', default: 1.2, tooltip: "The parameter for repetition penalty. Defaults to 1.0." },
  min_new_tokens: { type: 'number', default: undefined, tooltip: "The minimum number of new tokens to generate. The model will continue to generate tokens until it has produced at least this many new ones." },
  early_stopping: { type: 'string', default: 'False', tooltip:  "Controls the stopping condition for beam-based methods. If True, generation is stopped when at least num_beams sentences finished per batch item, otherwise it continues until max_length is reached." },
  max_time: { type: 'number', default: undefined, tooltip:"The maximum amount of time you allow the computation to run for in seconds. It's a safeguard to prevent the generation process from running indefinitely." },
  do_sample: { type: 'boolean', default: false, tooltip: "If set to False, the model will use a greedy decoding approach, always choosing the token with the highest probability as the next token. If True, the model will sample from the distribution of next token probabilities, potentially creating more diverse outputs at the cost of more mistakes." },
  num_beams: { type: 'number', default: 1, tooltip:  "Number of beams for beam search. Beam search is a decoding strategy that maintains multiple hypotheses (the 'beams') at each step and chooses the most probable sequence of tokens among them. This can improve the quality of the output but increases computational cost." },
  num_beam_groups: { type: 'number', default: 1, tooltip: "Number of groups to divide num_beams into. This introduces diversity in the beam search by having different groups explore different parts of the probability space." },
  penalty_alpha: { type: 'number', default: undefined, tooltip: "The values balance the model confidence and the degeneration penalty." },
  use_cache: { type: 'boolean', default: true, tooltip: "Whether or not the model should use the past last key/values attentions. Defaults to True." },
  typical_p: { type: 'number', default: 1.0, tooltip: "Local typicality measures. Defaults to 1.0." },
  epsilon_cutoff: { type: 'number', default: 0.0, tooltip: "If set to float strictly between 0 and 1, only tokens with a conditional probability greater than epsilon_cutoff will be sampled. Defaults to 0.0." },
  eta_cutoff: { type: 'number', default: 0.0, tooltip: "Eta sampling. Defaults to 0.0." },
  diversity_penalty: { type: 'number', default: 0.0, tooltip: "This value is subtracted from a beam’s score if it generates a token same as any beam from other group at a particular time. Defaults to 0.0." },
  encoder_repetition_penalty: { type: 'number', default: 1.0, tooltip: "The paramater for encoder_repetition_penalty. Defaults to 1.0." },
  length_penalty: { type: 'number', default: 1.0, tooltip: "Exponential penalty to the length. Defaults to 1.0." },
  no_repeat_ngram_size: { type: 'number', default: 0, tooltip: "If set to an integer greater than 0, the model is not allowed to generate any ngrams (sequences of n tokens) that it has already generated. This can prevent repetitive outputs and increase the diversity of the generated text." },
  bad_words: { type: 'text', default: undefined, tooltip: "List of token ids that are not allowed to be generated. This can be used to prevent the model from generating specific words or phrases." },
  force_words: { type: 'text', default: undefined, tooltip: "List of token ids that must be generated." },
  renormalize_logits: { type: 'boolean', default: false, tooltip: "Whether to renormalize the logits after applying all the logits processors or warpers. Defaults to False." },
  forced_bos_token: { type: 'text', default: undefined, tooltip: "The token to force as the first generated token. Defaults to model.config.forced_bos_token_id." },
  forced_eos_token: { type: 'text', default: undefined, tooltip: "The token to force as the last generated token. Defaults to model.config.forced_eos_token_id." },
  remove_invalid_values: { type: 'boolean', default: false, tooltip: "Whether to remove possible nan and inf outputs of the model. Defaults to model.config.remove_invalid_values." },
  exponential_decay_length_penalty: { type: 'text', default: undefined, tooltip: "An exponentially increasing length penalty." },
  suppress_tokens: { type: 'text', default: undefined, tooltip: "A list of tokens that will be suppressed at generation." },
  begin_suppress_tokens: { type: 'text', default: undefined, tooltip: "A list of tokens that will be suppressed at the beginning of the generation." },
  forced_decoder_ids: { type: 'text', default: undefined, tooltip: "A list of pairs of integers which indicates a mapping from generation indices to token indices that will be forced before sampling." },
  num_return_sequences: { type: 'number', default: 1, tooltip: "The number of independently computed returned sequences for each element in the batch. Defaults to 1." },
  output_attentions: { type: 'boolean', default: false, tooltip: "Whether or not to return the attentions tensors of all attention layers. Defaults to False." },
  output_hidden_states: { type: 'boolean', default: false, tooltip: "Whether or not to return the hidden states of all layers. Defaults to False." },
  output_scores: { type: 'boolean', default: false, tooltip: "Whether or not to return the prediction scores. Defaults to False." },
  return_dict_in_generate: { type: 'boolean', default: false, tooltip: "Whether or not to return a ModelOutput instead of a plain tuple. Defaults to False." },
  encoder_no_repeat_ngram_size: { type: 'number', default: 0, tooltip: "If set to an integer greater than 0, any ngrams of that size that occur in the encoder input cannot occur in the decoder output. This can be useful in tasks like summarization to prevent the model from simply copying large chunks of the input." },
  decoder_start_token: { type: 'text', default: undefined, tooltip: "If an encoder-decoder model starts decoding with a different token than bos, the id of that token.  the token that should be used as the first token for the decoder when generating a sequence. This is typically used in sequence-to-sequence tasks where the start token for the decoder may be different from the BOS token." }
};

export interface ConfigProps {
  form: {[key: string]: string | number | boolean | undefined};
}

export const GenerationConfigForm: React.FC<ConfigProps> = ({ form }) => {
  console.log(form);
  return (
    <>
    <div className='flex flex-row w-full'>
    <div className='flex w-3/4'>
      <h1>Generation Config</h1>
      </div>
      <div className='flex w-1/4 mt-3'>
        <div className="flex flex-wrap items-center gap-[15px] px-5">
          <Label.Root className="text-[15px] font-medium leading-[35px] text-white" htmlFor="firstName">
            Generation Presets
          </Label.Root>
          <SelectElement options={ modelConfigs } id="generation_config" label="Presets" defaultVal="logical" />
        </div>
      </div>
    </div>
    <p className="text-gray-600">Configure the generation parameters for inference and prompt completion.</p>
    <ConfigForm fields={GENERATION_FIELDS} form={form} />
    </>
  )
}

export default GenerationConfigForm;
