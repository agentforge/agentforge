'use client';
import * as React from 'react';
import CheckboxElement from '@/components/shared/checkbox';
import SelectElement from '@/components/shared/select';
import * as ScrollArea from '@radix-ui/react-scroll-area';
import * as Label from '@radix-ui/react-label';
import ConfigForm from './configform';

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

  const MODEL_FIELDS: ConfigFields = {
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
  };

  const CONFIG_FIELDS: ConfigFields = {
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
      // Handle the form su bmission...
    };
    
    return (
      <ScrollArea.Root className="w-full h-screen rounded overflow-hidden">
      <ScrollArea.Viewport className="w-full h-full rounded">
        <div className="flex w-full mt-3">
            <div className="w-3/4">
              <h1>Rendering</h1>
            </div>
            <div className='flex flex-wrap items-center gap-[15px] px-5 w-1/4'>
                <Label.Root className="text-[15px] font-medium leading-[35px] text-white" htmlFor="firstName">
                  Avatar Presets
                </Label.Root>
                <SelectElement options={avatars} id="avatar" label="Avatar" defaultVal="caretaker" />
              </div>
            {/* <div className='mt-6   w-2/12'>
              <Button color="primary" type="submit">Save</Button>
            </div> */}
          </div>
          <div className="container mx-auto">
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
          <div className='flex flex-row w-full'>
            <div className='flex w-3/4'>
              <h1>Model Config</h1>
            </div>
            <div className='flex w-1/4 mt-3'>
              <div className="flex flex-wrap items-center gap-[15px] px-5">
                <Label.Root className="text-[15px] font-medium leading-[35px] text-white" htmlFor="firstName">
                  Model Presets
                </Label.Root>
                <SelectElement options={models} id="model_key" label="Model" defaultVal="alpaca-lora-7b" />
              </div>
            </div>
          </div>
          <form className="mb-9" onSubmit={handleSubmit}>
          <p className="text-gray-600">Configure the generation parameters for the model.</p>
          <ConfigForm fields={MODEL_FIELDS} form={form} />
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
          <p className="text-gray-600">Configure the generation parameters for the model.</p>
          <ConfigForm fields={CONFIG_FIELDS} form={form} />
          {/* <div className='flex w-full mt-3'>
            <ButtonComponent text="Expand Video" onClick={fullScreen} />
          </div>   */}
            <h1>Prompt Tinkering</h1>
            <div className="flex flex-row mt-9">
              <div className="flex w-1/2">
                  <textarea
                  id="user-input"
                  defaultValue="Prompt goes here..."
                  className="form-control"
                  rows={4}
                  style={{ width: '100%' }}
                ></textarea>
              </div>
              <div className="flex w-1/2 ml-4">
                <div className="flex w-full flex-col space-y-4">
                  <a href="#button1" className="w-full border border-white text-white font-bold py-2 px-4 rounded bg-transparent">
                    instruct
                  </a>

                  <a href="#button2" className="w-full border border-white text-white font-bold py-2 px-4 rounded bg-transparent">
                  instruct_w_memory
                  </a>

                  <a href="#button3" className="w-full border border-white text-white font-bold py-2 px-4 rounded bg-transparent">
                    mpt
                  </a>
                </div>  
              </div>
            </div>
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
    );
  }
  
  export default GenerationConfigForm;
  