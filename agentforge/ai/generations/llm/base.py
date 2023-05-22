### LLModel class ###
### RESTful API for the LLM services ###
### Maintains any necessary queue and rate limiting for ###
### accessing GPU/TPU resources ###

### Imports ###
import copy, json, gc
import torch
from agentforge.config import Config
import logging, time
from transformers import GenerationConfig
from agentforge.language_model.generators import Generator
from accelerate import Accelerator
from agentforge.language_model.loaders import Loader
from agentforge.helpers import Parser
from .text_streamer import TextStreamer
from agentforge import LLM_CONFIG_FILE
DEFAULT_LLM = 'alpaca-lora-7b'

### Manages Base LLM functions ###
class LLM():
  def __init__(self,  opts) -> None:
    self.opts = {} if opts == None else opts
    self.model_key = opts.get("model_key", DEFAULT_LLM)
    self.gc_name = opts.get("generation_config", "llm/logical")
    self.multi_gpu=opts.get("multi_gpu", False)
    self.device_map=opts.get("device_map", "auto")

    self.config_controller = Config(None)

    # Load the default model's config
    # self.config_controller.load_config(LLM_CONFIG_FILE)
    self.config = self.config_controller.get_config(DEFAULT_LLM)
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
    config = self.generator.prep_generation_config(kwargs.get("generation_config", "logical"))
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
            self.text_streamer(kwargs["streaming"]),
            **kwargs
        )
    # Use default generator
    output = self.generator.generate(
        prompt,
        self.loader.model,
        self.loader.tokenizer,
        self.text_streamer(kwargs["streaming"]),
        **kwargs
    )
    return self.parser.parse_output(output)

  def load_model(self, model_key):
      # Check key and load logic according to key
      self.config = self.config_controller.get_config(model_key)
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
