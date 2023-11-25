from fastapi import APIRouter, Request, UploadFile, Depends, status, HTTPException
from pydantic import BaseModel
from typing import List
from agentforge.factories import resource_factory
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
from agentforge.api.app import init_api
import base64
import traceback

vqa = resource_factory.get_resource("vqa")
app = init_api()
class VQARequest(BaseModel):
   url: str
   question: str

class TextResponse(BaseModel):
   text: str

@app.post("/v1/generate", operation_id="vqaQuery")
async def generate_endpoint(request: Request):
    try:
        payload = await request.json()
        img_data = payload.get('img', '')
        prompt = payload.get('prompt', '')

        if img_data:
            img_base64 = img_data.split(",")[-1]
            img_bytes = base64.b64decode(img_base64)
            response = await vqa.generate(img_bytes, prompt)
        else:
            response = "No 'img' field found in the message."

    except Exception as e:
        response = f"An error has occurred: {str(e)}"
        print(traceback.format_exc())
    return TextResponse(text=response)
