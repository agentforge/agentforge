from fastapi import APIRouter, Request, UploadFile, Depends, status, HTTPException
from pydantic import BaseModel
from typing import List
from agentforge.factories import resource_factory
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
from agentforge.api.app import init_api

import traceback

vqa = resource_factory.get_resource("vqa")
app = init_api()
class VQARequest(BaseModel):
   url: str
   question: str

class TextResponse(BaseModel):
   text: str

@app.post("/v1/generate", operation_id="vqaQuery")
async def generate_endpoint(request: Request, img: UploadFile):
    payload = await request.json()
    img_bytes = await img.read()
    prompt = payload['prompt'] if 'prompt' in payload else ""

    try:
        response = await vqa.generate(img_bytes, prompt)

    except Exception as e:
        response = f"An error has occurred: {str(e)}"

    return TextResponse(text=response)