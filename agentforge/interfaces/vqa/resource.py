### Imports ###
import gc, os
import torch
import logging
from dotenv import load_dotenv
import asyncio
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch, uuid

### Manages Base LLM functions ###
DST_PATH = os.getenv('DST_PATH', './')

class LocalVQA():
  def __init__(self) -> None:
    self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-VL-Chat-Int4", trust_remote_code=True)
    self.model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL-Chat-Int4", device_map="cuda", trust_remote_code=True).eval()
    self.device = "cuda"
    self.semaphore = asyncio.Semaphore(1)  # Allow only one request at a time

    # create a shared dictionary to store the model to be used by other workers
    logging.info(f"VQA CUDA enabled: {torch.cuda.is_available()}")

  async def generate(self, img_bytes: bytes, prompt="", **kwargs):
      async with self.semaphore:  # Acquire semaphore before proceeding
          # Generate a unique filename for the image
          img_filename = f"{DST_PATH}/{uuid.uuid4()}.jpg"
          # Save the image to disk
          with open(img_filename, 'wb') as img_file:
              img_file.write(img_bytes)
          try:
              # Adjust the query to use the local file path
              query = self.tokenizer.from_list_format([
                  {'image': img_filename},
                  {'text': prompt},
              ])
              response, history = self.model.chat(self.tokenizer, query=query, history=None)
              print(response)
          finally:
              # Ensure the image file is deleted
              if os.path.exists(img_filename):
                  os.remove(img_filename)
          return response
