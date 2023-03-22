import torch
import transformers
import time
from peft import PeftModel
from transformers import LlamaTokenizer, LlamaForCausalLM, GenerationConfig

from core.cognition.agent import Agent

from langchain import PromptTemplate, LLMChain
from core.cognition.base import LLM
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.llms import HuggingFaceModel

### Alpaca -- Stanford's davinci-003 model
AGENT_MODEL="decapoda-research/llama-7b-hf"
PEFT_MODEL="tloen/alpaca-lora-7b"

# AGENT_MODEL="decapoda-research/llama-13b-hf"
# PEFT_MODEL="mattreid/alpaca-lora-13b"

CONFIG_NAME="llm"

class Alpaca(Agent):
  def __init__(self, opts={}) -> None:
    if len(opts) == 0:
      opts = {"model_name": AGENT_MODEL, "config_name": CONFIG_NAME}
    super().__init__(opts)

  # Setup alpaca and load models
  def setup_alpaca(self):
    self.load_alpaca()

  def load_alpaca(self):
    self.tokenizer = LlamaTokenizer.from_pretrained(AGENT_MODEL)

    self.model = LlamaForCausalLM.from_pretrained(
      AGENT_MODEL,
      load_in_8bit=True,
      torch_dtype=torch.float16,
      device_map="auto",
    )

    self.model = PeftModel.from_pretrained(
        self.model, PEFT_MODEL, torch_dtype=torch.float16
    )

  def generate(
          self,
          instruct,
          temperature=0.88,
          top_p=0.75,
          top_k=64,
          repetition_penalty=1.2,
          no_repeat_ngram_size=3,
          do_sample=True,
          num_beams=4,
          **kwargs,
  ):
      prompt = self.instruct_prompt_w_memory(instruct)
      self.memory.chat_memory.add_user_message(instruct)
      inputs = self.tokenizer(prompt, return_tensors="pt")
      input_ids = inputs["input_ids"].cuda()
      generation_config = GenerationConfig(
          temperature=temperature,
          #top_p=top_p,
          top_k=top_k,
          do_sample=do_sample,
          no_repeat_ngram_size=no_repeat_ngram_size,
          repetition_penalty=repetition_penalty,
          renormalize_logits=True,
          num_beams=num_beams,
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

