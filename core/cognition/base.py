### LLModel class ###
### RESTful API for the LLM services ###
### Maintains any necessary queue and rate limiting for ###
### accessing GPU/TPU resources ###

### Imports ###
import torch
from core.config.config import Config
import logging
from core.cognition.manager import LLMModelManager

DEFAULT_MAX_NEW_TOKENS = 2048

### Manages Base LLM functions ###
class LLM():
  def __init__(self,  opts) -> None:
    self.opts = {} if opts == None else opts
    self.model_key = opts.get("model_key", "base")
    self.gc_name = opts.get("generation_config", "llm/logical")
    
    # Loads the model configuration
    self.generation_config = Config(self.gc_name)
    self.model = None # default states
    self.tokenizer = None # default state
    self.device = opts.get("device", "cuda")

    # create a shared dictionary to store the model to be used by other workers
    logging.info(f"LLM CUDA enabled: {self.device == 'cuda' and torch.cuda.is_available()}")

    # Load LLM Model Manager
    self.llm = LLMModelManager()

  def configure(self, config) -> None:
    self.set_generation_config(config.get("generation_config", self.gc_name))
    self.set_max_new_tokens(config.get("max_new_tokens", DEFAULT_MAX_NEW_TOKENS))
    self.set_model_config(config.get("model_key", self.llm.key))

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

  def set_model_config(self, model_key):
    # grab the config
    if self.llm.key != model_key:
      self.llm.switch_model(model_key)

  # Get the name of the class
  def name(self):
    return self.__class__.__name__

  # Get status of the GPU
  def gpu(self) -> bool:
    return self.device == "cuda" and torch.cuda.is_available()

  # Loads the model and transfomer given the model name
  def load(self, model_key, **kwargs) -> None:
    self.llm.load_model(model_key)

  # Given a prompt, generates a response
  def generate(self, prompt: str, **kwargs) -> str:
    input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
    input_ids = input_ids.to('cuda') if self.gpu() else torch.device("cpu")
    response = self.model.generate(
        input_ids=input_ids,
        pad_token_id=self.tokenizer.eos_token_id,
        max_new_tokens=self.max_new_tokens,
        **self.config.to_dict()
    )
    self.result = self.tokenizer.decode(response[0])
    return {"response": self.result}