### LLModel class ###
### RESTful API for the LLM services ###
### Maintains any necessary queue and rate limiting for ###
### accessing GPU/TPU resources ###

### Imports ###
import torch
from core.config.config import Config
import logging
from core.cognition.prompt import Prompt
from core.cognition.manager import LLMModelManager
from langchain.chains.conversation.memory import ConversationBufferMemory


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

    # Load memory, prompt, and LLM Model Manager
    self.memory = ConversationBufferMemory(return_messages=True)
    self.prompt_manager = Prompt(self.memory)
    self.llm = LLMModelManager()

  def configure(self, config) -> None:
    self.set_generation_config(config.get("generation_config", self.gc_name))
    self.set_model_config(config.get("model_key", self.llm.key))

  def set_generation_config(self, generation_config):
    # grab the config
    if self.gc_name != generation_config:
      self.generation_config = Config("llm/" + generation_config)
      self.gc_name = generation_config

  def set_model_config(self, model_key):
    # grab the config
    if self.llm.key != model_key:
      self.llm.switch_model(model_key)

  # Get the prompt based on the current model key
  def get_prompt(self, **kwargs):
    # If memory is an argument let's extract relevant information from it
    return self.prompt_manager.get_prompt(self.llm.config["prompt_type"], **kwargs)

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
        **self.config.to_dict()
    )
    self.result = self.tokenizer.decode(response[0])
    return {"response": self.result}