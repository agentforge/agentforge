import numpy as np
import pandas as pd
from .star import Star
from .concept import Concept

class Lifeform:
    """
    Unicellular to Sentient Lifeforms and more
    """
    def __init__(self):
        self.star = Star()
        self.life_form_characteristic_names = list(set(b for biomes in self.life_form_characteristics.values() for b in biomes))
        self.life_form_categories = list(self.life_form_characteristics.keys())
        # Create concepts for each planet type
        self.biologic_concepts = {}
        for biologic_type in self.life_form_categories:
            self.biologic_concepts[biologic_type] = Concept(biologic_type, "Biological Type")

    def create_biological_matrix_row_normalization(self):
        """
        Create a matrix for biological types with characteristics based on base and standard deviation values.
        Then apply normalization across each row to convert these values into normalized scores.

        :param biological_types: Dictionary of biological types with characteristics' base and std values
        :param characteristics: List of characteristics to consider
        :return: DataFrame representing the biological characteristics matrix with normalized scores
        """
        # Initialize a DataFrame to hold the matrix values
        matrix_df = pd.DataFrame(index=self.life_form_characteristics.keys(), columns=self.life_form_characteristic_names)

        # Populate the DataFrame with generated values
        for bio_type, bio_chars in self.life_form_characteristics.items():
            for char in self.life_form_characteristic_names:
                base, std = bio_chars.get(char, {}).get('base', 0), bio_chars.get(char, {}).get('std', 0)
                matrix_df.at[bio_type, char] = np.random.normal(base, std) if std > 0 else base

        # Replace any NaN values with 0 and apply row-wise normalization
        matrix_df.fillna(0, inplace=True)

        # Adjust normalization to avoid division by zero
        row_sums = matrix_df.sum(axis=1)
        row_sums[row_sums == 0] = 1  # Replace 0 sums with 1 to avoid division by zero
        normalized_matrix = matrix_df.div(row_sums, axis=0)

        return normalized_matrix

    # Create a set of attributes/genetic profile for this life form type
    def sample_genetic_profile(self, key):
        genetic_profile = {}
        for attribute, values in self.life_form_characteristics[key].items():
            base = values["base"]
            std = values["std"]
            # Sampling from a normal distribution with the given base and standard deviation
            genetic_profile[attribute] = max(min(round(np.random.normal(base, std), 2), 100.0), 0.0)
        return genetic_profile
    
    # Mapping lifeform category to life of lifeform attributes -- > output: values
    life_form_characteristics = {
        "Amorphous": {
            "Height": {"base": 1, "std": 1},  # Height in meters
            "Mass": {"base": 1, "std": 1},  # Mass in kilograms
            "Intelligence": {"base": 20, "std": 10},
            "Strength": {"base": 30, "std": 15},
            "Dexterity": {"base": 50, "std": 20},
            "Constitution": {"base": 70, "std": 10},
            "Charisma": {"base": 5, "std": 5},
            "Wisdom": {"base": 20, "std": 10},
            "Perception": {"base": 40, "std": 15},
            "Endurance": {"base": 60, "std": 20},
            "Speed": {"base": 20, "std": 10},
            "Adaptability": {"base": 80, "std": 10},
            "Camouflage": {"base": 70, "std": 15},
            "Aquatic Adaptation": {"base": 60, "std": 20},
            "Thermal Resistance": {"base": 50, "std": 20},
            "Radiation Resistance": {"base": 40, "std": 20},
            "Photosynthetic Ability": {"base": 0, "std": 0},
            "Regeneration": {"base": 80, "std": 10},
            "Longevity": {"base": 50, "std": 20},
            "Reproductive Rate": {"base": 80, "std": 10},
            "Sensory Range": {"base": 40, "std": 15},
            "Ecosystem Impact": {"base": 40, "std": 20},
            "Resource Utilization": {"base": 60, "std": 20}, # High Resource Utilization indicates usage efficiency
            "Stealth": {"base": 70, "std": 15},
            "Flight Capability": {"base": 0, "std": 0},
            "Immune System Strength": {"base": 90, "std": 5},
            "Nutritional Requirements": {"base": 20, "std": 10},
            "Pressure Resistance": {"base": 80, "std": 10},
            "Social Cooperation": {"base": 50, "std": 50},
            "Oxygen Utilization Efficiency": {"base": 100, "std": 0},
            "Vision Adaptation": {"base": 0, "std": 0},
            "Eco-Sensitivity": {"base": 15, "std": 5},
            "Predation Instincts": {"base": 50, "std": 25},
            "Toxin Resistance": {"base": 10, "std": 5},
            "Toxin Production": {"base": 0, "std": 0},
            "Navigation Skills": {"base": 80, "std": 10},
            "Offspring": {"base": 1, "std": 0},
        },
        "Aquatic": {
            "Height": {"base": 50, "std": 20},  # Height in meters
            "Mass": {"base": 50, "std": 20},  # Mass in kilograms
            "Intelligence": {"base": 50, "std": 15},  # Varies among species
            "Strength": {"base": 60, "std": 15},      # Swimming power
            "Dexterity": {"base": 50, "std": 20},     # Finesse in water movement
            "Constitution": {"base": 70, "std": 10},  # Health and resistance in aquatic environment
            "Charisma": {"base": 30, "std": 20},      # Social influence among species
            "Wisdom": {"base": 40, "std": 15},        # Environmental awareness
            "Perception": {"base": 70, "std": 10},    # Sensory perception in water
            "Endurance": {"base": 60, "std": 20},     # Sustaining swimming activity
            "Speed": {"base": 70, "std": 15},         # Swimming speed
            "Adaptability": {"base": 50, "std": 20},  # Adjusting to different aquatic environments
            "Camouflage": {"base": 60, "std": 15},    # Blending with aquatic surroundings
            "Aquatic Adaptation": {"base": 100, "std": 0}, # Perfect adaptation to water
            "Thermal Resistance": {"base": 50, "std": 20}, # Tolerance to water temperature variations
            "Radiation Resistance": {"base": 30, "std": 20}, # Resistance to underwater radiation
            "Photosynthetic Ability": {"base": 10, "std": 10}, # Only for some species
            "Regeneration": {"base": 40, "std": 20},  # Healing and regrowth ability
            "Longevity": {"base": 50, "std": 20},     # Lifespan potential in water
            "Reproductive Rate": {"base": 70, "std": 15}, # Reproductive efficiency
            "Sensory Range": {"base": 70, "std": 10}, # Range of underwater senses
            "Mental Fortitude": {"base": 40, "std": 20},  # Mental resilience
            "Physical Fortitude": {"base": 60, "std": 15}, # Resistance to physical damage
            "Ecosystem Impact": {"base": 50, "std": 20},  # Influence in aquatic ecosystems
            "Social Structure": {"base": 40, "std": 20},  # Social organization in species
            "Resource Utilization": {"base": 60, "std": 15}, # Efficiency in using aquatic resources
            "Stealth": {"base": 60, "std": 15},        # Ability to move undetected in water
            "Flight Capability": {"base": 0, "std": 0},   # Not applicable in traditional sense
            "Immune System Strength": {"base": 90, "std": 5},
            "Nutritional Requirements": {"base": 20, "std": 10},
            "Pressure Resistance": {"base": 80, "std": 10},
            "Social Cooperation": {"base": 50, "std": 50},
            "Oxygen Utilization Efficiency": {"base": 100, "std": 0},
            "Vision Adaptation": {"base": 0, "std": 0},
            "Eco-Sensitivity": {"base": 15, "std": 5},
            "Predation Instincts": {"base": 50, "std": 25},
            "Toxin Resistance": {"base": 10, "std": 5},
            "Toxin Production": {"base": 0, "std": 0},
            "Navigation Skills": {"base": 80, "std": 10},
            "Offspring": {"base": 1, "std": 0},
        },
        "Cold-Tolerant Fauna": {
            "Height": {"base": 50, "std": 20},  # Height in meters
            "Mass": {"base": 50, "std": 20},  # Mass in kilograms
            "Intelligence": {"base": 50, "std": 15},  # Average, varies among species
            "Strength": {"base": 65, "std": 15},      # Physical power for survival in harsh climates
            "Dexterity": {"base": 40, "std": 20},     # Coordination, limited by bulky physiques
            "Constitution": {"base": 80, "std": 10},  # Robust health, stamina, cold resistance
            "Charisma": {"base": 30, "std": 20},      # Social influence, varies among species
            "Wisdom": {"base": 55, "std": 15},        # Adaptation and judgment in cold environments
            "Perception": {"base": 60, "std": 15},    # Sensory acuity in cold, often low-visibility environments
            "Endurance": {"base": 70, "std": 10},     # Sustaining activity in cold climates
            "Speed": {"base": 50, "std": 20},         # Movement rate, can be limited by terrain and body structure
            "Adaptability": {"base": 60, "std": 15},  # Adjusting to varying cold environments
            "Camouflage": {"base": 60, "std": 15},    # Blending with snowy and icy surroundings
            "Aquatic Adaptation": {"base": 40, "std": 20}, # For species that interact with icy waters
            "Thermal Resistance": {"base": 90, "std": 5},  # High tolerance to extreme cold
            "Radiation Resistance": {"base": 30, "std": 20}, # General resistance to radiation
            "Photosynthetic Ability": {"base": 0, "std": 0}, # Not applicable
            "Regeneration": {"base": 30, "std": 20},  # Limited regenerative abilities
            "Longevity": {"base": 60, "std": 20},     # Lifespan potential in harsh climates
            "Reproductive Rate": {"base": 40, "std": 20}, # Often lower in harsh conditions
            "Sensory Range": {"base": 60, "std": 15}, # Adapted sensory range for cold environments
            "Mental Fortitude": {"base": 70, "std": 10},  # Resilience to environmental stress
            "Physical Fortitude": {"base": 80, "std": 10}, # Physical resilience in cold climates
            "Ecosystem Impact": {"base": 50, "std": 20},  # Influence within their ecological niche
            "Social Structure": {"base": 40, "std": 20},  # Varies among species
            "Resource Utilization": {"base": 50, "std": 20}, # Efficiency in resource-scarce environments
            "Stealth": {"base": 40, "std": 20},        # Predatory or defensive stealth
            "Flight Capability": {"base": 10, "std": 10},   # Limited to certain bird species
            "Immune System Strength": {"base": 90, "std": 5},
            "Nutritional Requirements": {"base": 20, "std": 10},
            "Pressure Resistance": {"base": 80, "std": 10},
            "Social Cooperation": {"base": 50, "std": 50},
            "Oxygen Utilization Efficiency": {"base": 100, "std": 0},
            "Vision Adaptation": {"base": 0, "std": 0},
            "Eco-Sensitivity": {"base": 15, "std": 5},
            "Predation Instincts": {"base": 50, "std": 25},
            "Toxin Resistance": {"base": 10, "std": 5},
            "Toxin Production": {"base": 0, "std": 0},
            "Navigation Skills": {"base": 80, "std": 10},
            "Offspring": {"base": 1, "std": 0},
        },
        "Cold-Tolerant Flora": {
            "Height": {"base": 50, "std": 20},  # Height in meters
            "Mass": {"base": 50, "std": 20},  # Mass in kilograms
            "Intelligence": {"base": 1, "std": 1},  # Limited to adaptive behaviors
            "Strength": {"base": 20, "std": 10},    # Structural strength against elements
            "Dexterity": {"base": 1, "std": 1},     # Limited to growth patterns
            "Constitution": {"base": 80, "std": 10}, # Health and resistance to cold
            "Charisma": {"base": 20, "std": 15},    # Influence on pollinators and animals
            "Wisdom": {"base": 1, "std": 1},        # Adaptation to environment
            "Perception": {"base": 1, "std": 1},    # Limited to basic environmental responses
            "Endurance": {"base": 90, "std": 5},    # Survival through harsh conditions
            "Speed": {"base": 1, "std": 1},         # Growth rate, slow in cold environments
            "Adaptability": {"base": 70, "std": 10}, # Adapting to cold environments
            "Camouflage": {"base": 60, "std": 15},  # Blending with snowy environments
            "Aquatic Adaptation": {"base": 10, "std": 10}, # For those near water sources
            "Thermal Resistance": {"base": 95, "std": 5},  # High resistance to cold
            "Radiation Resistance": {"base": 30, "std": 15}, # Resistance to UV radiation
            "Photosynthetic Ability": {"base": 70, "std": 15}, # Efficiency under low light
            "Regeneration": {"base": 40, "std": 20},  # Ability to regrow after damage
            "Longevity": {"base": 80, "std": 10},     # Lifespan, many are perennials
            "Reproductive Rate": {"base": 40, "std": 20}, # Seed dispersal and germination
            "Sensory Range": {"base": 1, "std": 1},   # Limited to basic environmental responses
            "Mental Fortitude": {"base": 1, "std": 1},  # Not applicable
            "Physical Fortitude": {"base": 80, "std": 10}, # Resistance to physical elements
            "Ecosystem Impact": {"base": 70, "std": 15},  # Influence on the cold ecosystem
            "Social Structure": {"base": 1, "std": 1},  # Limited to plant interactions
            "Resource Utilization": {"base": 60, "std": 15}, # Resource efficiency
            "Stealth": {"base": 1, "std": 1},         # Not applicable
            "Flight Capability": {"base": 1, "std": 1},   # Limited to seed dispersal
            "Immune System Strength": {"base": 90, "std": 5},
            "Nutritional Requirements": {"base": 20, "std": 10},
            "Pressure Resistance": {"base": 80, "std": 10},
            "Social Cooperation": {"base": 50, "std": 50},
            "Oxygen Utilization Efficiency": {"base": 100, "std": 0},
            "Vision Adaptation": {"base": 0, "std": 0},
            "Eco-Sensitivity": {"base": 15, "std": 5},
            "Predation Instincts": {"base": 50, "std": 25},
            "Toxin Resistance": {"base": 10, "std": 5},
            "Toxin Production": {"base": 0, "std": 0},
            "Navigation Skills": {"base": 80, "std": 10},
            "Offspring": {"base": 1, "std": 0},
        },
        "Gaseous": {
            "Height": {"base": 80, "std": 20},  # Height in meters
            "Mass": {"base": 1, "std": 1},  # Mass in kilograms
            "Intelligence": {"base": 10, "std": 5},   # Hypothetical cognitive abilities
            "Strength": {"base": 5, "std": 5},        # Limited physical force
            "Dexterity": {"base": 80, "std": 10},     # High maneuverability in gaseous state
            "Constitution": {"base": 70, "std": 15},  # Resilience in gaseous form
            "Charisma": {"base": 10, "std": 10},      # Hypothetical social influence
            "Wisdom": {"base": 10, "std": 10},        # Environmental awareness
            "Perception": {"base": 60, "std": 20},    # Sensing changes in the environment
            "Endurance": {"base": 80, "std": 10},     # Sustaining form over time
            "Speed": {"base": 90, "std": 10},         # Rapid movement as gas
            "Adaptability": {"base": 80, "std": 10},  # Adjusting to environmental changes
            "Camouflage": {"base": 80, "std": 10},    # Blending into gaseous environments
            "Aquatic Adaptation": {"base": 20, "std": 15}, # Limited underwater capability
            "Thermal Resistance": {"base": 70, "std": 15}, # Tolerance to temperature changes
            "Radiation Resistance": {"base": 50, "std": 20}, # Resistance to radiation
            "Photosynthetic Ability": {"base": 0, "std": 0}, # Not applicable
            "Regeneration": {"base": 80, "std": 10},  # Reforming after dispersion
            "Longevity": {"base": 50, "std": 20},     # Lifespan potential
            "Reproductive Rate": {"base": 50, "std": 20}, # Hypothetical reproduction rate
            "Sensory Range": {"base": 60, "std": 20}, # Sensory perception in a gaseous state
            "Mental Fortitude": {"base": 20, "std": 15},  # Resilience to mental stress
            "Physical Fortitude": {"base": 30, "std": 20}, # Resistance to physical alterations
            "Ecosystem Impact": {"base": 40, "std": 20},  # Influence on surrounding environment
            "Social Structure": {"base": 10, "std": 10},  # Hypothetical social interactions
            "Resource Utilization": {"base": 70, "std": 15}, # Efficiency in resource use
            "Stealth": {"base": 80, "std": 10},        # Moving undetected
            "Flight Capability": {"base": 100, "std": 0},   # Innate ability to float or drift
            "Immune System Strength": {"base": 90, "std": 5},
            "Nutritional Requirements": {"base": 20, "std": 10},
            "Pressure Resistance": {"base": 80, "std": 10},
            "Social Cooperation": {"base": 50, "std": 50},
            "Oxygen Utilization Efficiency": {"base": 100, "std": 0},
            "Vision Adaptation": {"base": 0, "std": 0},
            "Eco-Sensitivity": {"base": 15, "std": 5},
            "Predation Instincts": {"base": 50, "std": 25},
            "Toxin Resistance": {"base": 10, "std": 5},
            "Toxin Production": {"base": 0, "std": 0},
            "Navigation Skills": {"base": 80, "std": 10},
            "Offspring": {"base": 1, "std": 0},
        },
        "Plasma": {
            "Height": {"base": 20, "std": 20},  # Height in meters
            "Mass": {"base": 20, "std": 20},  # Mass in kilograms
            "Intelligence": {"base": 30, "std": 20},  # Hypothetical cognitive abilities
            "Strength": {"base": 40, "std": 20},      # Potential force exertion in a plasma state
            "Dexterity": {"base": 70, "std": 15},     # Maneuverability and shape adaptation
            "Constitution": {"base": 60, "std": 20},  # Overall resilience in a plasma state
            "Charisma": {"base": 10, "std": 10},      # Hypothetical social influence
            "Wisdom": {"base": 20, "std": 15},        # Environmental awareness and adaptation
            "Perception": {"base": 50, "std": 20},    # Sensing environmental changes
            "Endurance": {"base": 80, "std": 10},     # Sustaining form and energy
            "Speed": {"base": 75, "std": 15},         # Movement and reaction rates
            "Adaptability": {"base": 80, "std": 10},  # Adjusting to different environments
            "Camouflage": {"base": 70, "std": 15},    # Blending with energy fields or lights
            "Aquatic Adaptation": {"base": 20, "std": 20}, # Interactions with liquids
            "Thermal Resistance": {"base": 90, "std": 10}, # High tolerance to temperature
            "Radiation Resistance": {"base": 80, "std": 15}, # Withstanding high energy environments
            "Photosynthetic Ability": {"base": 0, "std": 0}, # Not applicable
            "Regeneration": {"base": 80, "std": 10},  # Reconstituting plasma structure
            "Longevity": {"base": 50, "std": 20},     # Theoretical lifespan
            "Reproductive Rate": {"base": 40, "std": 20}, # Hypothetical reproduction methods
            "Sensory Range": {"base": 60, "std": 20}, # Sensing in a plasma state
            "Mental Fortitude": {"base": 30, "std": 20},  # Resilience to mental or energy stress
            "Physical Fortitude": {"base": 50, "std": 20}, # Resistance to physical disruptions
            "Ecosystem Impact": {"base": 40, "std": 20},  # Influence on surrounding environment
            "Social Structure": {"base": 10, "std": 15},  # Hypothetical social organization
            "Resource Utilization": {"base": 60, "std": 20}, # Efficiency in energy use
            "Stealth": {"base": 50, "std": 20},        # Ability to exist undetected
            "Flight Capability": {"base": 100, "std": 0},  # Innate floating or flying ability
            "Immune System Strength": {"base": 90, "std": 5},
            "Nutritional Requirements": {"base": 20, "std": 10},
            "Pressure Resistance": {"base": 80, "std": 10},
            "Social Cooperation": {"base": 50, "std": 50},
            "Oxygen Utilization Efficiency": {"base": 100, "std": 0},
            "Vision Adaptation": {"base": 0, "std": 0},
            "Eco-Sensitivity": {"base": 15, "std": 5},
            "Predation Instincts": {"base": 50, "std": 25},
            "Toxin Resistance": {"base": 10, "std": 5},
            "Toxin Production": {"base": 0, "std": 0},
            "Navigation Skills": {"base": 80, "std": 10},
            "Offspring": {"base": 1, "std": 0},
        },
        "Crystalline": {
            "Height": {"base": 50, "std": 50},  # Height in meters
            "Mass": {"base": 50, "std": 50},  # Mass in kilograms
            "Intelligence": {"base": 20, "std": 10},  # Hypothetical cognitive abilities
            "Strength": {"base": 80, "std": 10},      # Structural robustness and stability
            "Dexterity": {"base": 10, "std": 5},      # Limited due to rigid structure
            "Constitution": {"base": 90, "std": 5},   # High resilience, resistance to toxins
            "Charisma": {"base": 10, "std": 10},      # Hypothetical influence
            "Wisdom": {"base": 25, "std": 15},        # Environmental awareness
            "Perception": {"base": 40, "std": 20},    # Sensing changes, possibly through vibrations
            "Endurance": {"base": 90, "std": 10},     # Longevity and durability
            "Speed": {"base": 5, "std": 5},           # Limited movement capabilities
            "Adaptability": {"base": 30, "std": 15},  # Limited due to rigid structure
            "Camouflage": {"base": 60, "std": 20},    # Blending with mineral environments
            "Aquatic Adaptation": {"base": 20, "std": 15}, # Limited interaction with water
            "Thermal Resistance": {"base": 80, "std": 10}, # Resistance to temperature changes
            "Radiation Resistance": {"base": 70, "std": 15}, # Resistance to radiation
            "Photosynthetic Ability": {"base": 0, "std": 0}, # Not applicable
            "Regeneration": {"base": 30, "std": 20},  # Limited ability to reform
            "Longevity": {"base": 100, "std": 0},     # Potentially very long lifespan
            "Reproductive Rate": {"base": 10, "std": 10}, # Hypothetical reproduction methods
            "Sensory Range": {"base": 30, "std": 20}, # Limited sensory perception
            "Mental Fortitude": {"base": 20, "std": 15},  # Resilience to mental or energy stresses
            "Physical Fortitude": {"base": 90, "std": 10}, # High resistance to physical damage
            "Ecosystem Impact": {"base": 40, "std": 20},  # Influence on surrounding environment
            "Social Structure": {"base": 10, "std": 10},  # Hypothetical social interactions
            "Resource Utilization": {"base": 50, "std": 20}, # Efficiency in resource use
            "Stealth": {"base": 40, "std": 20},        # Ability to remain undetected
            "Flight Capability": {"base": 0, "std": 0},  # Not applicable
            "Immune System Strength": {"base": 90, "std": 5},
            "Nutritional Requirements": {"base": 20, "std": 10},
            "Pressure Resistance": {"base": 80, "std": 10},
            "Social Cooperation": {"base": 50, "std": 50},
            "Oxygen Utilization Efficiency": {"base": 100, "std": 0},
            "Vision Adaptation": {"base": 0, "std": 0},
            "Eco-Sensitivity": {"base": 15, "std": 5},
            "Predation Instincts": {"base": 50, "std": 25},
            "Toxin Resistance": {"base": 10, "std": 5},
            "Toxin Production": {"base": 0, "std": 0},
            "Navigation Skills": {"base": 80, "std": 10},
            "Offspring": {"base": 1, "std": 0},
        },
        "Electromagnetic": {
            "Height": {"base": 50, "std": 50},  # Height in meters
            "Mass": {"base": 50, "std": 50},  # Mass in kilograms
            "Intelligence": {"base": 40, "std": 20},  # Hypothetical cognitive abilities in manipulating electromagnetic fields
            "Strength": {"base": 70, "std": 15},      # Ability to exert force through electromagnetic interactions
            "Dexterity": {"base": 60, "std": 20},     # Coordination and control over electromagnetic phenomena
            "Constitution": {"base": 80, "std": 10},  # Robustness in an electromagnetic environment
            "Charisma": {"base": 30, "std": 20},      # Hypothetical social influence through electromagnetic interactions
            "Wisdom": {"base": 50, "std": 15},        # Insight and judgment in utilizing electromagnetic fields
            "Perception": {"base": 80, "std": 10},    # Sensory acuity based on electromagnetic sensing
            "Endurance": {"base": 70, "std": 15},     # Sustaining electromagnetic activities over time
            "Speed": {"base": 90, "std": 10},         # Rapid movement and reaction in an electromagnetic context
            "Adaptability": {"base": 75, "std": 15},  # Adjusting to varying electromagnetic environments
            "Camouflage": {"base": 80, "std": 10},    # Blending into electromagnetic fields
            "Aquatic Adaptation": {"base": 50, "std": 20}, # Interaction with electromagnetic properties of water
            "Thermal Resistance": {"base": 70, "std": 15}, # Tolerance to temperature effects on electromagnetism
            "Radiation Resistance": {"base": 90, "std": 10}, # Withstanding electromagnetic radiation
            "Photosynthetic Ability": {"base": 0, "std": 0}, # Not applicable
            "Regeneration": {"base": 60, "std": 20},  # Ability to reorganize electromagnetic structure
            "Longevity": {"base": 60, "std": 20},     # Lifespan in an electromagnetic context
            "Reproductive Rate": {"base": 40, "std": 20}, # Hypothetical reproduction methods
            "Sensory Range": {"base": 90, "std": 10}, # Broad range of electromagnetic sensory perception
            "Mental Fortitude": {"base": 50, "std": 20},  # Resilience to mental or electromagnetic stress
            "Physical Fortitude": {"base": 70, "std": 15}, # Resistance to physical disruptions in an electromagnetic context
            "Ecosystem Impact": {"base": 60, "std": 20},  # Influence on surrounding electromagnetic environment
            "Social Structure": {"base": 20, "std": 15},  # Hypothetical social organization based on electromagnetic communication
            "Resource Utilization": {"base": 70, "std": 15}, # Efficiency in using electromagnetic resources
            "Stealth": {"base": 70, "std": 15},        # Moving undetected within electromagnetic fields
            "Flight Capability": {"base": 80, "std": 10},   # Manipulating electromagnetic fields for movement
            "Immune System Strength": {"base": 90, "std": 5},
            "Nutritional Requirements": {"base": 20, "std": 10},
            "Pressure Resistance": {"base": 80, "std": 10},
            "Social Cooperation": {"base": 50, "std": 50},
            "Oxygen Utilization Efficiency": {"base": 100, "std": 0},
            "Vision Adaptation": {"base": 0, "std": 0},
            "Eco-Sensitivity": {"base": 15, "std": 5},
            "Predation Instincts": {"base": 50, "std": 25},
            "Toxin Resistance": {"base": 10, "std": 5},
            "Toxin Production": {"base": 0, "std": 0},
            "Navigation Skills": {"base": 80, "std": 10},
            "Offspring": {"base": 1, "std": 0},
        },
        "Flora": {
            "Height": {"base": 50, "std": 50},  # Height in meters
            "Mass": {"base": 50, "std": 25},  # Mass in kilograms
            "Intelligence": {"base": 1, "std": 1},  # Limited to adaptive responses
            "Strength": {"base": 30, "std": 15},    # Structural strength against gravity and elements
            "Dexterity": {"base": 1, "std": 1},     # Limited to growth patterns
            "Constitution": {"base": 70, "std": 15}, # Health, resilience, and disease resistance
            "Charisma": {"base": 20, "std": 15},    # Influence on pollinators and animals
            "Wisdom": {"base": 1, "std": 1},        # Adaptation and response to environmental conditions
            "Perception": {"base": 1, "std": 1},    # Basic environmental sensing
            "Endurance": {"base": 80, "std": 10},   # Survival through varying conditions
            "Speed": {"base": 1, "std": 1},         # Growth rate
            "Adaptability": {"base": 60, "std": 20}, # Adapting to different terrestrial environments
            "Camouflage": {"base": 40, "std": 20},  # Blending with the environment
            "Aquatic Adaptation": {"base": 10, "std": 10}, # Interaction with water
            "Thermal Resistance": {"base": 50, "std": 20}, # Tolerance to temperature variations
            "Radiation Resistance": {"base": 30, "std": 20}, # Resistance to UV radiation
            "Photosynthetic Ability": {"base": 90, "std": 10}, # Energy derivation from sunlight
            "Regeneration": {"base": 50, "std": 20},  # Ability to regrow parts
            "Longevity": {"base": 60, "std": 20},     # Lifespan potential
            "Reproductive Rate": {"base": 70, "std": 15}, # Seed production and dispersal
            "Sensory Range": {"base": 1, "std": 1},   # Limited to basic environmental sensing
            "Mental Fortitude": {"base": 1, "std": 1},  # Not applicable
            "Physical Fortitude": {"base": 60, "std": 20}, # Resistance to physical damage
            "Ecosystem Impact": {"base": 70, "std": 15},  # Influence on the terrestrial ecosystem
            "Social Structure": {"base": 1, "std": 1},  # Interaction with other plants and organisms
            "Resource Utilization": {"base": 70, "std": 15}, # Efficiency in using soil and sunlight
            "Stealth": {"base": 1, "std": 1},         # Not applicable
            "Flight Capability": {"base": 1, "std": 1},   # Limited to seed dispersal
            "Immune System Strength": {"base": 90, "std": 5},
            "Nutritional Requirements": {"base": 20, "std": 10},
            "Pressure Resistance": {"base": 80, "std": 10},
            "Social Cooperation": {"base": 50, "std": 50},
            "Oxygen Utilization Efficiency": {"base": 100, "std": 0},
            "Vision Adaptation": {"base": 0, "std": 0},
            "Eco-Sensitivity": {"base": 15, "std": 5},
            "Predation Instincts": {"base": 50, "std": 25},
            "Toxin Resistance": {"base": 10, "std": 5},
            "Toxin Production": {"base": 0, "std": 0},
            "Navigation Skills": {"base": 80, "std": 10},     
            "Offspring": {"base": 1, "std": 0},      
        },
        "Pressure-Resistant": {
            "Height": {"base": 50, "std": 50},  # Height in meters
            "Mass": {"base": 50, "std": 50},  # Mass in kilograms
            "Intelligence": {"base": 30, "std": 15},  # Cognitive abilities focused on survival in high-pressure environments
            "Strength": {"base": 60, "std": 20},      # Physical strength to withstand pressure
            "Dexterity": {"base": 40, "std": 20},     # Agility under pressure, possibly limited by environmental constraints
            "Constitution": {"base": 90, "std": 10},  # Robustness and resistance to high-pressure conditions
            "Charisma": {"base": 20, "std": 15},      # Influence within their species, limited social interactions
            "Wisdom": {"base": 40, "std": 15},        # Judgment and awareness in a high-pressure environment
            "Perception": {"base": 70, "std": 15},    # Sensory abilities adapted to deep-sea or high-pressure conditions
            "Endurance": {"base": 80, "std": 10},     # Ability to sustain activities under constant pressure
            "Speed": {"base": 30, "std": 15},         # Movement rate, likely reduced due to environmental density
            "Adaptability": {"base": 60, "std": 15},  # Adaptation to varying pressures and related environmental factors
            "Camouflage": {"base": 50, "std": 20},    # Ability to blend into high-pressure environments
            "Aquatic Adaptation": {"base": 80, "std": 10}, # Primarily for aquatic organisms in high-pressure zones
            "Thermal Resistance": {"base": 60, "std": 20}, # Resistance to temperature variations in high-pressure environments
            "Radiation Resistance": {"base": 40, "std": 20}, # Resistance to radiation, depending on environment
            "Photosynthetic Ability": {"base": 5, "std": 10}, # Limited due to lack of light in deep environments
            "Regeneration": {"base": 50, "std": 20},  # Healing abilities under pressure
            "Longevity": {"base": 60, "std": 20},     # Lifespan potential in a high-pressure environment
            "Reproductive Rate": {"base": 40, "std": 20}, # Reproduction in a challenging environment
            "Sensory Range": {"base": 70, "std": 15}, # Sensory perception adapted to deep or high-pressure conditions
            "Mental Fortitude": {"base": 50, "std": 20},  # Psychological resilience to the demands of their environment
            "Physical Fortitude": {"base": 90, "std": 10}, # High resistance to physical damage from pressure
            "Ecosystem Impact": {"base": 50, "std": 20},  # Influence on and adaptation to their high-pressure ecosystem
            "Social Structure": {"base": 20, "std": 15},  # Social interactions, likely limited
            "Resource Utilization": {"base": 60, "std": 15}, # Efficient use of available resources in their environment
            "Stealth": {"base": 40, "std": 20}, # Ability to move or exist without detection, adapted to high-pressure conditions
            "Flight Capability": {"base": 10, "std": 10}, # Limited to swimming capabilities, not traditional flight
            "Immune System Strength": {"base": 90, "std": 5},
            "Nutritional Requirements": {"base": 20, "std": 10},
            "Pressure Resistance": {"base": 80, "std": 10},
            "Social Cooperation": {"base": 50, "std": 50},
            "Oxygen Utilization Efficiency": {"base": 100, "std": 0},
            "Vision Adaptation": {"base": 0, "std": 0},
            "Eco-Sensitivity": {"base": 15, "std": 5},
            "Predation Instincts": {"base": 50, "std": 25},
            "Toxin Resistance": {"base": 10, "std": 5},
            "Toxin Production": {"base": 0, "std": 0},
            "Navigation Skills": {"base": 80, "std": 10},
            "Offspring": {"base": 1, "std": 0},
        },
        "Quantum": {
            "Height": {"base": 50, "std": 50},  # Height in meters
            "Mass": {"base": 50, "std": 50},  # Mass in kilograms
            "Intelligence": {"base": 80, "std": 10},  # Advanced cognitive abilities, potentially linked to quantum computing principles
            "Strength": {"base": 50, "std": 20},      # Conceptual strength, possibly related to influence on quantum states
            "Dexterity": {"base": 70, "std": 15},     # Agility in manipulating quantum phenomena
            "Constitution": {"base": 60, "std": 20},  # Robustness in a quantum environment
            "Charisma": {"base": 40, "std": 20},      # Hypothetical influence over other quantum entities
            "Wisdom": {"base": 75, "std": 15},        # Insight and judgment in a quantum context
            "Perception": {"base": 90, "std": 10},    # Sensory abilities heightened by quantum awareness
            "Endurance": {"base": 80, "std": 10},     # Sustaining quantum coherence over time
            "Speed": {"base": 100, "std": 0},         # Instantaneous action at a distance, influenced by quantum entanglement
            "Adaptability": {"base": 80, "std": 10},  # Rapid adjustment to new environments, based on quantum superposition
            "Camouflage": {"base": 80, "std": 10},    # Ability to blend into environments using quantum effects
            "Aquatic Adaptation": {"base": 50, "std": 20}, # Interactions with environments, not specifically aquatic
            "Thermal Resistance": {"base": 70, "std": 15}, # Tolerance to temperature at a quantum level
            "Radiation Resistance": {"base": 80, "std": 10}, # Withstanding high levels of radiation using quantum effects
            "Photosynthetic Ability": {"base": 0, "std": 0}, # Not applicable
            "Regeneration": {"base": 90, "std": 10},  # Quantum-level self-reorganization and healing
            "Longevity": {"base": 100, "std": 0},     # Theoretical immortality at a quantum level
            "Reproductive Rate": {"base": 60, "std": 20}, # Hypothetical reproduction, possibly involving quantum replication
            "Sensory Range": {"base": 90, "std": 10}, # Extended sensory perception through quantum phenomena
            "Mental Fortitude": {"base": 80, "std": 10},  # Resistance to mental stress in a quantum realm
            "Physical Fortitude": {"base": 70, "std": 15}, # Physical resilience interpreted through quantum robustness
            "Ecosystem Impact": {"base": 60, "std": 20},  # Influence on and adaptation to a quantum ecosystem
            "Social Structure": {"base": 50, "std": 20},  # Hypothetical social organization within a quantum framework
            "Resource Utilization": {"base": 70, "std": 15}, # Efficiency in using quantum resources
            "Stealth": {"base": 80, "std": 10},        # Moving or existing undetected, aided by quantum indeterminacy
            "Flight Capability": {"base": 50, "std": 20},   # Potential for movement not bound by traditional physics
            "Immune System Strength": {"base": 90, "std": 5},
            "Nutritional Requirements": {"base": 20, "std": 10},
            "Pressure Resistance": {"base": 80, "std": 10},
            "Social Cooperation": {"base": 50, "std": 50},
            "Oxygen Utilization Efficiency": {"base": 100, "std": 0},
            "Vision Adaptation": {"base": 0, "std": 0},
            "Eco-Sensitivity": {"base": 15, "std": 5},
            "Predation Instincts": {"base": 50, "std": 25},
            "Toxin Resistance": {"base": 10, "std": 5},
            "Toxin Production": {"base": 0, "std": 0},
            "Navigation Skills": {"base": 80, "std": 10},
            "Offspring": {"base": 1, "std": 0},
        },
        "Radiation-Resistant": {
            "Height": {"base": 50, "std": 50},  # Height in meters
            "Mass": {"base": 50, "std": 50},  # Mass in kilograms
            "Intelligence": {"base": 10, "std": 10},  # Limited to adaptive behaviors and survival strategies
            "Strength": {"base": 30, "std": 20},      # Physical strength, relevant to structural integrity under radiation
            "Dexterity": {"base": 10, "std": 10},     # Limited to growth and movement capabilities
            "Constitution": {"base": 90, "std": 10},  # High robustness and resistance to radiation
            "Charisma": {"base": 5, "std": 5},        # Influence within microbial communities or ecosystems
            "Wisdom": {"base": 10, "std": 10},        # Environmental awareness and adaptation
            "Perception": {"base": 20, "std": 15},    # Sensory abilities, focusing on detecting environmental changes
            "Endurance": {"base": 80, "std": 10},     # Ability to sustain viability in high-radiation environments
            "Speed": {"base": 10, "std": 10},         # Movement rate, generally low for such organisms
            "Adaptability": {"base": 80, "std": 10},  # Capacity to adjust to various levels and types of radiation
            "Camouflage": {"base": 20, "std": 15},    # Ability to blend into their environments
            "Aquatic Adaptation": {"base": 30, "std": 20}, # Some may be adapted to aquatic environments
            "Thermal Resistance": {"base": 50, "std": 20}, # Resistance to temperature variations, which may accompany radiation
            "Radiation Resistance": {"base": 100, "std": 0}, # Maximum resistance to radiation
            "Photosynthetic Ability": {"base": 10, "std": 10}, # Limited to specific organisms
            "Regeneration": {"base": 70, "std": 15},  # Ability to repair radiation-induced damage
            "Longevity": {"base": 40, "std": 20},     # Lifespan, which can be variable
            "Reproductive Rate": {"base": 50, "std": 20}, # Reproduction efficiency under radiation stress
            "Sensory Range": {"base": 20, "std": 15}, # Range of sensory perception, mainly environmental
            "Mental Fortitude": {"base": 10, "std": 10},  # Resilience to environmental stresses
            "Physical Fortitude": {"base": 80, "std": 15}, # High resistance to physical damage from radiation
            "Ecosystem Impact": {"base": 40, "std": 20},  # Influence on ecosystems, particularly in radiation-affected areas
            "Social Structure": {"base": 5, "std": 5},  # Limited to interactions within microbial or ecological communities
            "Resource Utilization": {"base": 60, "std": 15}, # Efficiency in using available resources in radiation-affected environments
            "Stealth": {"base": 20, "std": 15},        # Ability to exist without detection, relevant in microbial communities
            "Flight Capability": {"base": 0, "std": 0},   # Not applicable
            "Immune System Strength": {"base": 90, "std": 5},
            "Nutritional Requirements": {"base": 20, "std": 10},
            "Pressure Resistance": {"base": 80, "std": 10},
            "Social Cooperation": {"base": 50, "std": 50},
            "Oxygen Utilization Efficiency": {"base": 100, "std": 0},
            "Vision Adaptation": {"base": 0, "std": 0},
            "Eco-Sensitivity": {"base": 15, "std": 5},
            "Predation Instincts": {"base": 50, "std": 25},
            "Toxin Resistance": {"base": 10, "std": 5},
            "Toxin Production": {"base": 0, "std": 0},
            "Navigation Skills": {"base": 80, "std": 10},
            "Offspring": {"base": 1, "std": 0},
        },
        "Temperature-Resistant": {
            "Height": {"base": 50, "std": 50},  # Height in meters
            "Mass": {"base": 50, "std": 50},  # Mass in kilograms
            "Intelligence": {"base": 10, "std": 10},  # Limited to basic survival instincts and adaptations
            "Strength": {"base": 40, "std": 20},      # Physical strength, relevant to structural integrity under extreme temperatures
            "Dexterity": {"base": 20, "std": 15},     # Limited movement capabilities
            "Constitution": {"base": 90, "std": 10},  # High robustness and resistance to extreme temperatures
            "Charisma": {"base": 5, "std": 5},        # Limited social interactions
            "Wisdom": {"base": 20, "std": 15},        # Environmental awareness and adaptation
            "Perception": {"base": 40, "std": 20},    # Sensory abilities, adapted to detect changes in extreme thermal environments
            "Endurance": {"base": 80, "std": 10},     # Ability to withstand extreme temperatures for prolonged periods
            "Speed": {"base": 10, "std": 10},         # Movement rate, often reduced due to environmental constraints
            "Adaptability": {"base": 70, "std": 15},  # Capacity to adjust to varying temperature extremes
            "Camouflage": {"base": 30, "std": 20},    # Ability to blend into thermal environments
            "Aquatic Adaptation": {"base": 50, "std": 20}, # Adaptation to thermal aquatic environments, like hot springs or polar waters
            "Thermal Resistance": {"base": 100, "std": 0}, # Maximum resistance to extreme temperatures
            "Radiation Resistance": {"base": 30, "std": 20}, # Variable resistance to radiation
            "Photosynthetic Ability": {"base": 20, "std": 20}, # Present in some thermophilic algae and bacteria
            "Regeneration": {"base": 40, "std": 20},  # Ability to recover from temperature-induced damage
            "Longevity": {"base": 50, "std": 20},     # Lifespan potential in extreme environments
            "Reproductive Rate": {"base": 40, "std": 20}, # Efficiency of reproduction under thermal stress
            "Sensory Range": {"base": 50, "std": 20}, # Sensory perception adapted to extreme thermal conditions
            "Mental Fortitude": {"base": 10, "std": 10},  # Psychological resilience to environmental stresses
            "Physical Fortitude": {"base": 90, "std": 10}, # High resistance to physical damage from extreme temperatures
            "Ecosystem Impact": {"base": 40, "std": 20},  # Influence on and adaptation to thermal ecosystems
            "Social Structure": {"base": 5, "std": 5},  # Limited to interactions within microbial communities
            "Resource Utilization": {"base": 60, "std": 15}, # Efficiency in using resources in extreme thermal environments
            "Stealth": {"base": 20, "std": 15},        # Limited applicability
            "Flight Capability": {"base": 0, "std": 0},   # Not applicable
            "Immune System Strength": {"base": 90, "std": 5},
            "Nutritional Requirements": {"base": 20, "std": 10},
            "Pressure Resistance": {"base": 80, "std": 10},
            "Social Cooperation": {"base": 50, "std": 50},
            "Oxygen Utilization Efficiency": {"base": 100, "std": 0},
            "Vision Adaptation": {"base": 0, "std": 0},
            "Eco-Sensitivity": {"base": 15, "std": 5},
            "Predation Instincts": {"base": 50, "std": 25},
            "Toxin Resistance": {"base": 10, "std": 5},
            "Toxin Production": {"base": 0, "std": 0},
            "Navigation Skills": {"base": 80, "std": 10},
            "Offspring": {"base": 1, "std": 0},
        },
        "Terrestrial": {
            "Height": {"base": 50, "std": 20},  # Height in meters
            "Mass": {"base": 50, "std": 20},  # Mass in kilograms
            "Intelligence": {"base": 50, "std": 20},  # Varies from simple instinctive behaviors to complex problem-solving in higher mammals
            "Strength": {"base": 50, "std": 20},      # Ranges from the minimal strength of small insects to the great power of large mammals
            "Dexterity": {"base": 50, "std": 20},     # Coordination and fine motor skills vary among species, from limited to highly skilled
            "Constitution": {"base": 60, "std": 20},  # Overall health and resistance to diseases, variable across species
            "Charisma": {"base": 30, "std": 20},      # Social influence and charm, significant in social animals
            "Wisdom": {"base": 40, "std": 20},        # Insight and judgment, more pronounced in species with complex social structures
            "Perception": {"base": 60, "std": 20},    # Sensory abilities adapted to terrestrial environments
            "Endurance": {"base": 50, "std": 20},     # Ability to sustain physical activity, varies from short bursts in some to long-distance migration in others
            "Speed": {"base": 50, "std": 20},         # Movement rate, covering a range from slow-moving species to fast predators
            "Adaptability": {"base": 50, "std": 20},  # Capacity to adjust to different terrestrial environments
            "Camouflage": {"base": 40, "std": 20},    # Ability to blend into terrestrial surroundings
            "Aquatic Adaptation": {"base": 20, "std": 20}, # Limited for most, except for amphibious species
            "Thermal Resistance": {"base": 50, "std": 20}, # Tolerance to temperature variations, higher in species adapted to extreme climates
            "Radiation Resistance": {"base": 30, "std": 20}, # Generally low, except for certain resilient species
            "Photosynthetic Ability": {"base": 0, "std": 0}, # Not applicable to animal life forms
            "Regeneration": {"base": 30, "std": 20}, # Varies from minor wound healing to limb regeneration in select species
            "Longevity": {"base": 50, "std": 20}, # Lifespan ranges widely, from a few days in some insects to over a century in some larger mammals
            "Reproductive Rate": {"base": 60, "std": 20}, # Reproduction speed varies from multiple generations per year to several years between births
            "Sensory Range": {"base": 60, "std": 20}, # Sensory perception adapted to land environments, from basic to highly developed
            "Mental Fortitude": {"base": 40, "std": 20}, # Psychological resilience, important in more complex animals
            "Physical Fortitude": {"base": 60, "std": 20}, # Physical robustness, higher in larger or well-adapted species
            "Ecosystem Impact": {"base": 50, "std": 20}, # Influence on terrestrial ecosystems, varies by species
            "Social Structure": {"base": 40, "std": 20}, # Social interactions, significant in herd, pack, or community-forming species
            "Resource Utilization": {"base": 50, "std": 20}, # Efficiency in using available resources, varies based on ecological niche
            "Stealth": {"base": 40, "std": 20}, # Ability to move undetected, important for predators and prey alike
            "Flight Capability": {"base": 20, "std": 20}, # Present in birds and some insects, not applicable to most terrestrial species
            "Immune System Strength": {"base": 90, "std": 5},
            "Nutritional Requirements": {"base": 20, "std": 10},
            "Pressure Resistance": {"base": 80, "std": 10},
            "Social Cooperation": {"base": 50, "std": 50},
            "Oxygen Utilization Efficiency": {"base": 100, "std": 0},
            "Vision Adaptation": {"base": 0, "std": 0},
            "Eco-Sensitivity": {"base": 15, "std": 5},
            "Predation Instincts": {"base": 50, "std": 25},
            "Toxin Resistance": {"base": 10, "std": 5},
            "Toxin Production": {"base": 0, "std": 0},
            "Navigation Skills": {"base": 80, "std": 10},
            "Offspring": {"base": 1, "std": 0},
            }
    }