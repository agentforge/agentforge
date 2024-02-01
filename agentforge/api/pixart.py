from fastapi import Request
from pydantic import BaseModel
from typing import List
from agentforge.factories import resource_factory
from agentforge.api.app import init_api

image_gen = resource_factory.get_resource("image_gen")
app = init_api()

class VQARequest(BaseModel):
   url: str
   question: str

class TextResponse(BaseModel):
   text: str

# Test me: curl -X POST -d '{"prompt": "test"}' http://pixart:8000/v1/generate
@app.post("/v1/generate", operation_id="pixArtQuery")
async def generate_endpoint(request: Request):
    print("request")
    payload = await request.json()
    prompt = payload.get('prompt', '')
    response = await image_gen.generate(prompt)
    return TextResponse(text=response)
