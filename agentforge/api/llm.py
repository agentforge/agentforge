from fastapi import Request, Depends
from pydantic import BaseModel
from typing import List
from agentforge.factories import resource_factory
from agentforge.api.app import init_api

app = init_api()
llm = resource_factory.get_resource("llm")

class TextResponse(BaseModel):
   text: str

class CompletionsResponse(BaseModel):
   choices: List[TextResponse]

# Given the following text request generate a wav file and return to the client
@app.post("/v1/completions", operation_id="createLanguageModelCompletion")
def output(request: Request) -> CompletionsResponse:
  config = request.json
  response = llm.generate(**config)
  return CompletionsResponse(text=TextResponse(choices=response))

