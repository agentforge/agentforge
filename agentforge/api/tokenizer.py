from fastapi import Request, Depends, status, HTTPException
from pydantic import BaseModel
from typing import List
from agentforge.factories import resource_factory
from agentforge.api.app import init_api
from agentforge.utils import logger
import traceback
from transformers import AutoTokenizer
import threading

app = init_api()
tokenizer = AutoTokenizer.from_pretrained("uukuguy/speechless-llama2-luban-orca-platypus-13b")
tokenizer_lock = threading.Lock()

class TextResponse(BaseModel):
   text: str

@app.post("/v1/tokenizer", operation_id="getTokenizerCount")
async def output(request: Request) -> TextResponse:
   payload = await request.json()
   try:
      with tokenizer_lock:
         response = len(tokenizer.encode(payload['prompt']))
   except:
      response = "An error has occurred. Please try again later."
      traceback.print_exc()
   return TextResponse(text=response)
