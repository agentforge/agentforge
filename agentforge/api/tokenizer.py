from fastapi import Request, Depends, status, HTTPException
from pydantic import BaseModel
from typing import List
from agentforge.factories import resource_factory
from agentforge.api.app import init_api
from agentforge.utils import logger
import traceback
from transformers import AutoTokenizer

app = init_api()
tokenizer = AutoTokenizer.from_pretrained("uukuguy/speechless-llama2-luban-orca-platypus-13b")

class TextResponse(BaseModel):
   text: str

# Given the following text request generate a wav file and return to the client
@app.post("/v1/tokenizer", operation_id="getTokenizerCount")
async def output(request: Request) -> TextResponse:
   payload = await request.json()
   try:
      response = len(tokenizer.encode(**payload['prompt']))
   except:
      response = "An error has occurred. Please try again later."
      traceback.print_exc()
   return TextResponse(text=response)