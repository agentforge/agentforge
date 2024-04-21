import os
from fastapi import UploadFile, HTTPException
from typing import Dict, Any
from pydantic import BaseModel
from agentforge.utils import async_execution_decorator
from agentforge.interfaces.api import VQAService
from agentforge.utils import logger
from agentforge.ai.agents.context import Context

class ImageProcessor:
    def __init__(self):
        self.vqa_service = VQAService()

    def execute(self, context: Context) -> Dict[str, Any]:        
        messages = context.get('input.messages')
        if messages is None:
            return context

        if not 'img' in messages[-1] or messages[-1]['img'] is None:
            return context

        img_bytes = messages[-1]['img']
        prompt = messages[-1]['content']
        try:
            response_data = self.vqa_service.process(prompt, img_bytes)
        except HTTPException as e:
            raise e  # Re-raise the exception

        text_response = response_data.get('text')
        if text_response is None:
            raise HTTPException(status_code=500, detail="Unexpected response format from VQA service")
        context.set('image_response', text_response)  # Set the response in the context
        return context
