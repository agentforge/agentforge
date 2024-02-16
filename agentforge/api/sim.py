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

class GalaxyResponse(BaseModel):
   systems: Dict


### Generates a galaxy and saves it to the database
### If the galaxy already exists, it will be returned
### @param key: The key to store the galaxy under
### @param num_systems: The number of systems to generate
### @param anim_steps: The number of animation steps to generate
### @param recreate: Whether to recreate the galaxy if it already exists
### @return: The generated galaxy
async def get_galaxy(
        key: str,
        num_systems: int,
        anim_steps: int = 100,
        recreate: bool = False
    ):
    response = {}
    BATCH_SIZE = 50
    galaxy = Galaxy(
        config={
            "NUM_SYSTEMS": num_systems,
            "ANIM_STEPS": anim_steps,
        }
    )
    db = interface_interactor.get_interface("db")
    galaxies_collection = "galaxies"
    systems_collection = "solar_systems"
    planets_collection = "planets"

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
    response = await galaxy.generate_with_life()

    # Split and store systems in separate collections
    systems = response.pop('systems', [])
    print(len(systems))
    has_life = response.pop('has_life', [])
    planet_queue = []

    for system in systems:
        if 'Planets' not in system:
            continue
        for planet in system['Planets']:
            planet['system_id'] = system['uuid']
            system['galaxy_key'] = key
            planet_queue.append(planet)
        system.pop('Planets')

    planet_slices = [planet_queue[i:i + BATCH_SIZE] for i in range(0, len(planet_queue), BATCH_SIZE)]
    for i, slice in enumerate(planet_slices):
        db.batch_upload(planets_collection, slice)
    system_slices = [systems[i:i + BATCH_SIZE] for i in range(0, len(systems), BATCH_SIZE)]
    sector_keys = []

    for i, slice in enumerate(system_slices):
        sector_key = f"sector{i:0>{3}}" # creates a fixed length string with leading zeros
        for system in slice:
            system['sector_key'] = sector_key
            system['galaxy_key'] = key

        db.batch_upload(systems_collection, slice)
        sector_keys.append(sector_key)

    # Store the rest of the galaxy data with references to the systems
    galaxy_data = {**response, 'sector_keys': sector_keys}
    db.create(galaxies_collection, key, galaxy_data)

    response['systems'] = systems  # Re-add systems for the response
    response.pop('_id', None)
    return GalaxyResponse(systems=response)

@router.post("/generate-galaxy", operation_id="generateGalaxy")
async def output() -> GalaxyResponse:
   response = await get_galaxy("milky_way", 625)
   return GalaxyResponse(systems=response)