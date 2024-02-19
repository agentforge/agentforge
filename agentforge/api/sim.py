import os
from fastapi import APIRouter, Request, Depends, status, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from agentforge.factories import resource_factory
from agentforge.api.app import init_api
from agentforge.utils import logger
from agentforge.ai.worldmodel.galaxy import Galaxy
from agentforge.ai.worldmodel.biome import Biome
from agentforge.ai.worldmodel.species import Species
from agentforge.ai.worldmodel.probability import UniverseProbability
from agentforge.ai.worldmodel.evolution import EvolutionarySimulation
from agentforge.ai.worldmodel.civilization import Civilization
from agentforge.interfaces import interface_interactor
import traceback
from celery import Celery

class GalaxyResponse(BaseModel):
   systems: Dict

router = APIRouter()
db_uri = os.getenv("MONGODB_URI")

# Initialize a Celery instance - adjust broker URL as needed
app = Celery(
    'evolution',
    broker=db_uri,
    backend=db_uri,
)

def analyze_biome_species(biomes, db):
    max_score = 0
    apex_species = None
    highest_evolutionary_level = 0
    for biome in biomes.values():
        if 'apex_species' not in biome or biome['apex_species'] is None:
            continue
        species = Species.load(db, 'species', biome['apex_species']['id'], load_individuals=False)
        if species.evolutionary_stage >= highest_evolutionary_level:
            highest_evolutionary_level = species.evolutionary_stage
            high_score = biome['apex_species']['score']
            if high_score > max_score:
                max_score = high_score
                apex_species = species
    return apex_species


@app.task
def evolve_society():
    db = interface_interactor.get_interface("db")
    planet = db.get_one("planets", {"evolution_complete": True, "civilization": {"$exists": False}, "civilization_emerging": {"$exists": False}})
    if planet:
        planet["civilization_emerging"] = True
        db.set("planets", planet["id"], planet)
        print(f"Getting species for planet {planet['id']}")
        apex_species = analyze_biome_species(planet["Biomes"], db)
        # for _, s in enumerate(species_cursor):
        #     species_objs.append(Species.load_from_object(db, 'species', s))
        # apex_species = EvolutionarySimulation.identify_apex_species(species_objs)
        print(f"Apex species: {apex_species}")
        societies = Civilization.run(species_ids=[apex_species.uuid])
        print(societies)
        planet["civilization_emerging"] = False
        planet["civilization"] = True
        planet["societies"] = societies
        db.set("planets", planet["id"], planet)
        # return evolve_society()
    print("Generation complete")

@app.task
def evolve_life():
    biome = Biome()
    up = UniverseProbability()
    up.setup()
    db = interface_interactor.get_interface("db")
    # Grab a planet to evolve
    planet_info = db.get_one("planets", {"Life Presence": True, "evolution_in_progress": {"$exists": False}, "evolution_complete": {"$exists": False}})
    if planet_info:
        print(f"Evolution in progress for planet {planet_info['id']}")
        planet_info["evolution_in_progress"] = True
        db.set("planets", planet_info["id"], planet_info)
        for biome_type in planet_info["Biomes"].keys():
            if planet_info["Biomes"][biome_type]['evolved'] == False:
                evolutionary_report = biome.evolve_for_biome(planet_info, biome_type, up.normalized_bx_b_df, up.normalized_bx_lf_df)
                # Convert lifeforms to UUIDs for lookup on the species table
                for i, life in enumerate(evolutionary_report["lifeforms"]):
                    evolutionary_report["lifeforms"][i] = life.uuid
                del evolutionary_report["environment"]
                # planet_info["Biomes"][biome_type]['Evolution'] = evolutionary_report
                planet_info["Biomes"][biome_type]['evolved'] = True
                planet_info["Biomes"][biome_type]["evolutionary_stage"] = evolutionary_report["final_evolutionary_stage"]
                planet_info["Biomes"][biome_type]["apex_species"] = {
                    "id": evolutionary_report["apex_species"],
                    "score": evolutionary_report["apex_species_score"],
                }
        planet_info["evolution_in_progress"] = False
        planet_info["evolution_complete"] = True
        db.set("planets", planet_info["id"], planet_info)
        return evolve_life() # recursively try again
    
    # No more planets to evolve
    print("Generation complete")

### Generates a galaxy and saves it to the database
### If the galaxy already exists, it will be returned
### @param key: The key to store the galaxy under
### @param num_systems: The number of systems to generate
### @param anim_steps: The number of animation steps to generate
### @param recreate: Whether to recreate the galaxy if it already exists
### @return: The generated galaxy
async def evolve_galaxy(
        key: str,
        num_systems: int = 625,
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
    has_life = response.pop('has_life', [])
    planet_queue = []

    for system in systems:
        if 'Planets' not in system:
            continue
        for planet in system['Planets']:
            planet['system_id'] = system['id']
            system['galaxy_key'] = key
            planet_queue.append(planet)
        system.pop('Planets')

    print("Saving galaxy to database...")
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
   response = await evolve_galaxy("milky_way", 625)
   return GalaxyResponse(systems=response)