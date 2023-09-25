### Imports ###
import gc, os
import torch
from agentforge.config import Config
import logging
from dotenv import load_dotenv

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
#torch.manual_seed(1234)

### Manages Base LLM functions ###
class LocalVQA():
  def __init__(self,  config: dict = None) -> None:
    self.config = {} if config == None else config
    self.model_key = self.config['model_config']['model_name'] if 'model_config' in self.config else None
    self.multi_gpu = False # TODO: Reenable

    self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-VL-Chat-Int4", trust_remote_code=True)
    self.model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL-Chat-Int4", device_map="cuda", trust_remote_code=True).eval()
    self.device = "cuda"

    # create a shared dictionary to store the model to be used by other workers
    logging.info(f"VQA CUDA enabled: {torch.cuda.is_available()}")

  async def generate(self, prompt="", **kwargs):
    query = tokenizer.from_list_format([
    {'image': 'https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg'},
    {'text': 'What is this?'},
    ])
    response, history = model.chat(tokenizer, query=query, history=None)
    print(response)
    return response
