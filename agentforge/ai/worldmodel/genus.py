import numpy as np
import json, os
class Genus:
    
    def __init__(self):
        pass

    def get_genus(self, biological_type, evolutionary_stage):
        if biological_type not in self.lifeform_genus_data:
            print(f"Biological type not found in genus data '{biological_type}'")
            return "Exotic"
        probabilities = list(self.lifeform_genus_data[biological_type][evolutionary_stage].values())
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]
        names = list(self.lifeform_genus_data[biological_type][evolutionary_stage].keys())
        return np.random.choice(names, p=probabilities)

    # More speciiic life form concepts -- to supply LLM prompts
    lifeform_genus_data = json.load(open(os.environ.get("WORLDGEN_DATA_DIR", "./") + "lifeform_genus_data.json"))