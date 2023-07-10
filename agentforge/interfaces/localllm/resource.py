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
from agentforge.interfaces.localllm.lib.text_streamer import TextStreamer
from dotenv import load_dotenv

### Manages Base LLM functions ###
class LocalLLM():
  def __init__(self,  config: dict = None) -> None:
    self.config = {} if config == None else config
    self.model_key = self.config['model_config']['model_name'] if 'model_config' in self.config else None
    self.multi_gpu = False # TODO: Reenable

    self.tokenizer = None
    self.model = None
    
    if self.multi_gpu:
        self.accelerator = Accelerator()
        self.device = self.accelerator.device
    else:
        self.device = "cuda"

    # create a shared dictionary to store the model to be used by other workers
    logging.info(f"LLM CUDA enabled: {torch.cuda.is_available()}")

    if self.model_key:
        self.setup(self.config, init=True)
        self.load_model(self.config)

  def setup(self, config: dict, init: bool = False):
    if config['model_config']['model_name'] != self.model_key or init:
      self.parser = Parser()
      self.loader = LocalLoader(config['model_config'])
      self.generator = LocalGenerator(config)

  # Get the name of the class
  def name(self):
    return self.__class__.__name__

  # Get status of the GPU
  def gpu(self) -> bool:
    return self.device == "cuda" and torch.cuda.is_available()

  # Loads the model and transfomer given the model name
  def load(self, model_key=None, **kwargs) -> None:
    print(model_key)
    if model_key == None:
      # If we aren't overriding use the default model
      model_key = self.model_key
    elif model_key is not None and model_key == self.model_key:
      # If we are already using this model, don't reload
      return
    # Load the model
    print(model_key)
    self.switch_model(model_key, kwargs)
    print('generator')

    self.generator.set_models(self.model, self.tokenizer, self.text_streamer(False))
    print('done')

  # Setup and return the text streamer
  def text_streamer(self, streaming):
    if streaming == False:
      return None
    return TextStreamer(self.tokenizer, skip_prompt=True)

  async def generate(self, prompt="", **kwargs):
    # setup the generator
    config = kwargs['generation_config']
    streaming = True if "streaming" in kwargs['model_config'] and kwargs['model_config']["streaming"] else False
    print(streaming)
    self.setup(kwargs)
    print('load')
    self.load(model_key=kwargs['model_config'].get("model_name", self.model_key), **kwargs)
    kwargs.update(config)

    if "generator" in kwargs:
        # Use custom generator based on function string
        function_name = kwargs["generator"]
        function = getattr(self.generator, function_name)
        return function(
            prompt,
            self.loader.model, 
            self.loader.tokenizer,
            self.text_streamer(streaming),
            **kwargs
        )
    # Use default generator
    output = self.generator.generate(
        prompt,
        self.loader.model,
        self.loader.tokenizer,
        self.text_streamer(streaming),
        **kwargs
    )
    return output

  def load_model(self, config):
    # Check key and load logic according to key
    # self.config = self.config_controller.get_config(model_key)
    model, tokenizer = self.loader.load(config['model_config'], device=self.device)
    self.model = model
    self.tokenizer = tokenizer
    self.model_key = config['model_config']['model_name']

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
  def switch_model(self, key, config):
    if self.model_key != key:
      self.unload_model()
      self.load_model(config)
      self.model_key = key
