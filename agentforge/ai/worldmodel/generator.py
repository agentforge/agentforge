import json
from agentforge.interfaces.model_profile import ModelProfile
from agentforge.interfaces import interface_interactor

### Generates a species for a planet in a biome. 
class SpeciesGenerator:

    def __init__(self, planet_type) -> None:
        self.planet_type = planet_type
        self.model_profile_interface = ModelProfile()
        self.model_profile = self.model_profile_interface.get("64fdf296716cbeaafedc545e")
        self.service = interface_interactor.get_interface("llm")
    
    def generate(self, biome, evolutionary_stage, life_form_class):
        # Create a species
        prompt = """Generate a species for a {} planet in a {} biome. The ecological system is in the evolutionary stage {}. The Species classification is {}. Be creative in the naming conventions and descriptions. DO NOT NAME THE SPECIES AFTER A VARIATION AFTER ANY OF THE ABOVE INFORMATION. Output the reponse using the following template:
        {{   "Name": "Species Name",
             "Type": "Species Type",
             "Description": "Species Description",
        }}
        """.format(self.planet_type, biome, evolutionary_stage, life_form_class)
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
        try:
            return json.loads(val)
        except:
            print("Failed to parse: {}".format(val))
            return {}
