from fastapi import APIRouter, Request, Depends, status, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from agentforge.factories import resource_factory
from agentforge.api.app import init_api
from agentforge.utils import logger
from agentforge.ai.worldmodel.galaxy import Galaxy
import traceback

router = APIRouter()
galaxy = Galaxy()

class GalaxyResponse(BaseModel):
   systems: Dict

# Given the following text request generate a wav file and return to the client
@router.post("/generate-galaxy", operation_id="generateGalaxy")
async def output(request: Request) -> GalaxyResponse:
   # payload = await request.json()
   
   # Generate a galaxy and return the information
   response = await galaxy.generate()
   return GalaxyResponse(systems=response)