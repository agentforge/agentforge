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

@router.post("/generate-galaxy", operation_id="generateGalaxy")
async def output(request: Request) -> GalaxyResponse:
    # Access the database
    db = interface_interactor.get_interface("db")

    # Define collection and key for lookup
    collection = "galaxies"
    key = "milky_way" # TODO: Make this a parameter based on input data

    # Check if galaxy data already exists
    existing_data = db.get(collection, key)
    if existing_data:
         existing_data.pop('_id', None)  # Safely remove '_id' if it exists
         return GalaxyResponse(systems=existing_data)

    # If data doesn't exist, generate and save it
    response = await galaxy.generate(625)

    # Save generated data to the database
    db.create(collection, key, response)

    return GalaxyResponse(systems=response)