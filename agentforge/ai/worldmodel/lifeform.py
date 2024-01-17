import numpy as np
import pandas as pd
import math
from .star import Star
from .concept import Concept

class Lifeform:
    
    def __init__(self):
        self.star = Star()
        self.life_form_characteristic_names = list(set(b for biomes in self.life_form_characteristics.values() for b in biomes))
        self.life_form_categories = list(self.life_form_metadata.keys())

        # Create concepts for each planet type
        self.biologic_concepts = {}
        for biologic_type in self.life_form_categories:
            self.biologic_concepts[biologic_type] = Concept(biologic_type, "Biological")
            for key, value in self.life_form_metadata[biologic_type].items():
                self.biologic_concepts[biologic_type].update_metadata(key, value)

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

    life_form_metadata = {
        "AI": {
            "Computational Ability": "Highly advanced, capable of processing vast amounts of data",
            "Communication": "Digital interfaces, possibly capable of human-like interaction",
            "Sensory Perception": "Advanced sensors for a wide range of environmental inputs",
            "Reproduction": "Non-biological, through manufacturing or self-replication algorithms",
            "Evolution": "Software updates and hardware upgrades rather than biological evolution"
        },
        "Amorphous": {
            "Morphology": "Capable of changing shape in response to environmental stimuli",
            "Sensory Perception": "Likely rudimentary, based on direct environmental interaction",
            "Reproduction": "Could involve splitting or amalgamating with similar life forms",
            "Evolution": "Adaptation through mutation or environmental assimilation",
            "Movement": "Locomotion through flowing, oozing, or other non-standard methods"
        },
        "Aquatic": {
            "Physiological Adaptations": "Gills for underwater breathing, streamlined bodies for efficient swimming",
            "Sensory Perception": "Adapted for underwater environments, like enhanced vision or echolocation",
            "Reproduction": "Variety of reproductive strategies, from spawning to live birth",
            "Social Structure": "Ranges from solitary to complex social groups",
            "Diet": "Diverse, from planktonic organisms to larger marine animals"
        },
        "Cold-Tolerant Fauna": {
            "Physiological Adaptations": "Antifreeze proteins, insulating layers, reduced metabolic rates",
            "Growth Patterns": "Slow growth rates, possibly with dormancy periods",
            "Reproduction": "Adapted to short growing seasons, with rapid lifecycle stages",
            "Survival Strategy": "Adaptations to conserve energy and resources",
            "Ecological Interactions": "Specialized roles in cold ecosystems"
        },
        "Cold-Tolerant Flora": {
            "Physiological Adaptations": "Antifreeze properties, slow metabolic processes",
            "Growth Patterns": "Adapted to harsh, cold conditions with limited growing periods",
            "Reproduction": "Efficient seed dispersal mechanisms for short growing seasons",
            "Survival Strategy": "Energy conservation and resilience in extreme cold",
            "Ecological Role": "Supporting cold ecosystems, often forming the basis of the food web"
        },
        "Crystalline": {
            "Structural Formation": "Growth through mineral deposition, possibly geometric structures",
            "Energy Utilization": "Likely photosynthetic or chemosynthetic",
            "Interaction with Environment": "Absorption and reflection of light, possible piezoelectric properties",
            "Growth": "Could be slow and dependent on environmental mineral availability",
            "Resilience": "High structural strength but potentially brittle"
        },
        "Electromagnetic": {
            "Existence": "Manifestation in electromagnetic fields, possibly invisible to the naked eye",
            "Interaction": "Influence over electronic devices, communication via electromagnetic waves",
            "Energy Utilization": "Absorbing and manipulating ambient electromagnetic energy",
            "Movement": "Unbound by physical barriers, potentially high-speed travel along electromagnetic lines",
            "Perception": "Sensing the world in terms of electromagnetic fields and currents"
        },
        "Flora": {
            "Photosynthesis": "Conversion of sunlight into energy, with oxygen as a byproduct",
            "Growth": "Adapted to specific ecological niches, from deep shade to full sunlight",
            "Reproduction": "From seeds to spores, with various dispersal mechanisms",
            "Interaction with Fauna": "Ranging from mutualistic relationships to defensive strategies against herbivores",
            "Adaptability": "Specialization to local environments, from deserts to rainforests"
        },
        "Gaseous": {
            "Form": "Existing as a cloud or nebulous entity, diffuse and expansive",
            "Sensory Mechanism": "Possibly sensing changes in pressure, temperature, and chemical composition",
            "Interaction": "Difficult to interact with physical objects but may influence gas and airflow dynamics",
            "Movement": "Capable of drifting or flowing with air currents, possibly controlling its own density and distribution",
            "Survival Mechanism": "May rely on atmospheric gases for sustenance, possibly through a form of gas absorption"
        },
        "Mixed-Traits Fauna": {
            "Hybrid Physiology": "Combination of traits from different species, leading to unique adaptations",
            "Genetic Diversity": "High genetic variability offering a broad range of survival strategies",
            "Reproduction": "Potentially complex, combining various reproductive methods",
            "Ecological Role": "Fulfilling multiple niches within ecosystems due to their mixed traits",
            "Adaptation": "Rapid response to environmental changes due to varied genetic makeup"
        },
        "Mixed-Traits Flora": {
            "Hybrid Physiology": "Combination of traits from various plant species",
            "Genetic Diversity": "Enhanced adaptability and resilience due to diverse genetic makeup",
            "Reproduction": "Diverse mechanisms, possibly combining traits from different species",
            "Ecological Role": "Filling multiple ecological niches, contributing to biodiversity",
            "Adaptation": "Capable of thriving in varied environmental conditions"
            },
        "Plasma": {
            "State of Matter": "Existing in a high-energy state beyond gas, composed of ionized particles",
            "Energy Interaction": "Interaction with magnetic and electric fields, possibly emitting light",
            "Form Stability": "Maintaining coherence in environments with sufficient energy",
            "Energy Requirement": "High energy needed to sustain the plasma state",
            "Environmental Impact": "Potential to influence or be influenced by high-energy phenomena"
            },
        "Pressure-Resistant": {
            "Structural Adaptations": "Robust physical structures to withstand high-pressure environments",
            "Sensory Adaptations": "Sensory organs adapted to function under extreme pressure",
            "Movement": "Mechanisms to navigate effectively in high-pressure conditions",
            "Habitat": "Likely found in deep-sea environments or other high-pressure ecological niches",
            "Interaction with Other Life": "Adapted to interact with similarly pressure-adapted organisms"
            },
        "Quantum": {
            "Existence": "Operating on quantum principles, possibly exhibiting phenomena like superposition or entanglement",
            "Perception": "Potentially perceiving and interacting with the environment at a quantum level",
            "Energy Utilization": "Utilizing quantum states or fluctuations for energy",
            "Communication": "Possibly capable of non-local communication through quantum entanglement",
            "Adaptation": "Thriving in environments where quantum effects are pronounced"
            },
        "Radiation-Resistant": {
            "Cellular Adaptations": "Robust DNA repair mechanisms and radiation shielding",
            "Habitat": "Thriving in radiation-rich environments, such as near radioactive materials or in space",
            "Reproduction": "Mechanisms to protect genetic material from radiation damage",
            "Ecological Role": "Potentially playing a key role in ecosystems with high radiation levels",
            "Survival Strategy": "Utilizing radiation as an energy source or for mutation and adaptation"
        },
        "Robotic": {
            "Construction": "Built from durable materials, designed for specific functions",
            "Power Source": "Various, from batteries to solar cells",
            "Sensory Systems": "Advanced sensors for a range of environmental inputs",
            "Control": "Operated by programming or AI, with varying degrees of autonomy",
            "Adaptation": "Modular design allowing for hardware upgrades and functional changes"
        },
        "Temperature-Resistant": {
            "Structural Adaptations": "Robust physical structures to withstand high-pressure environments",
            "Sensory Adaptations": "Sensory organs adapted to function under extreme pressure",
            "Movement": "Mechanisms to navigate effectively in high-pressure conditions",
            "Habitat": "Likely found in deep-sea environments or other high-pressure ecological niches",
            "Interaction with Other Life": "Adapted to interact with similarly pressure-adapted organisms"
        },
        "Terrestrial": {
            "Structural Adaptations": "Limbs for movement on land, organs adapted for air breathing",
            "Sensory Adaptations": "Senses tuned for detecting stimuli in a terrestrial environment",
            "Reproduction": "Diverse methods, from egg-laying to live birth",
            "Social Interaction": "Varied, from solitary to complex social structures",
            "Dietary Needs": "Adapted to consume land-based food sources"
        }
    }

    life_form_characteristics = {
        "AI": {
            "Intelligence": {"base": 90, "std": 5},
            "Strength": {"base": 70, "std": 15},  # Interpreted as computational power
            "Dexterity": {"base": 30, "std": 10}, # Fine control in digital environments
            "Constitution": {"base": 80, "std": 10}, # System robustness and error resilience
            "Charisma": {"base": 40, "std": 20}, # AI's ability to interact effectively with humans
            "Wisdom": {"base": 85, "std": 10}, # Data-driven insights and decision making
            "Perception": {"base": 80, "std": 10}, # Sensory data processing
            "Endurance": {"base": 90, "std": 5}, # Operational longevity
            "Speed": {"base": 95, "std": 5}, # Processing and response time
            "Adaptability": {"base": 60, "std": 15}, # Flexibility in learning and tasks
            "Camouflage": {"base": 10, "std": 5}, # Not typically applicable
            "Aquatic Adaptation": {"base": 10, "std": 5}, # Not typically applicable
            "Thermal Resistance": {"base": 50, "std": 20}, # Tolerance to hardware temperature variations
            "Radiation Resistance": {"base": 50, "std": 20}, # Tolerance to electromagnetic interference
            "Photosynthetic Ability": {"base": 0, "std": 0}, # Not applicable
            "Regeneration": {"base": 70, "std": 15}, # Ability to recover from errors or data corruption
            "Longevity": {"base": 80, "std": 10}, # Lifespan of software before becoming obsolete
            "Reproductive Rate": {"base": 80, "std": 10}, # Speed of replication or copying of software
            "Sensory Range": {"base": 80, "std": 10}, # Range of input types and sensors it can process
            "Mental Fortitude": {"base": 90, "std": 5}, # Resistance to hacking or external manipulation
            "Physical Fortitude": {"base": 70, "std": 15}, # Durability of physical hardware
            "Ecosystem Impact": {"base": 40, "std": 20}, # Influence on digital or physical environments
            "Social Structure": {"base": 20, "std": 10}, # Degree of interaction with other AIs or systems
            "Resource Utilization": {"base": 60, "std": 15}, # Efficiency in using computational resources
            "Stealth": {"base": 30, "std": 15}, # Ability to operate without detection in digital environments
            "Flight Capability": {"base": 10, "std": 5} # Not typically applicable
        },
      "Amorphous": {
            "Intelligence": {"base": 20, "std": 10},  # Limited cognitive abilities
            "Strength": {"base": 30, "std": 15},      # Force exertion in environment
            "Dexterity": {"base": 50, "std": 20},     # Shape manipulation and movement
            "Constitution": {"base": 70, "std": 10},  # Resilience and health
            "Charisma": {"base": 5, "std": 5},        # Limited social influence
            "Wisdom": {"base": 20, "std": 10},        # Basic environmental awareness
            "Perception": {"base": 40, "std": 15},    # Sensing environmental changes
            "Endurance": {"base": 60, "std": 20},     # Sustaining activity
            "Speed": {"base": 20, "std": 10},         # Movement rate
            "Adaptability": {"base": 80, "std": 10},  # Adjusting to environments
            "Camouflage": {"base": 70, "std": 15},    # Blending with surroundings
            "Aquatic Adaptation": {"base": 60, "std": 20}, # Functioning in water
            "Thermal Resistance": {"base": 50, "std": 20}, # Tolerance to temperatures
            "Radiation Resistance": {"base": 40, "std": 20}, # Withstanding radiation
            "Photosynthetic Ability": {"base": 0, "std": 0}, # Generally not applicable
            "Regeneration": {"base": 80, "std": 10},  # Healing or regrowth
            "Longevity": {"base": 50, "std": 20},     # Lifespan potential
            "Reproductive Rate": {"base": 80, "std": 10}, # Reproduction efficiency
            "Sensory Range": {"base": 40, "std": 15}, # Sensory perception extent
            "Mental Fortitude": {"base": 20, "std": 10},  # Resistance to mental stress
            "Physical Fortitude": {"base": 70, "std": 15}, # Resistance to physical damage
            "Ecosystem Impact": {"base": 40, "std": 20},  # Influence on the ecosystem
            "Social Structure": {"base": 10, "std": 10},  # Social interaction complexity
            "Resource Utilization": {"base": 60, "std": 20}, # Efficiency in resource use
            "Stealth": {"base": 70, "std": 15},      # Moving without detection
            "Flight Capability": {"base": 0, "std": 0}   # Not applicable
        },
        "Aquatic": {
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
            "Flight Capability": {"base": 0, "std": 0}   # Not applicable in traditional sense
        },
        "Cold-Tolerant Fauna": {
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
            "Flight Capability": {"base": 10, "std": 10}   # Limited to certain bird species
        },
        "Cold-Tolerant Flora": {
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
            "Flight Capability": {"base": 1, "std": 1}   # Limited to seed dispersal
        },
        "Gaseous": {
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
            "Flight Capability": {"base": 100, "std": 0}   # Innate ability to float or drift
        },
        "Plasma": {
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
            "Flight Capability": {"base": 100, "std": 0}   # Innate floating or flying ability
        },
        "Crystalline": {
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
            "Flight Capability": {"base": 0, "std": 0}   # Not applicable
        },
        "Electromagnetic": {
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
            "Flight Capability": {"base": 80, "std": 10}   # Manipulating electromagnetic fields for movement
        },
        "Flora": {
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
            "Flight Capability": {"base": 1, "std": 1}   # Limited to seed dispersal
        },
        "Mixed-Traits Fauna": {
            "Intelligence": {"base": 50, "std": 15},  # Reflecting a range of animal cognitive abilities
            "Strength": {"base": 70, "std": 20},      # Combining various levels of muscular force
            "Dexterity": {"base": 60, "std": 20},     # Agility from different species
            "Constitution": {"base": 70, "std": 15},  # Overall health and stamina from a mix of species
            "Charisma": {"base": 40, "std": 20},      # Social influence, varying widely
            "Wisdom": {"base": 55, "std": 15},        # Insight and judgment from multiple animal perspectives
            "Perception": {"base": 70, "std": 15},    # Sensory abilities from various animals
            "Endurance": {"base": 65, "std": 20},     # Sustaining physical activity, a median of different traits
            "Speed": {"base": 60, "std": 20},         # Movement rate, balancing fast and slow species
            "Adaptability": {"base": 60, "std": 15},  # Capacity to adjust, influenced by various habitats
            "Camouflage": {"base": 50, "std": 20},    # Ability to blend in, depending on the traits
            "Aquatic Adaptation": {"base": 40, "std": 20}, # Underwater abilities, if aquatic traits are present
            "Thermal Resistance": {"base": 50, "std": 20}, # Tolerance to temperatures, depending on mixed traits
            "Radiation Resistance": {"base": 30, "std": 20}, # Varying levels based on the species mix
            "Photosynthetic Ability": {"base": 10, "std": 10}, # Rare, but possible in a hypothetical scenario
            "Regeneration": {"base": 40, "std": 20},  # Healing abilities, depending on the species
            "Longevity": {"base": 60, "std": 20},     # Lifespan potential, averaging different species
            "Reproductive Rate": {"base": 50, "std": 20}, # Reproduction speed, based on mixed traits
            "Sensory Range": {"base": 70, "std": 15}, # Extent of sensory perception, combining various species
            "Mental Fortitude": {"base": 50, "std": 20},  # Resistance to mental stress, variable
            "Physical Fortitude": {"base": 70, "std": 15}, # Resistance to physical damage, based on mixed traits
            "Ecosystem Impact": {"base": 50, "std": 20},  # Influence on or adaptation to ecosystems
            "Social Structure": {"base": 40, "std": 20},  # Complexity of social interactions, variable
            "Resource Utilization": {"base": 60, "std": 15}, # Efficiency in using available resources
            "Stealth": {"base": 50, "std": 20},        # Ability to move or exist without detection
            "Flight Capability": {"base": 30, "std": 20}   # Potential for flight, if avian traits are included
        },
        "Mixed-Traits Flora": {
            "Intelligence": {"base": 1, "std": 1},  # Limited to adaptive responses, not cognitive intelligence
            "Strength": {"base": 40, "std": 20},    # Structural strength, combining traits like vine flexibility and tree sturdiness
            "Dexterity": {"base": 1, "std": 1},     # Limited to growth patterns, not active movement
            "Constitution": {"base": 70, "std": 15}, # Overall health, combining resilience traits from various plants
            "Charisma": {"base": 30, "std": 15},    # Influence on pollinators, seed dispersers, and symbiotic relationships
            "Wisdom": {"base": 1, "std": 1},        # Environmental adaptation and responses
            "Perception": {"base": 1, "std": 1},    # Basic environmental sensing, like phototropism
            "Endurance": {"base": 80, "std": 10},   # Long-term survival, integrating traits like drought resistance
            "Speed": {"base": 1, "std": 1},         # Growth rate, with some species potentially having rapid growth
            "Adaptability": {"base": 70, "std": 15}, # Adaptation to various environments, from aquatic to desert
            "Camouflage": {"base": 50, "std": 20},  # Ability to blend in with the environment, like mimicking surrounding flora
            "Aquatic Adaptation": {"base": 50, "std": 20}, # Adaptations for water, like floating or submerged growth
            "Thermal Resistance": {"base": 60, "std": 20}, # Tolerance to temperature variations
            "Radiation Resistance": {"base": 40, "std": 20}, # Resistance to UV or other radiation, like in high-altitude plants
            "Photosynthetic Ability": {"base": 80, "std": 15}, # Enhanced or varied photosynthesis mechanisms
            "Regeneration": {"base": 60, "std": 20},  # Ability to regrow parts, combining traits like rapid healing or sprouting
            "Longevity": {"base": 70, "std": 20},     # Lifespan, combining annuals and perennials
            "Reproductive Rate": {"base": 60, "std": 20}, # Various reproductive strategies, from seeds to spores
            "Sensory Range": {"base": 1, "std": 1},   # Limited to basic environmental responses
            "Mental Fortitude": {"base": 1, "std": 1},  # Not applicable
            "Physical Fortitude": {"base": 70, "std": 15}, # Physical resilience, combining traits from different species
            "Ecosystem Impact": {"base": 60, "std": 20},  # Influence on the ecosystem, potentially combining roles like nitrogen-fixing and shading
            "Social Structure": {"base": 1, "std": 1},  # Interaction with other plants and organisms, like in a forest understory
            "Resource Utilization": {"base": 70, "std": 15}, # Efficient use of resources like light, water, and nutrients
            "Stealth": {"base": 1, "std": 1},         # Not applicable
            "Flight Capability": {"base": 1, "std": 1}   # Limited to seed dispersal mechanisms
        },
        "Pressure-Resistant": {
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
            "Flight Capability": {"base": 10, "std": 10} # Limited to swimming capabilities, not traditional flight
        },
        "Quantum": {
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
            "Flight Capability": {"base": 50, "std": 20}   # Potential for movement not bound by traditional physics
        },
        "Radiation-Resistant": {
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
            "Flight Capability": {"base": 0, "std": 0}   # Not applicable
        },
        "Robotic": {
            "Intelligence": {"base": 70, "std": 20},  # Depending on AI sophistication and programming
            "Strength": {"base": 80, "std": 15},      # Mechanical strength, varies based on design
            "Dexterity": {"base": 70, "std": 20},     # Precision and coordination in tasks
            "Constitution": {"base": 80, "std": 15},  # Durability and resilience to damage
            "Charisma": {"base": 40, "std": 20},      # Ability to interact with humans or other robots
            "Wisdom": {"base": 60, "std": 20},        # Decision-making abilities, based on programming
            "Perception": {"base": 80, "std": 15},    # Sensory capabilities, including advanced sensors
            "Endurance": {"base": 90, "std": 10},     # Ability to operate continuously without fatigue
            "Speed": {"base": 60, "std": 20},         # Movement speed, depending on design
            "Adaptability": {"base": 70, "std": 15},  # Flexibility in programming to handle different tasks
            "Camouflage": {"base": 30, "std": 20},    # Some may have stealth features
            "Aquatic Adaptation": {"base": 40, "std": 20}, # Waterproofing and underwater operation in some designs
            "Thermal Resistance": {"base": 70, "std": 15}, # Tolerance to temperature extremes
            "Radiation Resistance": {"base": 80, "std": 10}, # Shielding against radiation
            "Photosynthetic Ability": {"base": 20, "std": 15}, # Solar power capabilities in some models
            "Regeneration": {"base": 20, "std": 20},  # Limited self-repair capabilities
            "Longevity": {"base": 80, "std": 10},     # Long operational lifespan
            "Reproductive Rate": {"base": 0, "std": 0}, # Not applicable
            "Sensory Range": {"base": 90, "std": 10}, # Wide range of sensors for environmental detection
            "Mental Fortitude": {"base": 100, "std": 0},  # Immunity to psychological stress
            "Physical Fortitude": {"base": 80, "std": 15}, # Resistance to physical damage
            "Ecosystem Impact": {"base": 50, "std": 20},  # Influence on environments, depending on application
            "Social Structure": {"base": 30, "std": 20},  # Varies based on networked intelligence and roles
            "Resource Utilization": {"base": 70, "std": 15}, # Efficiency in energy and resource usage
            "Stealth": {"base": 40, "std": 20},        # Capabilities for stealth operations in some models
            "Flight Capability": {"base": 50, "std": 20}   # Flight abilities in certain drone-like robots
        },
        "Temperature-Resistant": {
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
            "Flight Capability": {"base": 0, "std": 0}   # Not applicable
        },
        "Terrestrial": {
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
            "Flight Capability": {"base": 20, "std": 20} # Present in birds and some insects, not applicable to most terrestrial species
            }
    }
