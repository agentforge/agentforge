from fastapi import APIRouter, Request, Depends, status, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from agentforge.factories import resource_factory
from agentforge.api.app import init_api
from agentforge.utils import logger
from agentforge.ai.worldmodel.galaxy import Galaxy
from agentforge.interfaces import interface_interactor
import traceback

router = APIRouter()
galaxy = Galaxy()

class GalaxyResponse(BaseModel):
   systems: Dict

response = {}

# Modify the get_galaxy function to accept parameters
async def get_galaxy(key: str, num_systems: int):
   db = interface_interactor.get_interface("db")
   collection = "galaxies"

   existing_data = db.get(collection, key)
   if existing_data:
      existing_data.pop('_id', None)
      logger.info(existing_data)
      return GalaxyResponse(systems=existing_data)

   response = await galaxy.generate_with_life(num_systems)
   db.create(collection, key, response)

   response.pop('_id', None)
   return response

@router.post("/generate-galaxy", operation_id="generateGalaxy")
async def output() -> GalaxyResponse:
   response = await get_galaxy("milky_way", 625)
   return GalaxyResponse(systems=response)