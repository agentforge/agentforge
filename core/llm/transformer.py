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
import pickle

### Class Definition ###
class LLM():
  def __init__(self,  opts) -> None:
    self.opts = {} if opts == None else opts
    self.model_name = opts.get("model_name", "gpt2")
    self.config_name = opts.get("config_name", "llm.json")
    self.model = None # default states
    self.tokenizer = None # default state
    self.device = opts.get("device", "cuda")
    # create a shared dictionary to store the model to be used by other workers
    self.manager = Manager()
    self.shared_dict = self.manager.dict()
    logging.info("LLM CUDA enabled: ", self.device == "cuda" and torch.cuda.is_available())

  def gpu(self) -> bool:
    return self.device == "cuda" and torch.cuda.is_available()

  # Loads the model and transfomer given the model name
  def load(self, **kwargs) -> None:
    # get opts if it is available
    opts = kwargs.get("opts", self.opts)
    # Check shared dict to see if model_name has been loaded, if we haven't already
    if self.get_model() is not None and self.get_tokenizer() is not None:
      if self.model is None:
        self.model = self.get_model()
      if self.tokenizer is None:
        self.tokenizer = self.get_tokenizer()

    # Validate that both model_name and config_name exist
    if self.model_name == None or self.config_name == None:
      raise ValueError("model_name and config_name must be defined")

    # Loads the model configuration
    self.config = Config(self.config_name)

    # Sets the model revision and torch dtype
    revision = opts.get("revision", "float16")
    torch_dtype = opts.get("torch_dtype", torch.float16)

    # Given the model name, loads the requested revision model and transfomer
    self.model = AutoModelForCausalLM.from_pretrained(
      self.model_name,
      revision = revision,
      torch_dtype = torch_dtype,
    )

    self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    # Loads the model into GPU if available
    device = torch.device("cuda") if self.gpu() else torch.device("cpu")
    self.model = self.model.to(device)

    # Store model reference in shared dict if necessary
    self.fanout()

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