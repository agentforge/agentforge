from fastapi import Request, Depends, status, HTTPException
from pydantic import BaseModel
from typing import List
from agentforge.factories import resource_factory
from agentforge.api.app import init_api
from agentforge.utils import logger
from starlette.responses import JSONResponse

app = init_api()
llm = resource_factory.get_resource("llm")

class TextResponse(BaseModel):
   text: str

class CompletionsResponse(BaseModel):
   choices: List[TextResponse]

# Given the following text request generate a wav file and return to the client
@app.post("/v1/completions", operation_id="createLanguageModelCompletion")
async def output(request: Request) -> CompletionsResponse:
   print(request)
   response = ""
   payload = await request.json()
   print(payload)
   response = llm.generate(**payload)
   # pass
   print(response)
   return CompletionsResponse(choices=[TextResponse(text=response)])