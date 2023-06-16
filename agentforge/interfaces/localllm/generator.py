import torch
import time, threading, json, logging
from transformers import GenerationConfig, StoppingCriteria, StoppingCriteriaList
import numpy as np
from agentforge.config import Config

def convert_to_serializable(obj):
    if isinstance(obj, StopOnTokens):
        return obj.stop_token_ids
    if isinstance(obj, torch.Tensor):
        return obj.tolist()
    elif isinstance(obj, GenerationConfig):
        return obj.to_dict()
    key_err = f"""Object of type {obj.__class__.__name__} is not JSON serializable;
      Add a new Exception to convert_to_serializable() in agentforge/language_model/logger.py"""
    raise TypeError(key_err)

class StopOnTokens(StoppingCriteria):
  def __init__(self, stop_token_ids):
    self.stop_token_ids = stop_token_ids
  def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
    idx = len(self.stop_token_ids)
    for stop_id in self.stop_token_ids:
      if input_ids[0][-idx] != stop_id:
        return False
      idx -= 1
    return True

# Drives text generation for multiple models.
class LocalGenerator:
  def __init__(self, config: dict):
    if "multi_gpu" in config:
      self.multi_gpu = config["multi_gpu"]
    else:
      self.multi_gpu = False

    # Set at runtime by the base LLM class.
    self.model = None
    self.tokenizer = None
    self.streamer = None

    self.configs = {}

    # simple lock to prevent async calls from stepping on each other
    self.lock = threading.Lock() # for async calls
  
  def set_models(self, model, tokenizer, streamer):
    self.model = model
    self.tokenizer = tokenizer
    self.streamer = streamer

  def prep_max_new_tokens(self, max_new_tokens):
    # grab the config
    if max_new_tokens != 'NaN' and max_new_tokens != None:
      max_new_tokens = int(max_new_tokens)
    else:
      max_new_tokens = 2048
    return max_new_tokens

  def get_probabilities(self, model, tokenizer, inputs, completion):
    trans_scores = model.compute_transition_scores(
      completion.sequences, completion.scores, normalize_logits=True
    )

    input_length = 1 if model.config.is_encoder_decoder else inputs.input_ids.shape[1]
    generated_tokens = completion.sequences[:, input_length:]

    probs = []
    logging.info("""| token | token string | logits | probability |""")
    logging.info("""| ----- | ------------ | ------ | ----------- |""")
    for tok,score in zip(generated_tokens[0], trans_scores[0]):
      score = score.cpu().numpy()
      logging.info(f"| {tok:5d} | {tokenizer.decode([tok]):8s} | {score:.3f} | {np.exp(score):.2%} |")

  # Generates a response given a prompt
  def generate(self, prompt, model, tokenizer, streamer, **kwargs):

    # Set model arguments from generation config.
    if self.multi_gpu:
      config = model.module.generation_config
    else:
      config = model.generation_config

    gen_config = kwargs["generation_config"]

    if 'stopping_criteria' in gen_config:
      stop_val = tokenizer.encode(gen_config['stopping_criteria'])
      stop = StopOnTokens(stop_val)
      stopping_criteria=StoppingCriteriaList([stop])

    gen_config = {k: v for k, v in gen_config.items() if v is not None and v != ""}

    logging.info(prompt)
    with torch.autocast("cuda"):
      inputs = tokenizer(prompt, return_tensors="pt")
      input_ids = inputs.input_ids.cuda()
      generation_config = GenerationConfig(
          **gen_config,
      )
      start_time = time.time()
      with torch.no_grad():
          # If we are using multi-gpu, we need to use the model.module.generate method.
          if self.multi_gpu:
            gen = model.module.generate
          else:
            gen = model.generate
            final_kwargs = {
              'input_ids': input_ids,
              'generation_config': generation_config,
              'attention_mask': inputs.attention_mask,
              'stopping_criteria': stopping_criteria,
          }

          if 'stopping_criteria' in gen_config:
            final_kwargs['stopping_criteria'] = stopping_criteria

          if "eos_token_id" in gen_config:
            final_kwargs['eos_token_id'] = gen_config["eos_token_id"]
          else:
            final_kwargs['eos_token_id'] = tokenizer.eos_token_id
          if "bos_token_id" in gen_config:
            final_kwargs['bos_token_id'] = gen_config["bos_token_id"]
          else:
            final_kwargs['bos_token_id'] = tokenizer.bos_token_id
          if "pad_token_id" in gen_config:
            final_kwargs['pad_token_id'] = gen_config["pad_token_id"]
          else:
            final_kwargs['pad_token_id'] = tokenizer.eos_token_id
  
          logging.info(f"Rendering with {json.dumps(final_kwargs, indent=4, default=convert_to_serializable)}")
          if streamer != None:
            final_kwargs['streamer'] = streamer
          with self.lock:
            generation_output = gen(**final_kwargs)
            if 'return_probabilities' in gen_config and gen_config['return_probabilities']:
              self.get_probabilities(model, tokenizer, inputs, generation_output)
      end_time = time.time()
      execution_time = end_time - start_time
      logging.info(f"Execution time: {execution_time:.6f} seconds")
      s = generation_output.sequences[0]
      output = tokenizer.decode(s, skip_special_tokens=True)
      return output
 
  def dolly(self, prompt, model, tokenizer, _, gc_name=None, **kwargs) -> str:
    kwargs = self.prep_generation_config(gc_name)
    generation_config = GenerationConfig(
        **kwargs,
    )

    kwargs["output_attentions"] = False
    kwargs["output_attentions"] = False
    kwargs["output_hidden_states"] = False
    kwargs["use_cache"] = True # config.use_cache

    kwargs["output_hidden_states"] = False
    kwargs["use_cache"] = True # config.use_cache

    end_key_token_id = tokenizer.encode("### End")[0]
    pad_token_id = tokenizer.pad_token_id
    eos_token_id = end_key_token_id

    input = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")

    if self.multi_gpu:
      gen = model.module.generate
    else:
      gen = model.generate

    outputs = gen(
        input,
        pad_token_id=pad_token_id,
        eos_token_id=eos_token_id,
        max_new_tokens=self.max_new_tokens,
        generation_config=generation_config,
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    fixed_prompt = prompt.replace("### Instruction:", "").replace("### Response:", "")
    response = response.replace(fixed_prompt, "")
    response = response.strip()
    end = "### End"  # the output seems to contain lots of ### End of ...
    if end in response:
      response = response[:response.index(end)].strip()
    if "A: " in response: # GPT loves to add A: with random nonsense
      response = response[:response.index("A: ")].strip() 
    return response