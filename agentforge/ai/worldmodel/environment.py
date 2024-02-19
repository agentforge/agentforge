class Environment:
    def __init__(self, total_nutrients):
        self.environment = {
            'Temperature': 20,  # Average temperature in Celsius
            'Gravity': 9.81,  # Gravity in m/s^2
            'Atmosphere Thickness': 1,  # Relative thickness, Earth's atmosphere = 1
            'Water Coverage': 0.5,  # Fraction of surface covered by water, 1 = 100%
            'Radiation': 0.5,  # Relative radiation level, 1 = High radiation
            'UV Index': 0.5,  # Relative UV Index, 1 = High UV exposure
            'Weather Pattern': 0.5,  # Stability of weather, 0 = chaotic, 1 = stable
            'Season': 0.5,  # Variability of seasons, 0 = extreme, 1 = mild
            'Water': total_nutrients,  # Placeholder for water resources
            'Sunlight': 100,  # Amount of sunlight (arbitrary units)
            'Nutrients': total_nutrients  # Total nutrients available in the environment
        }

        # Dictionary to store various resources
        self.resources = 5000

    def get(self, key):
        return self.environment[key]
    
    def set(self, key, value):
        self.environment[key] = value

    # Interactaction with the environment and lifeforms
    def interact(self, lifeform):
      for effect in self.environmental_effects:
        for individual in lifeform.individuals:
            genetics = lifeform.decode_genetics(individual['genes'], lifeform.genetic_base_line())
            individual['health'] += effect(self, genetics, lifeform.species_data['Biological Type'])
            if individual['health'] <= 0:
                individual['health'] = 0
                lifeform.population -= 1
      return lifeform


    environmental_effects = [
        # Temperature Impact
        lambda self, lifeform, bio_type: (-abs(self.environment['Temperature'] - 20) * (1 - lifeform["Thermal Resistance"] / 100)),

        # Gravity Impact on strength and endurance
        lambda self, lifeform, bio_type: (-abs(self.environment['Gravity'] - 9.81) * (1 - (lifeform["Strength"] + lifeform["Endurance"]) / 200)),

        # Gravity Impact on height and mass
        lambda self, lifeform, bio_type: (
            ((9.81 - self.environment['Gravity']) * lifeform["Height"] / 100) +
            ((9.81 - self.environment['Gravity']) * lifeform["Mass"] / 100)
        ),

        # Atmosphere Thickness Impact
        lambda self, lifeform, bio_type: (-abs(self.environment['Atmosphere Thickness'] - 1) * (1 - lifeform["Oxygen Utilization Efficiency"] / 100)),

        # Water Coverage Impact
        lambda self, lifeform, bio_type: (self.environment['Water Coverage'] * lifeform["Aquatic Adaptation"] / 100),

        # Radiation Impact
        lambda self, lifeform, bio_type: (-self.environment['Radiation'] * (1 - lifeform["Radiation Resistance"] / 100)),

        # Photosynthetic Ability Impact (for flora)
        lambda self, lifeform, bio_type: (self.environment['UV Index'] * lifeform["Photosynthetic Ability"] / 100) if bio_type == "Flora" else 0,

        # UV Index Impact
        lambda self, lifeform, bio_type: (-self.environment['UV Index'] * (1 - lifeform["Regeneration"] / 100)),

        # # Weather Patterns and Seasons Impact
        # lambda lifeform, weather_pattern: lifeform.update_health(-abs(weather_pattern - 0.5) * (1 - lifeform.traits["Adaptability"] / 100)),
    ]

    def get_environment(self):
        return self.environment

    def get_resources(self):
        return self.resources