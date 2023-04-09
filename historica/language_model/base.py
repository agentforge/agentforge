### LLModel class ###
### RESTful API for the LLM services ###
### Maintains any necessary queue and rate limiting for ###
### accessing GPU/TPU resources ###

### Imports ###
import copy
import torch
from historica.config import Config
import logging, time
from historica import DEFAULT_MAX_NEW_TOKENS
from .manager import LLMModelManager
from transformers import GenerationConfig, TextStreamer

### Manages Base LLM functions ###
class LLM():
  def __init__(self,  opts) -> None:
    self.opts = {} if opts == None else opts
    self.model_key = opts.get("model_key", "alpaca-lora-7b")
    self.gc_name = opts.get("generation_config", "llm/logical")
    
    # Loads the model configuration
    self.generation_config = Config(self.gc_name)
    self.device = opts.get("device", "cuda")

    # create a shared dictionary to store the model to be used by other workers
    logging.info(f"LLM CUDA enabled: {self.device == 'cuda' and torch.cuda.is_available()}")

    # Load LLM Model Manager
    self.llm = LLMModelManager()

  def configure(self, config) -> None:
    self.set_generation_config(config.get("generation_config", self.gc_name))
    self.set_max_new_tokens(config.get("max_new_tokens", DEFAULT_MAX_NEW_TOKENS))
    self.load(config.get("model_key", self.llm.key))

  def set_max_new_tokens(self, max_new_tokens):
    # grab the config
    if max_new_tokens != 'NaN':
      self.max_new_tokens = int(max_new_tokens)
    else:
      self.max_new_tokens = DEFAULT_MAX_NEW_TOKENS

  def set_generation_config(self, generation_config):
    # grab the config
    if self.gc_name != generation_config:
      self.generation_config = Config("llm/" + generation_config)
      self.gc_name = generation_config

  # Get the name of the class
  def name(self):
    return self.__class__.__name__

  # Get status of the GPU
  def gpu(self) -> bool:
    return self.device == "cuda" and torch.cuda.is_available()

  # Loads the model and transfomer given the model name
  def load(self, model_key=None, **kwargs) -> None:
    # If we aren't overriding use the default model
    if model_key == None:
      model_key = self.model_key

    # If we are already using this model, don't reload
    if model_key == self.llm.key:
      return  
    
    # Load the model
    self.llm.switch_model(model_key)
    
    # Create the streamer after loading tokenizer
    self.streamer = TextStreamer(self.llm.tokenizer)

  # Generates a response given a prompt
  def generate(self, prompt, gc_name=None):
    if gc_name is not None:
      self.set_generation_config(gc_name)
    kwargs = self.generation_config.to_dict()

    # Separate model arguments from generation config.
    config = self.llm.model.generation_config
    config = copy.deepcopy(config)
    kwargs = config.update(**kwargs)
    kwargs["output_attentions"] = False
    kwargs["output_hidden_states"] = False
    kwargs["use_cache"] = config.use_cache

    # Collect special token IDs.
    pad_token_id = config.pad_token_id
    bos_token_id = config.bos_token_id
    eos_token_id = config.eos_token_id

    if isinstance(eos_token_id, int):
        eos_token_id = [eos_token_id]
    if pad_token_id is None and eos_token_id is not None:
        kwargs["pad_token_id"] = eos_token_id[0]

    print(f"Rendering with {kwargs}")

    return self._generate(prompt, **kwargs)
  
  def _generate(
          self,
          instruct,
          **kwargs,
  ):
      # print(instruct)
      inputs = self.llm.tokenizer(instruct, return_tensors="pt")
      input_ids = inputs["input_ids"].cuda()
      generation_config = GenerationConfig(
          **kwargs,
      )
      # print(prompt)
      print("GENERATE...")
      print(generation_config)
      # raise Exception("STOP")
      start_time = time.time()
      with torch.no_grad():
          generation_output = self.llm.model.generate(
              input_ids=input_ids,
              generation_config=generation_config,
              return_dict_in_generate=True,
              output_scores=True,
              max_new_tokens=self.max_new_tokens,
              streamer=self.streamer,
          )
      end_time = time.time()
      execution_time = end_time - start_time
      print(f"Execution time: {execution_time:.6f} seconds")
      s = generation_output.sequences[0]
      output = self.llm.tokenizer.decode(s)
      output = self.parse(output)
      # print(output)
      return output

  # Returns and AgentResponse object that 
  def parse(self, output):
    responses = output.split("### Response:")
    candidate = responses[len(responses)-1].strip()
    # candidate = helpers.process_code_output(candidate)
    candidate = candidate.lstrip('\n')
    return candidate