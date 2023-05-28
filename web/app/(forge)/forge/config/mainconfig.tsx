'use client';
import * as React from 'react';
import CheckboxElement from '@/components/shared/checkbox';
import SelectElement from '@/components/shared/select';
import * as ScrollArea from '@radix-ui/react-scroll-area';
import * as Label from '@radix-ui/react-label';
import ConfigForm from './configform';
import * as ToggleGroup from '@radix-ui/react-toggle-group';
import { AvatarIcon, MixIcon, MixerHorizontalIcon, InputIcon } from '@radix-ui/react-icons';
import AvatarConfig from './avatarconfig';
import ModelConfig from './modelconfig';
import { GENERATION_FIELDS } from './genconfig';
import { MODEL_FIELDS } from './modelconfig';
import GenerationConfigForm from './genconfig';
import PromptConfig from './promptconfig';
import Button from '@/components/shared/button';

  interface GenerationConfig {
    // Parameters that control the length of the output
    max_length?: number; // The maximum length the generated tokens can have. Defaults to 20.
    max_new_tokens?: number; // The maximum numbers of tokens to generate.
    min_length?: number; // The minimum length of the sequence to be generated. Defaults to 0.
    min_new_tokens?: number; // The minimum numbers of tokens to generate.
    early_stopping?: boolean | string; // Controls the stopping condition for beam-based methods. Defaults to False.
    max_time?: number; // The maximum amount of time you allow the computation to run for in seconds.
  
    // Parameters that control the generation strategy used
    do_sample?: boolean; // Whether or not to use sampling. Defaults to False.
    num_beams?: number; // Number of beams for beam search. Defaults to 1.
    num_beam_groups?: number; // Number of groups to divide num_beams into. Defaults to 1.
    penalty_alpha?: number; // The values balance the model confidence and the degeneration penalty.
    use_cache?: boolean; // Whether or not the model should use the past last key/values attentions. Defaults to True.
  
    // Parameters for manipulation of the model output logits
    temperature?: number; // The value used to modulate the next token probabilities. Defaults to 1.0.
    top_k?: number; // The number of highest probability vocabulary tokens to keep for top-k-filtering. Defaults to 50.
    top_p?: number; // If set to float < 1, only the smallest set of most probable tokens with probabilities that add up to top_p or higher are kept for generation. Defaults to 1.0.
    typical_p?: number; // Local typicality measures. Defaults to 1.0.
    epsilon_cutoff?: number; // If set to float strictly between 0 and 1, only tokens with a conditional probability greater than epsilon_cutoff will be sampled. Defaults to 0.0.
    eta_cutoff?: number; // Eta sampling. Defaults to 0.0.
    diversity_penalty?: number; // This value is subtracted from a beam’s score if it generates a token same as any beam from other group at a particular time. Defaults to 0.0.
    repetition_penalty?: number; // The parameter for repetition penalty. Defaults to 1.0.
    encoder_repetition_penalty?: number; // The paramater for encoder_repetition_penalty. Defaults to 1.0.
    length_penalty?: number; // Exponential penalty to the length. Defaults to 1.0.
    no_repeat_ngram_size?: number; // If set to int > 0, all ngrams of that size can only occur once. Defaults to 0.
    bad_words_ids?: number[][]; // List of token ids that are not allowed to be generated.
    force_words_ids?: number[][] | number[][][]; // List of token ids that must be generated.
    renormalize_logits?: boolean; // Whether to renormalize the logits after applying all the logits processors or warpers. Defaults to False.
    forced_bos_token_id?: number; // The id of the token to force as the first generated token. Defaults to model.config.forced_bos_token_id.
    forced_eos_token_id?: number | number[]; // The id of the token to force as the last generated token. Defaults to model.config.forced_eos_token_id.
    remove_invalid_values?: boolean; // Whether to remove possible nan and inf outputs of the model. Defaults to model.config.remove_invalid_values.
    exponential_decay_length_penalty?: [number, number]; // An exponentially increasing length penalty.
    suppress_tokens?: number[]; // A list of tokens that will be suppressed at generation.
    begin_suppress_tokens?: number[]; // A list of tokens that will be suppressed at the beginning of the generation.
    forced_decoder_ids?: number[][]; // A list of pairs of integers which indicates a mapping from generation indices to token indices that will be forced before sampling.
    
    // Parameters that define the output variables of generate
    num_return_sequences?: number; // The number of independently computed returned sequences for each element in the batch. Defaults to 1.
    output_attentions?: boolean; // Whether or not to return the attentions tensors of all attention layers. Defaults to False.
    output_hidden_states?: boolean; // Whether or not to return the hidden states of all layers. Defaults to False.
    output_scores?: boolean; // Whether or not to return the prediction scores. Defaults to False.
    return_dict_in_generate?: boolean; // Whether or not to return a ModelOutput instead of a plain tuple. Defaults to False.
    
    // Special tokens that can be used at generation time
    pad_token_id?: number; // The id of the padding token.
    bos_token_id?: number; // The id of the beginning-of-sequence token.
    eos_token_id?: number | number[]; // The id of the end-of-sequence token.
    
    // Generation parameters exclusive to encoder-decoder models
    encoder_no_repeat_ngram_size?: number; // If set to int > 0, all ngrams of that size that occur in the encoder_input_ids cannot occur in the decoder_input_ids. Defaults to 0.
    decoder_start_token_id?: number; // If an encoder-decoder model starts decoding with a different token than bos, the id of that token.
  }

  export interface ConfigProps {
    form: {[key: string]: string | number | boolean | undefined};
  }  
  
  function MainConfigForm() {
    // Create a state object with default values from the config
    let config1 = Object.fromEntries(Object.entries(GENERATION_FIELDS).map(([key, { default: defaultValue }]) => [key, defaultValue]))
    let config2= Object.fromEntries(Object.entries(MODEL_FIELDS).map(([key, { default: defaultValue }]) => [key, defaultValue]))
    let mergedObject = { ...config1, ...config2 };
    const [form, setForm] = React.useState(mergedObject);
    const [currentTab, setCurrentTab] = React.useState<string>('avatar'); //defaults to avatar tab

    const handleSubmit = () => {
      // Handle the form su bmission...
      console.log("handleSubmit");
    };

    const handleRender = (value: string) => {
      // Set the current state of the tab to `value`
      setCurrentTab(value);
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
      <form className="pb-28">ModelConfig
        {currentTab == "avatar" ? ( <AvatarConfig />) : (<></>) }
        {currentTab == "model" ? (<ModelConfig form={ form } />) : (<></>) }
        {currentTab == "generation" ? (<GenerationConfigForm form={ form } />) : (<></>) }
        {currentTab == "prompt" ? (<PromptConfig form={ form } />) : (<></>) }
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
  
  export default MainConfigForm;
  