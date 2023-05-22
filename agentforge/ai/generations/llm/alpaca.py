import torch
import time
from transformers import  GenerationConfig
from . import LLM

MODEL_KEY="alpaca-lora-7b"

class Alpaca(LLM):
  def __init__(self, opts={}) -> None:
    self.opts = opts
    if len(opts) == 0:
      opts = {"model_key": MODEL_KEY }
    super().__init__(opts)
