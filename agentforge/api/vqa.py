from fastapi import Request, Depends, status, HTTPException
from pydantic import BaseModel
from typing import List
from agentforge.factories import resource_factory
from agentforge.api.app import init_api

from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig

import traceback


app = init_api()
#vqa = resource_factory.get_resource("vqa")

class VQARequest(BaseModel):
   url: str
   question: str

class TextResponse(BaseModel):
   text: str

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-VL-Chat-Int4", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL-Chat-Int4", device_map="cuda", trust_remote_code=True).eval()
#model.generation_config = GenerationConfig.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)

#query = tokenizer.from_list_format([
#   {'image': 'https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg'},
#   {'text': 'What is this?'},
#])

# Given the following text request generate a wav file and return to the client
@app.post("/v1/vqa", operation_id="vqaQuery")
async def output(request: Request) -> TextResponse:
    payload = await request.json()
    
    if 'url' in payload and 'question' in payload:
        url = payload['url']
        question = payload['question']
        try:
            query = tokenizer.from_list_format([
                {'image': url},
                {'text': question},
            ])
            response, history = model.chat(tokenizer, query=query, history=None)
        except Exception as e:
            response = f"An error has occurred: {str(e)}"
    else:
        response = "Invalid payload format. Make sure 'url' and 'question' are provided."

    return TextResponse(text=response)