import json

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

    values_based_on_genetics = json.load(open("values_based_on_genetics.json"))

    economic_mods = json.load(open("economic_mods.json"))

    sociopolitical_mods = sociopolitical_mods = json.load(open("sociopolitical_mods.json"))