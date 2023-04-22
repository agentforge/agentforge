import torch
import logging
from transformers import GenerationConfig

import logging.config
logging.config.fileConfig('../config/configs/logs/llm.conf')
logger = logging.getLogger('llm')

def convert_to_serializable(obj):
    if isinstance(obj, torch.Tensor):
        return obj.tolist()
    elif isinstance(obj, GenerationConfig):
        return obj.to_dict()
    key_err = f"""Object of type {obj.__class__.__name__} is not JSON serializable;
      Add a new Exception to convert_to_serializable() in historica/language_model/logger.py"""
    raise TypeError(key_err)
