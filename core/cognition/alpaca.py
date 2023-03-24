import torch
import time
from peft import PeftModel
from transformers import LlamaTokenizer, LlamaForCausalLM, GenerationConfig
from core.config.config import Config

from core.cognition.agent import Agent

class Alpaca(Agent):
  def __init__(self, opts={}) -> None:
    self.opts = opts
    self.config = Config("llm/" + self.opts["config"])
    super().__init__(opts)

  # Setup alpaca and load models
  def setup_alpaca(self):
    self.load_alpaca()

  def load_alpaca(self):
    self.tokenizer = LlamaTokenizer.from_pretrained(self.opts["model_name"])

    self.model = LlamaForCausalLM.from_pretrained(
      self.opts["model_name"],
      load_in_8bit=True,
      torch_dtype=torch.float16,
      device_map={'':0},
    )

    self.model = PeftModel.from_pretrained(
        self.model, self.opts["peft_model"], torch_dtype=torch.float16, device_map={'':0}
    )

  def generate(self, prompt, config=None):
     # grab the config
     if config != None and self.config.config_name != config:
        self.config = Config("llm/" + config)
     kwargs = self.config.to_dict()
     print(f"Rendering with {kwargs}")
     return self._generate(prompt, **kwargs)

  def _generate(
          self,
          instruct,
          **kwargs,
  ):
      prompt = self.instruct_prompt_w_memory(instruct)
      self.memory.chat_memory.add_user_message(instruct)
      inputs = self.tokenizer(prompt, return_tensors="pt")
      input_ids = inputs["input_ids"].cuda()
      generation_config = GenerationConfig(
          **kwargs,
      )
      # print(prompt)
      print("GENERATE...")
      start_time = time.time()
      with torch.no_grad():
          generation_output = self.model.generate(
              input_ids=input_ids,
              generation_config=generation_config,
              return_dict_in_generate=True,
              output_scores=True,
              max_new_tokens=2048,
          )
      end_time = time.time()
      execution_time = end_time - start_time
      print(f"Execution time: {execution_time:.6f} seconds")
      s = generation_output.sequences[0]
      output = self.tokenizer.decode(s)
      # print(output)
      out = self.parse(output)
      self.memory.chat_memory.add_ai_message(out.response)
      return out

