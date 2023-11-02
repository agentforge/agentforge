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

#model.generation_config = GenerationConfig.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)

#query = tokenizer.from_list_format([
#   {'image': 'https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg'},
#   {'text': 'What is this?'},
#])

@app.post("/v1/generate", operation_id="vqaQuery")
async def generate_endpoint(request: Request, img: UploadFile):
    payload = await request.json()
    img_bytes = await img.read()
    prompt = payload['prompt'] if 'prompt' in payload else ""

    try:
        response = await vqa.generate(img_bytes, prompt)

        # query = tokenizer.from_list_format([
        #     {'image': url},
        #     {'text': question},
        # ])
        # response, history = model.chat(tokenizer, query=query, history=None)

    except Exception as e:
        response = f"An error has occurred: {str(e)}"

    return TextResponse(text=response)