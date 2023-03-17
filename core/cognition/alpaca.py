import torch
import transformers
from peft import PeftModel
from transformers import LlamaTokenizer, LlamaForCausalLM, GenerationConfig

from langchain import PromptTemplate, LLMChain
from core.cognition.base import LLM
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.llms import HuggingFaceModel

### Alpaca -- Stanford's davinci-003 model
AGENT_MODEL="decapoda-research/llama-7b-hf"
CONFIG_NAME="llm"

class Alpaca(LLM):
  def __init__(self) -> None:
    super().__init__({"model_name": AGENT_MODEL, "config_name": CONFIG_NAME})
    self.setup()

  # Setup Agent and load models
  def setup(self):
    self.load()

  def load(self):
    self.tokenizer = LlamaTokenizer.from_pretrained("decapoda-research/llama-7b-hf")

    self.model = LlamaForCausalLM.from_pretrained(
      "decapoda-research/llama-7b-hf",
      load_in_8bit=True,
      torch_dtype=torch.float16,
      device_map="auto",
    )

    self.model = PeftModel.from_pretrained(
        self.model, "tloen/alpaca-lora-7b", torch_dtype=torch.float16
    )

  def generate_prompt(self, instruction):
    return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.
      ### Instruction:
      {instruction}
      ### Response:"""


  def generate(
          self,
          instruction,
          temperature=0.1,
          top_p=0.75,
          top_k=40,
          num_beams=4,
          **kwargs,
  ):
      prompt = self.generate_prompt(instruction)
      inputs = self.tokenizer(prompt, return_tensors="pt")
      input_ids = inputs["input_ids"].cuda()
      generation_config = GenerationConfig(
          temperature=temperature,
          top_p=top_p,
          top_k=top_k,
          num_beams=num_beams,
          **kwargs,
      )
      print("GENERATE...")
      with torch.no_grad():
          generation_output = self.model.generate(
              input_ids=input_ids,
              generation_config=generation_config,
              return_dict_in_generate=True,
              output_scores=True,
              max_new_tokens=2048,
          )
      print("GENERATED...")
      s = generation_output.sequences[0]
      output = self.tokenizer.decode(s)
      return output.split("### Response:")[1].strip()

