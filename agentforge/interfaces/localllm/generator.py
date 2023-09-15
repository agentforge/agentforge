import torch
import time, threading, json, logging
from transformers import GenerationConfig, StoppingCriteriaList, StoppingCriteria
import numpy as np
from typing import Optional, TypedDict, NamedTuple, List, Dict, Callable
from agentforge.config import Config
from agentforge.utils import logger

def convert_to_serializable(obj):
    if isinstance(obj, _SentinelTokenStoppingCriteria):
        return obj.sentinel_token_ids
    if isinstance(obj, torch.Tensor):
        return obj.tolist()
    elif isinstance(obj, GenerationConfig):
        return obj.to_dict()
    key_err = f"""Object of type {obj.__class__.__name__} is not JSON serializable;
      Add a new Exception to convert_to_serializable() in agentforge/language_model/logger.py"""
    raise TypeError(key_err)

class _SentinelTokenStoppingCriteria(StoppingCriteria):

    def __init__(self, sentinel_token_ids: list, starting_idx: int):
        StoppingCriteria.__init__(self)
        self.sentinel_token_ids = sentinel_token_ids
        self.starting_idx = starting_idx
        if len(self.sentinel_token_ids) > 0:
          self.shortest = min([x.shape[-1] for x in sentinel_token_ids])

    def __call__(self, input_ids: torch.LongTensor, _scores: torch.FloatTensor) -> bool:
        for sample in input_ids:
            trimmed_sample = sample[self.starting_idx:]
            trimmed_len = trimmed_sample.shape[-1]
            if trimmed_len < self.shortest:
                continue

            for sentinel in self.sentinel_token_ids:
                sentinel_len = sentinel.shape[-1]
                if trimmed_len < sentinel_len:
                    continue

                window = trimmed_sample[-sentinel_len:]
                logger.info(f"{sentinel} == {window}")
                if torch.all(torch.eq(sentinel, window)):
                    return True

        return False

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

  def valid_token(self, token_str, gen_config):
    if token_str in gen_config and gen_config[token_str] != None and gen_config[token_str] != "":
      return True
    return False

  def cgenerate(self, prompt, model, tokenizer, streamer, **kwargs):
    tokens = tokenizer.encode(prompt)
    ret = ""
    for token in model.generate(tokens):
        v = tokenizer.decode(token)
        print(v)
        ret += v
    return ret

  # Generates a response given a prompt
  def generate(self, prompt, model, tokenizer, slow_tokenizer, streamer, **kwargs):
    # Set model arguments from generation config.
    if self.multi_gpu:
      config = model.module.generation_config
    else:
      config = model.generation_config
    # kwargs["generation_config"].update(vars(config))
    gen_config = kwargs["generation_config"]
    model_config = kwargs["model_config"]
    sequence_bias_vals = kwargs['sequence_bias'] if 'sequence_bias' in kwargs else None
    sequence_bias = {}
    if sequence_bias_vals is not None:
      for s in sequence_bias_vals:
        sequence_bias[tuple(slow_tokenizer([s], add_special_tokens=False).input_ids[0])] = 100.0
    logger.info(f"{sequence_bias=}")
    # Config drive overrides -- ID over string
    if "eos_token_id" in model_config:
      print("eos_token_id set...")
      gen_config["eos_token_id"] = model_config["eos_token_id"]
    elif self.valid_token("eos_token", model_config):
      gen_config["eos_token_id"] = tokenizer.encode(model_config["eos_token"])[0]
    else:
      gen_config["eos_token_id"] = config.eos_token_id

    if self.valid_token("bos_token", model_config):
      gen_config["bos_token_id"] = tokenizer.encode(model_config["bos_token"])[0]
    else:
      gen_config["bos_token_id"] = config.bos_token_id
    
    if self.valid_token("pad_token", model_config):
      gen_config["pad_token_id"] = tokenizer.encode(model_config["pad_token"])[0]
    else:
      gen_config["pad_token_id"] = config.pad_token_id

    gen_config = {k: v for k, v in gen_config.items() if v is not None and v != ""}

     # Token IDs -- faster and cheaper
    if "stopping_criteria" in gen_config:
      logging.info("[STOPS]")
      logging.info(gen_config["stopping_criteria"])
      stop_words = gen_config["stopping_criteria"]
    else:
      stop_words = []

    ## less efficient to tokenize so often but works for dynamic
    if "stopping_criteria_string" in gen_config:
        stop_word_strings = gen_config["stopping_criteria_string"].split(",")
    else:
       stop_word_strings = []

    for txt in stop_word_strings:
      tok = tokenizer.encode(f"{txt}", add_special_tokens=False)
      stop_words.append(tok)
      tok = tokenizer.encode(f"<s>{txt}", add_special_tokens=False)[1:]
      stop_words.append(tok)

    stopping_criteria_list = StoppingCriteriaList()

    sentinel_token_ids = []
    for l in stop_words:
        sentinel_token_ids.append(torch.LongTensor(l).cuda()) #also consider 29937, 2277

    with torch.autocast("cuda"):
      inputs = tokenizer(prompt, return_tensors="pt")
      input_ids = inputs["input_ids"].cuda()
      if len(stop_words) > 0:
        logger.info("sentinel_token_ids")
        logger.info(sentinel_token_ids)
        stopping_criteria_list.append(
            _SentinelTokenStoppingCriteria(
                sentinel_token_ids=sentinel_token_ids, starting_idx=len(input_ids[0])
            )
        )
      generation_config = GenerationConfig(
          **gen_config,
      )
      start_time = time.time()

      with torch.no_grad():
          # instantiate logits processors
          # logits_processor = LogitsProcessorList(
          #     [
          #         MinLengthLogitsProcessor(10, eos_token_id=model.generation_config.eos_token_id),
          #     ]
          # )
          # If we are using multi-gpu, we need to use the model.module.generate method.
          if self.multi_gpu:
            gen = model.module.generate
          else:
            gen = model.generate
          
          final_kwargs = {
              'input_ids': input_ids,
              'generation_config': generation_config,
              'return_dict_in_generate': True,
              'attention_mask': torch.ones_like(input_ids),
          }

          if len(stopping_criteria_list) > 0:
            final_kwargs["stopping_criteria"] = stopping_criteria_list

          # logging.info(f"Rendering with {json.dumps(final_kwargs, indent=4, default=convert_to_serializable)}")

          ### Extra kwargs
          if streamer != None:
            final_kwargs['streamer'] = streamer
          if len(sequence_bias.keys()) > 0:
            final_kwargs['sequence_bias'] = sequence_bias

          with self.lock:
            generation_output = gen(**final_kwargs)
            if 'return_probabilities' in gen_config and gen_config['return_probabilities']:
              self.get_probabilities(model, tokenizer, inputs, generation_output)
      end_time = time.time()
      execution_time = end_time - start_time
      logging.info(f"Execution time: {execution_time:.6f} seconds")
      s = generation_output.sequences[0]
      output = tokenizer.decode(s)
      logging.info(f"Output: {output}")
      return output
 