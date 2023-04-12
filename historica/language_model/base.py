### LLModel class ###
### RESTful API for the LLM services ###
### Maintains any necessary queue and rate limiting for ###
### accessing GPU/TPU resources ###

### Imports ###
import copy, json, gc
import torch
from historica.config import Config
import logging, time
from transformers import GenerationConfig, TextStreamer
from historica.language_model.generators import Generator
from accelerate import Accelerator
from historica.language_model.loaders import Loader
from historica.helpers import Parser

from historica import CONFIG_FILE

DEFAULT_LLM = 'dolly-v1-6b'

### Manages Base LLM functions ###
class LLM():
  def __init__(self,  opts) -> None:
    self.opts = {} if opts == None else opts
    self.model_key = opts.get("model_key", DEFAULT_LLM)
    self.gc_name = opts.get("generation_config", "llm/logical")
    self.multi_gpu=opts.get("multi_gpu", False)
    self.device_map=opts.get("device_map", "auto")

    with open(CONFIG_FILE, "r") as f:
        self._loaded_configs = json.load(f)

    self.config = self.load_config(DEFAULT_LLM)
    self.streaming = self.config.get("streaming", False)

    self.tokenizer = None
    self.model = None
    
    if self.multi_gpu:
        self.accelerator = Accelerator()
        self.device = self.accelerator.device
    else:
        self.device = "cuda"
    self.loader = Loader(self.device_map, self.multi_gpu, self.device)
    self.parser = Parser()

    # create a shared dictionary to store the model to be used by other workers
    logging.info(f"LLM CUDA enabled: {torch.cuda.is_available()}")

    self.generator = Generator(self.gc_name, self.multi_gpu)

  def configure(self, config) -> None:
    self.generator.set_generation_config(config.get("generation_config", self.gc_name))
    self.generator.set_max_new_tokens(config.get("max_new_tokens", 1024))
    self.load(config.get("model_key", self.model_key))

  # Get the name of the class
  def name(self):
    return self.__class__.__name__

  # Get status of the GPU
  def gpu(self) -> bool:
    return self.device == "cuda" and torch.cuda.is_available()

  # Loads the model and transfomer given the model name
  def load(self, model_key=None, **kwargs) -> None:

    if model_key == None:
      # If we aren't overriding use the default model
      model_key = self.model_key
    elif model_key is not None and model_key == self.model_key:
      # If we are already using this model, don't reload
      return  
    
    # Load the model
    self.switch_model(model_key)

    self.generator.set_models(self.model, self.tokenizer, TextStreamer(self.tokenizer))

  def generate(self, prompt, **kwargs):
    # setup the generator

    if "generator" in self.config:
        # Use custom generator based on function string
        function_name = self.config["generator"]
        function = getattr(self.generator, function_name)
        return function(
            prompt,
            self.loader.model, 
            self.loader.tokenizer,
            TextStreamer(self.tokenizer),
            **kwargs
        )
    # Use default generator
    output = self.generator.generate(
        prompt,
        self.loader.model, 
        self.loader.tokenizer,
        TextStreamer(self.tokenizer),
        **kwargs
    )
    return self.parser.parse_output(output)
            

  def load_model(self, model_key):
      # Check key and load logic according to key
      self.config = self.load_config(model_key)
      model, tokenizer = self.loader.load(self.config, device=self.device)
      self.model = model
      self.tokenizer = tokenizer
      self.model_key = model_key

  def unload_model(self):
      if self.tokenizer is not None:
          del self.tokenizer
          self.tokenizer = None

      if self.model is not None:
          if not self.multi_gpu:
              self.model = self.model.cpu()
          del self.model
          self.model = None

      gc.collect()
      torch.cuda.empty_cache()

  # Switches model to a new model
  def switch_model(self, key):
      if self.model_key != key:
          self.unload_model()
          self.load_model(key)
          self.model_key = key
  
  def load_config(self, key):
      if key not in self._loaded_configs:
          with open(CONFIG_FILE, "r") as f:
              configs = json.load(f)
          self._loaded_configs[key] = configs[key]

      return self._loaded_configs[key]
