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

async def get_galaxy(key: str, num_systems: int):
    systems_per_slice = 500
    db = interface_interactor.get_interface("db")
    galaxies_collection = "galaxies"
    systems_collection = "solar_systems"

    # Check if galaxy data exists
    existing_data = db.get(galaxies_collection, key)
    if existing_data:
        existing_data.pop('_id', None)
        # Reassemble systems from slices stored in separate collections
        all_systems = []
        for system_key in existing_data.get('system_keys', []):
            systems_data = db.get(systems_collection, system_key)
            if systems_data:
                systems_data.pop('_id', None)
                all_systems.extend(systems_data.get('systems', []))

        existing_data['systems'] = all_systems
        logger.info(existing_data)
        return GalaxyResponse(systems=existing_data)

    # Generate new galaxy data
    response = await galaxy.generate_with_life(num_systems)

    # Split and store systems in separate collections
    systems = response.pop('systems', [])
    system_slices = [systems[i:i + systems_per_slice] for i in range(0, len(systems), systems_per_slice)]
    system_keys = []

    for i, slice in enumerate(system_slices):
        system_key = f"{key}_systems_{i}"
        db.create(systems_collection, system_key, {'systems': slice})
        system_keys.append(system_key)

    # Store the rest of the galaxy data with references to the systems
    galaxy_data = {**response, 'system_keys': system_keys}
    db.create(galaxies_collection, key, galaxy_data)

    response['systems'] = systems  # Re-add systems for the response
    response.pop('_id', None)
    return GalaxyResponse(systems=response)

@router.post("/generate-galaxy", operation_id="generateGalaxy")
async def output() -> GalaxyResponse:
   response = await get_galaxy("milky_way", 625)
   return GalaxyResponse(systems=response)