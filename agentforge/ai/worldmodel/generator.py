import json, os, re
from agentforge.interfaces.model_profile import ModelProfile
from agentforge.interfaces import interface_interactor
from agentforge.interfaces.milvusstore import MilvusVectorStore
import numpy as np

def extract_species(text):
    # Regular expression pattern to match species names
    pattern = r'\d+\.\s+[A-Za-z0-9 .,\-]+\s+-\s+[A-Za-z0-9 .,\-]+\n'
    return re.findall(pattern, text)

def process_candidates(candidates):
    processed_data = []

    for candidate in candidates:
        # Splitting on the "-" character
        parts = candidate.split(" - ")
        if len(parts) != 2:
            continue

        title, description = parts

        # Removing digit(s) plus "." from the title
        name = re.sub(r'^\d+\.\s+', '', title).strip()

        # Adding to the list as a dictionary
        processed_data.append({"Name": name, "Description": description.replace("\n","").strip()})

    # Convert to JSON format
    return processed_data

### Generates a species for a planet in a biome. 
class SpeciesGenerator:

    def __init__(self, planet_type, uuid) -> None:
        self.planet_type = planet_type
        self.model_profile_interface = ModelProfile()
        self.model_profile = self.model_profile_interface.get("64fdf296716cbeaafedc545e")
        self.service = interface_interactor.get_interface("llm")
        model_name = os.getenv("VECTOR_EMBEDDINGS_MODEL_NAME")
        collection = "species"
        self.vectorstoremanager = MilvusVectorStore(model_name, collection, reset=True)
        self.vectorstore = self.vectorstoremanager.init_store_connection(collection)
    
    def generate(self, biome, evolutionary_stage, life_form_class, role, behavior_role, previous_species="", attributes=[], attempts=0):
        # Create a species
        if previous_species != "":
            previous_species = "The previous species in this evolutionary chain was {}.".format(previous_species)
        attributes_str = ""
        if len(attributes) > 0:
            attributes_str = "The species has the following attributes: {}".format(", ".join(attributes))
        prompt = """
        Generate a species name and description with the following requirements: {} {} The species is on a {} planet in a {} biome. The ecological system is in the evolutionary stage {}. The Species classification is {} and ecological role is {}. The species has a behavior role of {}. Go step by step, create a list of species, and select a single unique and bold species. The species should be suited to it's environment. Determine whether the ideas are scientific and novel, modify the species as needed to make them bolder and more diverse.
        """.format(previous_species, attributes_str, self.planet_type, biome, evolutionary_stage, life_form_class, role, behavior_role, previous_species)
        gen_config = self.model_profile['generation_config']
        gen_config['temperature'] = 0.4
        model_config = self.model_profile['model_config']
        input = {
            "prompt": prompt,
            "generation_config": gen_config,
            "model_config": model_config,
            "user_id": "system",
            "user_name": "system",
            "agent_name": "agentforge",
        }
        response = self.service.call(input)
        val = response['choices'][0]['text']

        # This list is now extracted and tested against the existng species
        # Of the chosen species the most unique is selected
        species_list = extract_species(val)
        candidates = process_candidates(species_list)
        descriptions = {}

        if len(candidates) > 0:
            # Test each of the candidates against the existing species
            processed_candidates = []
            for candidate_species in candidates:
                query = candidate_species['Name']
                descriptions[query] = candidate_species['Description']
                docs = self.vectorstore.similarity_search_with_score(query, k=1)
                if len(docs) != 0:
                    for doc in docs:
                        processed_candidates.append({"name": query, "score": doc[1]})

            if len(processed_candidates) == 0:
                choice = np.random.choice(candidates)
                choice =  {"Name": choice['Name'], "Description": descriptions[choice['Name']]}
            else:
                sorted_candidates = sorted(processed_candidates, key=lambda x: x['score'])
                choice =  {"Name": sorted_candidates[0]['name'], "Description": descriptions[sorted_candidates[0]['name']]}

            # Add the species to the vector store
            self.vectorstore.add_texts([choice['Name']])
            
            return choice
        
        formatted_prompt = """Extract the species name and description from the following text: {}""".format(val)
        input['prompt'] = formatted_prompt
        # Try outlines
        input['schema'] = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "Name": {
                "type": "string"
                },
                "description": {
                "type": "string"
                }
            },
            "required": ["Name", "description"]
        }
        response = self.service.call(input)
        val = response['choices'][0]['text']

        try:
            ret_val = json.loads(val)
            return ret_val
        except:
            pass

        # If data is None try again
        if attempts > 5:
            print("we tried 5 times to generate a species and failed. Implement grammars already!")
            return {}
        return self.generate(biome, evolutionary_stage, life_form_class, role, behavior_role, previous_species, attributes=attributes, attempts= attempts + 1)

        # print(candidates)

        # Now extract as JSON
        extract_json = """
        Pick the species that is the most scientific and novel. YOU MUST OUTPUT THIS SPECIES IN JSON. Output the final reponse using the following JSON template:
        {{   "Name": "Species Name",
             "Type": "Species Type",
             "Description": "Species Description",
        }}
        """

        # val = extract_last_json_object(val)
        if val != None:
            return val
        # If data is None try again
        if attempts > 5:
            print("we tried 5 times to generate a species and failed. Implement grammars already!")
            return {}
        return self.generate(biome, evolutionary_stage, life_form_class, role, behavior_role, previous_species, attempts= attempts + 1)
