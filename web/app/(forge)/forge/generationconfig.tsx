'use client';
import * as React from 'react';
import { Input, Button, Checkbox, Text, Spacer } from '@nextui-org/react';
import CheckboxElement from '@/components/shared/checkbox';
import SelectElement from '@/components/shared/select';
import SliderElement from '@/components/shared/slider';
import { RemoveScroll } from 'react-remove-scroll';

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

  const CONFIG_FIELDS = {
    max_new_tokens: { type: 'number', default: 512, max: 2048, min: 0, step: 1 },
    min_length: { type: 'number', default: 0 },
    min_new_tokens: { type: 'number', default: undefined },
    early_stopping: { type: 'string', default: 'False' },
    max_time: { type: 'number', default: undefined },
    do_sample: { type: 'boolean', default: false },
    num_beams: { type: 'number', default: 1 },
    num_beam_groups: { type: 'number', default: 1 },
    penalty_alpha: { type: 'number', default: undefined },
    use_cache: { type: 'boolean', default: true },
    temperature: { type: 'number', default: 1.0 },
    top_k: { type: 'number', default: 50 },
    top_p: { type: 'number', default: 1.0 },
    typical_p: { type: 'number', default: 1.0 },
    epsilon_cutoff: { type: 'number', default: 0.0 },
    eta_cutoff: { type: 'number', default: 0.0 },
    diversity_penalty: { type: 'number', default: 0.0 },
    repetition_penalty: { type: 'number', default: 1.0 },
    encoder_repetition_penalty: { type: 'number', default: 1.0 },
    length_penalty: { type: 'number', default: 1.0 },
    no_repeat_ngram_size: { type: 'number', default: 0 },
    bad_words_ids: { type: 'text', default: undefined },
    force_words_ids: { type: 'text', default: undefined },
    renormalize_logits: { type: 'boolean', default: false },
    forced_bos_token_id: { type: 'number', default: undefined },
    forced_eos_token_id: { type: 'number', default: undefined },
    remove_invalid_values: { type: 'boolean', default: false },
    exponential_decay_length_penalty: { type: 'text', default: undefined },
    suppress_tokens: { type: 'text', default: undefined },
    begin_suppress_tokens: { type: 'text', default: undefined },
    forced_decoder_ids: { type: 'text', default: undefined },
    num_return_sequences: { type: 'number', default: 1 },
    output_attentions: { type: 'boolean', default: false },
    output_hidden_states: { type: 'boolean', default: false },
    output_scores: { type: 'boolean', default: false },
    return_dict_in_generate: { type: 'boolean', default: false },
    pad_token_id: { type: 'number', default: undefined },
    bos_token_id: { type: 'number', default: undefined },
    eos_token_id: { type: 'number', default: undefined },
    encoder_no_repeat_ngram_size: { type: 'number', default: 0 },
    decoder_start_token_id: { type: 'number', default: undefined },
  };

  //TODO GET FROM API
  const avatars = ['caretaker', 'default', 'makhno', 'fdr', 'sankara'];
  const modelConfigs = ['logical', 'creative', 'moderate'];
  const models = [
    'alpaca-lora-7b',
    'alpaca-lora-13b',
    'dolly-v1-6b',
    'dolly-v2-12b',
    'pythia-6.9b-gpt4all-pretrain',
    'vicuna-7b',
  ];
  
  function GenerationConfigForm() {
    // Create a state object with default values from the config
    const [form, setForm] = React.useState(
      Object.fromEntries(Object.entries(CONFIG_FIELDS).map(([key, { default: defaultValue }]) => [key, defaultValue]))
    );
  
    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      // Handle the form submission...
    };

    return (
      <RemoveScroll>
        <div className="flex w-full mt-3">
          <div className="w-10/12">
            <Text h1>Rendering</Text>
          </div>
          <div className='mt-6   w-2/12'>
            <Button color="primary" type="submit">Save</Button>
          </div>
        </div>
        <div className="container mx-auto">
          <div className="flex w-1/2 mt-3">
            <div className="w-1/2">
              <CheckboxElement label={"Speech"} id="speech" defaultVal={false} />
            </div>
            <div className="w-1/2">
              <CheckboxElement label={"Video"} id="lipsync" defaultVal={false}  />
            </div>
            <div className="w-1/2">
              <CheckboxElement label={"Streaming"} id="streaming" defaultVal={false} />
            </div>
          </div>
          {/* <div className='flex w-full'>
            <SliderElement defaultValue={512} max={2048} step={1} ariaLabel="Max New Tokens" width="200px" sliderId="tokens" />
          </div> */}
        </div>
        <div className='flex w-1/2'>
          <div className='flex w-1/3 mt-3'>
            <SelectElement options={avatars} id="avatar" label="Avatar" defaultVal="caretaker" />
          </div>
          <div className='flex w-1/3 mt-3'>
            <SelectElement options={ modelConfigs } id="generation_config" label="Prompt Config" defaultVal="logical" />
          </div>
          <div className='flex w-1/3 mt-3'>
            <SelectElement options={models} id="model_key" label="Model" defaultVal="alpaca-lora-7b" />
          </div>
        </div>
        <Text h1>Text Generation</Text>
        <p className="text-gray-600">Configure the generation parameters for the model.</p>
      <form onSubmit={handleSubmit}>
        {
          (() => {
            let rows: JSX.Element[] = [];
            let elements: JSX.Element[] = [];
            let counter = 0;
            const N = 4; // Replace with your desired value

            Object.entries(CONFIG_FIELDS).forEach(([key, { type }], index) => {
              let element: JSX.Element | null;

              switch (type) {
                case 'slider':
                  let sliderVal = '';
                  if (form[key] !== undefined) {
                    sliderVal = form[key]!.toString();
                  }
                  element = (
                    <div className="flex w-1/4">
                      <SliderElement defaultValue={512} max={2048} step={1} ariaLabel={key} sliderId="tokens" />
                      <Spacer y={2.5} />
                    </div>
                      );
                  break;
                case 'number':
                  let val = '';
                  if (form[key] !== undefined) {
                    val = form[key]!.toString();
                  }
                  element = (
                    <div className="flex w-1/4">
                      <Input bordered key={key} labelPlaceholder={key} type="number" />
                      <Spacer y={2.5} />
                    </div>
                  );
                  break;
                case 'boolean':
                  // Handle typesafety
                  let variable: string | number | boolean | undefined = form[key];
                  let booleanVariable: boolean | undefined;
                  if (typeof variable === 'boolean' || typeof variable === 'undefined') {
                    booleanVariable = variable;
                    element = (
                      <div className="flex w-1/4">
                        <Checkbox key={key} label={key} name={key} isSelected={booleanVariable} />
                      </div>
                    );
                  } else {
                    element = <span>Error incorrect type</span>;
                  }
                  break;

                // ... handle more field types ...
                default:
                  element = null;
              }

              if (element) {
                elements.push(element);
                counter++;
                if (counter === N || index === CONFIG_FIELDS.length - 1) {
                  rows.push(<div className="flex flex-row mt-9" key={`row${index}`}>{elements}</div>);
                  elements = [];
                  counter = 0;
                }
              }
            });

            return rows;
          })()
        }
        {/* <div className='flex w-full mt-3'>
          <ButtonComponent text="Expand Video" onClick={fullScreen} />
        </div>   */}
      </form>
      </RemoveScroll>
    );
  }
  
  export default GenerationConfigForm;
  