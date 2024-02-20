import json, os

class ValueFramework:
    def __init__(self, genetics):
      self.values = self.get_values(genetics)

    def has(self, value):
        return value in self.values

    def get_values(self, genetics):
        # Compile the list of sociological norms associated with the expressed genetic features
        sociological_values = []
        for feature in genetics:
            if feature in self.values_based_on_genetics:
                sociological_values.extend(self.values_based_on_genetics[feature])
                
        # Remove duplicates from the sociological values list
        return list(set(sociological_values))

    def serialize(self):
        return self.values
    
    @classmethod
    def deserialize(self, values):
        return ValueFramework(values)

    data_dir = os.environ.get("WORLDGEN_DATA_DIR", "./")
    values_based_on_genetics = json.load(open(data_dir + "values_based_on_genetics.json"))
    economic_mods = json.load(open(data_dir + "economic_mods.json"))
    sociopolitical_mods = sociopolitical_mods = json.load(open(data_dir + "sociopolitical_mods.json"))