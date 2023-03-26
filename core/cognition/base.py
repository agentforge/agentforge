### LLModel class ###
### RESTful API for the LLM services ###
### Maintains any necessary queue and rate limiting for ###
### accessing GPU/TPU resources ###

### Imports ###
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from core.config.config import Config
import logging
from torch.multiprocessing import Manager, Process
from core.cognition.prompt import Prompt
from core.cognition.manager import LLMModelManager
from langchain.chains.conversation.memory import ConversationBufferMemory


### Manages Base LLM functions ###
class LLM():
  def __init__(self,  opts) -> None:
    self.opts = {} if opts == None else opts
    self.model_name = opts.get("model_name", "gpt2")
    self.config_name = opts.get("config_name", "llm/logical")
    
    # Loads the model configuration
    self.config = Config(self.config_name)
    self.model = None # default states
    self.tokenizer = None # default state
    self.device = opts.get("device", "cuda")

    # create a shared dictionary to store the model to be used by other workers
    self.manager = Manager()
    self.shared_dict = self.manager.dict()
    logging.info(f"LLM CUDA enabled: {self.device == 'cuda' and torch.cuda.is_available()}")

    # Load memory, prompt, and LLM Model Manager
    self.memory = ConversationBufferMemory(return_messages=True)
    self.prompt_manager = Prompt(self.memory)
    self.llm_manager = LLMModelManager(self.config)

  # Get the prompt based on the current model key
  def get_prompt(self, **kwargs):
    # If memory is an argument let's extract relevant information from it
    prompt_func = self.prompt_manager.get_prompt(self.llm_manager.key)
    return prompt_func(**kwargs)

  # Get the name of the class
  def name(self):
    return self.__class__.__name__

  # Get status of the GPU
  def gpu(self) -> bool:
    return self.device == "cuda" and torch.cuda.is_available()

  # Loads the model and transfomer given the model name
  def load(self, **kwargs) -> None:
    # get opts if it is available
    opts = kwargs.get("opts", self.opts)
    

  def tokenizer_key(self):
    return f"{self.model_name}-tokenizer"

  def model_key(self):
    return f"{self.model_name}-model"

  # Gets the model
  def get_tokenizer(self):
    return self.shared_dict[self.tokenizer_key()] if self.tokenizer_key() in self.shared_dict else None

  # Gets the model
  def get_model(self):
    return self.shared_dict[self.model_key()] if self.model_key() in self.shared_dict else None

  ### Inits the model pointer in a shared dict for other torch processes that have access to this GPU ###
  def fanout(self) -> None:

    # async function to store the model in the shared dict
    def store_model(shared_dict, model, tokenizer, m_key, t_key):
      if m_key not in shared_dict:
        # create the model and store it in the shared 
        shared_dict[m_key] = model
      if t_key not in shared_dict:
        shared_dict[t_key] = tokenizer

    p_args = (self.shared_dict,self.model, self.tokenizer, self.model_key(), self.tokenizer_key(),)

    # start a separate process to create and store the model
    p = Process(target=store_model, args=p_args)
    p.start()

    # wait for the process to finish
    p.join()

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