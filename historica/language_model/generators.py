import torch
import time
from transformers import GenerationConfig
import numpy as np
from historica.config import Config
from historica import DEFAULT_MAX_NEW_TOKENS

# Drives text generation for multiple models.
class Generator:

  def __init__(self, gc_name=None, multi_gpu=False):
    self.gc_name = gc_name
    self.streameer = None
    self.multi_gpu = multi_gpu
    
    # Set at runtime by the base LLM class.
    self.model = None
    self.tokenizer = None
    self.streamer = None

  #Prep GenerationConfig
  def set_generation_config(self, gc_name=None, **kwargs):
    if gc_name is not None:
      # grab the config
      if self.gc_name != gc_name:
        self.generation_config = Config("llm/" + gc_name)
        self.gc_name = gc_name
    kwargs = self.generation_config.to_dict()
    return kwargs
  
  def set_models(self, model, tokenizer, streamer):
    self.model = model
    self.tokenizer = tokenizer
    self.streamer = streamer

  def set_max_new_tokens(self, max_new_tokens):
    # grab the config
    if max_new_tokens != 'NaN' and max_new_tokens != None:
      self.max_new_tokens = int(max_new_tokens)
    else:
      self.max_new_tokens = DEFAULT_MAX_NEW_TOKENS

  # Generates a response given a prompt
  def generate(self, prompt, model, tokenizer, streamer, gc_name=None, multi_gpu=False, **kwargs):

    kwargs = self.set_generation_config(gc_name)

    # Set model arguments from generation config.
    if multi_gpu:
      config = self.model.module.generation_config
    else:
      config = self.model.generation_config

    kwargs["output_attentions"] = False
    kwargs["output_hidden_states"] = False
    kwargs["use_cache"] = True # config.use_cache

    # Collect special token IDs.
    pad_token_id = config.pad_token_id
    bos_token_id = config.bos_token_id
    eos_token_id = config.eos_token_id

    if pad_token_id is None and eos_token_id is not None:
        self.model.generation_config.pad_token_id = eos_token_id

    # # Generate from eos if no input is specified.
    # if input_length == 0:
    #     input_ids = input_ids.new_ones((batch_size, 1)).long()
    #     if eos_token_id is not None:
    #         input_ids = input_ids * eos_token_id[0]
    #     input_length = 1

    print(f"Rendering with {kwargs}")

    with torch.autocast("cuda"):
      inputs = self.tokenizer(prompt, return_tensors="pt")
      input_ids = inputs["input_ids"].cuda()
      generation_config = GenerationConfig(
          **kwargs,
      )
      print("GENERATE...")
      print(generation_config)
      start_time = time.time()
      with torch.no_grad():
          # Set model arguments from generation config.
          if self.multi_gpu:
            gen = self.model.module.generate
          else:
            gen = self.model.generate
          kwargs = {
              'input_ids': input_ids,
              'generation_config': generation_config,
              'return_dict_in_generate': True,
              'output_scores': True,
              'max_new_tokens': self.max_new_tokens
          }
          if self.streamer != None:
            kwargs['streamer'] = self.streamer
          generation_output = gen(**kwargs)
      end_time = time.time()
      execution_time = end_time - start_time
      print(f"Execution time: {execution_time:.6f} seconds")
      s = generation_output.sequences[0]
      output = self.tokenizer.decode(s)
      return output
 
  def dolly(self, instruction: str, model, tokenizer, _, gc_name=None, **kwargs) -> str:
    print(instruction)
    kwargs = self.set_generation_config(gc_name)
    generation_config = GenerationConfig(
        **kwargs,
    )

    input_ids = tokenizer(instruction, return_tensors="pt").input_ids.to("cuda")

    # each of these is encoded to a single token
    response_key_token_id = tokenizer.encode("### Response:")[0]
    end_key_token_id = tokenizer.encode("### End")[0]

    gen_tokens = model.generate(input_ids, pad_token_id=tokenizer.pad_token_id, eos_token_id=end_key_token_id,
                                generation_config=generation_config, max_new_tokens=self.max_new_tokens,**kwargs)[0].cpu()

    # find where the response begins
    response_positions = np.where(gen_tokens == response_key_token_id)[0]

    if len(response_positions) >= 0:
        response_pos = response_positions[0]
        
        # find where the response ends
        end_pos = None
        end_positions = np.where(gen_tokens == end_key_token_id)[0]
        if len(end_positions) > 0:
            end_pos = end_positions[0]

        return tokenizer.decode(gen_tokens[response_pos + 1 : end_pos]).strip()

    return None
