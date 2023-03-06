### LLModel class ###
### RESTful API for the LLM services ###
### Maintains any necessary queue and rate limiting for ###
### accessing GPU/TPU resources ###

### Imports ###
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from agent_n.config import Config

### Class Definition ###
class LLM():
  def __init__(self, opts) -> None:
    self.opts = {} if opts == None else opts
    self.device = opts.get("device", "cuda")

  def gpu(self) -> bool:
    return self.device == "cuda" and torch.cuda.is_available()

  # Loads the model and transfomer given the model name
  def load(self, model_name, config_name, **kwargs) -> None:
    # Validate that both model_name and config_name exist
    if model_name == None or config_name == None:
      raise ValueError("model_name and config_name must be defined")

    # Loads the model configuration
    self.config = Config(config_name)

    # Sets the model revision and torch dtype
    revision = kwargs["opts"].get("revision", "float16")
    torch_dtype = kwargs["opts"].get("torch_dtype", torch.float16)

    args = {
      "revision": revision,
      "torch_dtype": torch_dtype,
    }

    # Given the model name, loads the requested revision model and transfomer
    self.model = AutoModelForCausalLM.from_pretrained(
      model_name,
      **args
    )

    self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Loads the model into GPU if available
    device = torch.device("cuda") if self.gpu() else torch.device("cpu")
    self.model = self.model.to(device)

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
    self.result = self.result.replace("\n", "<br>")
    # self.opts = opts
    # stop_words = ["Human:", "human:", "AI:", "Assistant:", "assistant:"]
    # self.result = self.llm_chain.predict(stop=stop_words, question=input_str)
    return {"response": self.result}