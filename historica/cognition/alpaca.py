import torch
import time
from peft import PeftModel
from transformers import LlamaTokenizer, LlamaForCausalLM, GenerationConfig, TextStreamer
from core.config.config import Config

from core.cognition.base import LLM

MODEL_KEY="alpaca-lora-7b"

class Alpaca(LLM):
  def __init__(self, opts={}) -> None:
    self.opts = opts
    if len(opts) == 0:
      opts = {"model_key": MODEL_KEY }
    super().__init__(opts)
    self.setup_alpaca()

  # Setup alpaca and load models
  def setup_alpaca(self):
    self.llm.load_model(self.model_key)
    self.streamer = TextStreamer(self.llm.tokenizer)

  def generate(self, prompt, gc_name=None):
    if gc_name is not None:
      self.set_generation_config(gc_name)
    kwargs = self.generation_config.to_dict()
    print(f"Rendering with {kwargs}")
    return self._generate(prompt, **kwargs)
  
  def _generate(
          self,
          instruct,
          **kwargs,
  ):
      print(instruct)
      inputs = self.llm.tokenizer(instruct, return_tensors="pt")
      input_ids = inputs["input_ids"].cuda()
      generation_config = GenerationConfig(
          **kwargs,
      )
      # print(prompt)
      print("GENERATE...")
      start_time = time.time()
      with torch.no_grad():
          generation_output = self.llm.model.generate(
              input_ids=input_ids,
              generation_config=generation_config,
              return_dict_in_generate=True,
              output_scores=True,
              max_new_tokens=self.max_new_tokens,
              streamer=self.streamer,
          )
      end_time = time.time()
      execution_time = end_time - start_time
      print(f"Execution time: {execution_time:.6f} seconds")
      s = generation_output.sequences[0]
      output = self.llm.tokenizer.decode(s)
      output = self.parse(output)
      # print(output)
      return output

  # Returns and AgentResponse object that 
  def parse(self, output):
    responses = output.split("### Response:")
    candidate = responses[len(responses)-1].strip()
    # candidate = helpers.process_code_output(candidate)
    candidate = candidate.lstrip('\n')
    return candidate