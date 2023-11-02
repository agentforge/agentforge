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
        if not context.has_key('input.img'):
            return context

        img = context.get('input.img')
        prompt = context.get('input.prompt')
        img_bytes = img.file.read()  # Synchronous read

        try:
            response_data = self.vqa_service.process(prompt, img_bytes)
        except HTTPException as e:
            raise e  # Re-raise the exception

        text_response = response_data.get('text')
        if text_response is None:
            raise HTTPException(status_code=500, detail="Unexpected response format from VQA service")

        context.set('response', text_response)  # Set the response in the context
        return context
