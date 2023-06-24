from fastapi import Request, Depends, status, HTTPException
from pydantic import BaseModel
from typing import List
from agentforge.factories import resource_factory
from agentforge.api.app import init_api
from agentforge.utils import logger
import traceback

app = init_api()
llm = resource_factory.get_resource("llm")

class TextResponse(BaseModel):
   text: str

class CompletionsResponse(BaseModel):
   choices: List[TextResponse]

# Given the following text request generate a wav file and return to the client
@app.post("/v1/completions", operation_id="createLanguageModelCompletion")
async def output(request: Request) -> CompletionsResponse:
   payload = await request.json()
   try:
      response = await llm.generate(**payload)
   except:
      response = "An error has occurred. Please try again later."
      traceback.print_exc()
   return CompletionsResponse(choices=[TextResponse(text=response)])