from fastapi import Request
from pydantic import BaseModel
from typing import List
from agentforge.utils import measure_time, comprehensive_error_handler
from agentforge.factories import resource_factory
from .app import init_api

app = init_api()
llm = resource_factory.get_resource("llm")

class TextResponse(BaseModel):
   text: str

class CompletionsResponse(BaseModel):
   choices: List[TextResponse]

# Given the following text request generate a wav file and return to the client
@app.post("/v1/completions")
@comprehensive_error_handler

@measure_time
def output(request: Request) -> CompletionsResponse:
  config = request.json
  response = llm.generate(**config)
  return CompletionsResponse(text=TextResponse(choices=response))

