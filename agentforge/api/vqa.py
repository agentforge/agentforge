from fastapi import Request, Depends, status, HTTPException
from pydantic import BaseModel
from typing import List
from agentforge.factories import resource_factory
from agentforge.api.app import init_api
from agentforge.utils import logger
import traceback

from agentforge.interfaces.vqa.resource import LocalVQA

app = init_api()
#vqa = resource_factory.get_resource("vqa")
vqa = LocalVQA()

# Given the following text request generate a wav file and return to the client
@app.post("/v1/vqa", operation_id="vqa")
async def output(request: Request) -> CompletionsResponse:
   payload = await request.json()
   try:
      response = await vqa.generate(**payload)
   except:
      response = "An error has occurred. Please try again later."
      traceback.print_exc()
   return response