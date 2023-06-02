### LLModel class ###
### RESTful API for the LLM services ###
### Maintains any necessary queue and rate limiting for ###
### accessing GPU/TPU resources ###

### Imports ###
import gc, os
import torch
from agentforge.config import Config
import logging
from .generator import LocalGenerator
from .loader import LocalLoader
from accelerate import Accelerator
from agentforge.utils import Parser
from .lib.text_streamer import TextStreamer
from agentforge import LLM_CONFIG_FILE
from dotenv import load_dotenv

### Manages Base LLM functions ###
class LocalLLM():
  def __init__(self,  config: dict = None) -> None:
    self.config = {} if config == None else config
    self.streaming = self.config['avatar_config'].get("streaming", False)
    self.model_key = self.config['model_config']['model_name']
    self.multi_gpu = False # TODO: Reenable

    self.tokenizer = None
    self.model = None
    
    if self.multi_gpu:
        self.accelerator = Accelerator()
        self.device = self.accelerator.device
    else:
        self.device = "cuda"

    self.loader = LocalLoader(self.config['model_config'])
    self.parser = Parser()

    # create a shared dictionary to store the model to be used by other workers
    logging.info(f"LLM CUDA enabled: {torch.cuda.is_available()}")

    self.generator = LocalGenerator(self.config)
    self.load_model(self.model_key)

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

    self.generator.set_models(self.model, self.tokenizer, self.text_streamer(False))

  # Setup and return the text streamer
  def text_streamer(self, streaming):
    if streaming == False:
      return None
    return TextStreamer(self.tokenizer, skip_prompt=True)

  def generate(self, prompt="", **kwargs):
    # setup the generator
    config = kwargs
    self.load(kwargs.get("model_key", self.model_key))
    kwargs.update(config)
    if "generator" in self.config:
        # Use custom generator based on function string
        function_name = self.config["generator"]
        function = getattr(self.generator, function_name)
        return function(
            prompt,
            self.loader.model, 
            self.loader.tokenizer,
            self.text_streamer(kwargs['model_config']["streaming"]),
            **kwargs
        )
    # Use default generator
    output = self.generator.generate(
        prompt,
        self.loader.model,
        self.loader.tokenizer,
        self.text_streamer(kwargs['model_config']["streaming"]),
        **kwargs
    )
    return self.parser.parse_output(output)

  def load_model(self, model_key):
      # Check key and load logic according to key
      # self.config = self.config_controller.get_config(model_key)
      model, tokenizer = self.loader.load(self.config['model_config'], device=self.device)
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
