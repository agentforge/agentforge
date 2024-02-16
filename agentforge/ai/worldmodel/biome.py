import math
from .concept import Concept, ensure_non_negative_and_normalize_row
from .lifeform import Lifeform
from agentforge.ai.worldmodel.evolution import EvolutionarySimulation
import numpy as np

class Biome:
    def __init__(self) -> None:
        self.lifeform = Lifeform()
        
        # Create concepts for each planet type
        self.biome_concepts = {}
        for biome_type in self.biomes:
            self.biome_concepts[biome_type] = Concept(biome_type, "Biome")

        # Extracting unique biology subcategories from biome_biology_probabilities
        unique_biology_subcategories = list(set(subcat for biomes in self.biome_biology_probabilities.values() for subcat in biomes))

        # Update biome_concepts with connections to biology subcategories including probabilities
        for biome_type, subcategory_probs in self.biome_biology_probabilities.items():
            for subcategory, probability in subcategory_probs.items():
                self.biome_concepts[biome_type].add_connection(subcategory, probability)

    def evolve_for_biome(self, planet_info, biome_type, normalized_bx_b_df, normalized_bx_lf_df):
        lifeforms = []
        biome_quotient = self.biome_biological_support[biome_type]['biological_diversity_quotient']
        biome_supported_species = math.ceil(25 * biome_quotient)
        biome_index = self.biomes.index(biome_type)

        for _ in range(biome_supported_species):
            biological_probabilities = normalized_bx_b_df.iloc[biome_index]
            biological_type = np.random.choice(self.lifeform.life_form_categories, p=biological_probabilities)

            biological_index = self.lifeform.life_form_categories.index(biological_type)

            life_form_characteristic_probabilities = normalized_bx_lf_df.iloc[biological_index]
            adjusted_probabilities = ensure_non_negative_and_normalize_row(life_form_characteristic_probabilities)
            life_form_characteristic_list = list(set(np.random.choice(self.lifeform.life_form_characteristic_names, p=adjusted_probabilities, size=5)))

            bio_info = {
                "Biological Type": biological_type,
                "Life Form Attributes": life_form_characteristic_list,
                "Genetic Profile": self.lifeform.sample_genetic_profile(biological_type),
            }

            lifeforms.append(bio_info)

        print("evolving life {} for {} ({})".format(len(lifeforms), planet_info['Planet Type'], biome_type))
        origin_of_species = EvolutionarySimulation(planet_info['Planet Type'], biome_type, planet_info['uuid'])
        evolutionary_report = origin_of_species.run(lifeforms)

        # Now update the planet/biome with the new life forms
        return evolutionary_report

    biomes = ["Forest", 
        "Desert", 
        "Ocean", 
        "Tundra", 
        "Grassland", 
        "Wetlands", 
        "Savanna", 
        "Taiga", 
        "Chaparral", 
        "Temperate Deciduous Forest", 
        "Temperate Rainforest", 
        "Mediterranean", 
        "Montane (Alpine)",
        "Coral Reefs", 
        "Mangroves",
        "Silicon-based", 
        "Ammonia-based", 
        "Lava", 
        "Ice", 
        "Super-Earth Oceanic", 
        "Carbon-rich", 
        "Iron-rich",
        "Helium-rich", 
        "Sulfuric Acid Cloud", 
        "Chlorine-based Atmosphere", 
        "Hydrocarbon Lakes", 
        "Supercritical Fluid", 
        "Subsurface Ocean"
    ]

    # Probabilities for life form subcategories in different biomes
    biome_biology_probabilities = {
        "Forest": {
            'Aquatic': 0.05, 'Terrestrial': 0.20, 'Flora': 0.30,
            'Crystalline': 0.00, 'Amorphous': 0.0001,
            'Cold-Tolerant Fauna': 0.02, 'Cold-Tolerant Flora': 0.03,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.00, 'Quantum': 0.00,
            'Radiation-Resistant': 0.00, 'Pressure-Resistant': 0.00, 'Temperature-Resistant': 0.00,
        },
        "Desert": {
            'Aquatic': 0.00, 'Terrestrial': 0.25, 'Flora': 0.15,
            'Crystalline': 0.00, 'Amorphous': 0.0001,
            'Cold-Tolerant Fauna': 0.01, 'Cold-Tolerant Flora': 0.01,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.00, 'Quantum': 0.00,
            'Radiation-Resistant': 0.00, 'Pressure-Resistant': 0.00, 'Temperature-Resistant': 0.00,
        },
        "Ocean": {
            'Aquatic': 0.30, 'Terrestrial': 0.00, 'Flora': 0.25,
            'Crystalline': 0.00, 'Amorphous': 0.0001,
            'Cold-Tolerant Fauna': 0.05, 'Cold-Tolerant Flora': 0.05,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.00, 'Quantum': 0.0001,
            'Radiation-Resistant': 0.00, 'Pressure-Resistant': 0.00, 'Temperature-Resistant': 0.00,
            },
        "Tundra": {
            'Aquatic': 0.05, 'Terrestrial': 0.15, 'Flora': 0.10,
            'Crystalline': 0.00, 'Amorphous': 0.0001,
            'Cold-Tolerant Fauna': 0.20, 'Cold-Tolerant Flora': 0.20,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.00, 'Quantum': 0.0001,
            'Radiation-Resistant': 0.00, 'Pressure-Resistant': 0.00, 'Temperature-Resistant': 0.00,
            },
        "Grassland": {
            'Aquatic': 0.03, 'Terrestrial': 0.25, 'Flora': 0.25,
            'Crystalline': 0.00, 'Amorphous': 0.0001,
            'Cold-Tolerant Fauna': 0.02, 'Cold-Tolerant Flora': 0.02,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.00, 'Quantum': 0.0001,
            'Radiation-Resistant': 0.00, 'Pressure-Resistant': 0.00, 'Temperature-Resistant': 0.00,
            },
        "Wetlands": {
            'Aquatic': 0.20, 'Terrestrial': 0.15, 'Flora': 0.20,
            'Crystalline': 0.00, 'Amorphous': 0.0001,
            'Cold-Tolerant Fauna': 0.03, 'Cold-Tolerant Flora': 0.03,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.00, 'Quantum': 0.0001,
            'Radiation-Resistant': 0.00, 'Pressure-Resistant': 0.00, 'Temperature-Resistant': 0.00,
            },
        "Savanna": {
            'Aquatic': 0.02, 'Terrestrial': 0.30,'Flora': 0.20,
            'Crystalline': 0.00, 'Amorphous': 0.0001,
            'Cold-Tolerant Fauna': 0.01, 'Cold-Tolerant Flora': 0.01,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.00, 'Quantum': 0.0001,
            'Radiation-Resistant': 0.00, 'Pressure-Resistant': 0.00, 'Temperature-Resistant': 0.00,
            },
        "Taiga": {
            'Aquatic': 0.03, 'Terrestrial': 0.20, 'Flora': 0.25,
            'Crystalline': 0.00, 'Amorphous': 0.0001,
            'Cold-Tolerant Fauna': 0.15, 'Cold-Tolerant Flora': 0.15,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.00, 'Quantum': 0.0001,
            'Radiation-Resistant': 0.00, 'Pressure-Resistant': 0.00, 'Temperature-Resistant': 0.00,
            },
        "Chaparral": {
            'Aquatic': 0.01, 'Terrestrial': 0.30, 'Flora': 0.20,
            'Crystalline': 0.00, 'Amorphous': 0.0001,
            'Cold-Tolerant Fauna': 0.01, 'Cold-Tolerant Flora': 0.01,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.00, 'Quantum': 0.0001,
            'Radiation-Resistant': 0.00, 'Pressure-Resistant': 0.00, 'Temperature-Resistant': 0.00,
            },
        "Temperate Deciduous Forest": {
            'Aquatic': 0.10, 'Terrestrial': 0.20, 'Flora': 0.25,
            'Crystalline': 0.00, 'Amorphous': 0.0001,
            'Cold-Tolerant Fauna': 0.05, 'Cold-Tolerant Flora': 0.05,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.00, 'Quantum': 0.0001,
            'Radiation-Resistant': 0.00, 'Pressure-Resistant': 0.00, 'Temperature-Resistant': 0.00,
        },
        "Temperate Rainforest": {
            'Aquatic': 0.15, 'Terrestrial': 0.15, 'Flora': 0.20,
            'Crystalline': 0.00, 'Amorphous': 0.0001,
            'Cold-Tolerant Fauna': 0.06, 'Cold-Tolerant Flora': 0.06,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.00, 'Quantum': 0.0001,
            'Radiation-Resistant': 0.00, 'Pressure-Resistant': 0.00, 'Temperature-Resistant': 0.00,
        },
        "Mediterranean": {
            'Aquatic': 0.10, 'Terrestrial': 0.20, 'Flora': 0.25,
            'Crystalline': 0.00, 'Amorphous': 0.0001,
            'Cold-Tolerant Fauna': 0.02, 'Cold-Tolerant Flora': 0.02,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.00, 'Quantum': 0.0001,
            'Radiation-Resistant': 0.00, 'Pressure-Resistant': 0.00, 'Temperature-Resistant': 0.00,
        },
        "Montane (Alpine)": {
            'Aquatic': 0.05, 'Terrestrial': 0.20, 'Flora': 0.25, 
            'Crystalline': 0.00, 'Amorphous': 0.0001,
            'Cold-Tolerant Fauna': 0.10, 'Cold-Tolerant Flora': 0.10, 
            'Gaseous': 0.00, 'Plasma': 0.00, 
            'Electromagnetic': 0.00, 'Quantum': 0.0001,
            'Radiation-Resistant': 0.00, 'Pressure-Resistant': 0.00, 'Temperature-Resistant': 0.00,
        },
        "Coral Reefs": {
            'Aquatic': 0.30, 'Terrestrial': 0.00, 'Flora': 0.20,
            'Crystalline': 0.00, 'Amorphous': 0.0001,
            'Cold-Tolerant Fauna': 0.00, 'Cold-Tolerant Flora': 0.00,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.00, 'Quantum': 0.0001,
            'Radiation-Resistant': 0.00, 'Pressure-Resistant': 0.00, 'Temperature-Resistant': 0.00,
        },
        "Mangroves": {
            'Aquatic': 0.15, 'Terrestrial': 0.15, 'Flora': 0.20,
            'Crystalline': 0.00, 'Amorphous': 0.0001,
            'Cold-Tolerant Fauna': 0.05, 'Cold-Tolerant Flora': 0.05,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.00, 'Quantum': 0.0001,
            'Radiation-Resistant': 0.00, 'Pressure-Resistant': 0.00, 'Temperature-Resistant': 0.00,
        },
        "Silicon-based": {
            'Aquatic': 0.0, 'Terrestrial': 0.0, 'Flora': 0.0,
            'Crystalline': 0.35, 'Amorphous': 0.35,  # Dominant Silicon-Based life forms
            'Cold-Tolerant Fauna': 0, 'Cold-Tolerant Flora': 0,
            'Gaseous': 0.05, 'Plasma': 0.05,  # Possible Non-Solvent-Based life forms
            'Electromagnetic': 0.05, 'Quantum': 0.05,  # Some potential for Energy Beings
            'Radiation-Resistant': 0, 'Pressure-Resistant': 0, 'Temperature-Resistant': 0,
        },
        "Ammonia-based": {
            'Aquatic': 0.0, 'Terrestrial': 0.0, 'Flora': 0.0,
            'Cold-Tolerant Fauna': 0.4, 'Cold-Tolerant Flora': 0.4,  # Dominant Ammonia-Based life forms
            'Crystalline': 0, 'Amorphous': 0,
            'Gaseous': 0, 'Plasma': 0,
            'Electromagnetic': 0.05, 'Quantum': 0.05,  # Some potential for Energy Beings
            'Radiation-Resistant': 0.025, 'Pressure-Resistant': 0.025, 'Temperature-Resistant': 0.025,
        },
        "Lava": {
            'Aquatic': 0.0, 'Terrestrial': 0.0, 'Flora': 0.0,
            'Crystalline': 0.05, 'Amorphous': 0.05,  # Silicon-Based life forms in harsh conditions
            'Cold-Tolerant Fauna': 0, 'Cold-Tolerant Flora': 0,
            'Gaseous': 0, 'Plasma': 0,
            'Electromagnetic': 0.05, 'Quantum': 0.05,  # Some potential for Energy Beings
            'Radiation-Resistant': 0.1, 'Pressure-Resistant': 0.1, 'Temperature-Resistant': 0.1,  # Extremophiles suited for harsh lava conditions
        },
        "Ice": {
            'Aquatic': 0.0, 'Terrestrial': 0.0, 'Flora': 0.0,  # Some Carbon-Based life possible
            'Cold-Tolerant Fauna': 0.3, 'Cold-Tolerant Flora': 0.3,  # Suitable for Ammonia-Based life
            'Crystalline': 0.01, 'Amorphous': 0,  # Silicon-Based life unlikely
            'Gaseous': 0, 'Plasma': 0,  # Non-Solvent-Based life unlikely
            'Electromagnetic': 0.05, 'Quantum': 0.05,  # Potential for Energy Beings
            'Radiation-Resistant': 0.10, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.5,  # Extremophiles adapted to cold
        },
        "Super-Earth Oceanic": {
            'Aquatic': 0.35, 'Terrestrial': 0.00, 'Flora': 0.15,  # Dominant Carbon-Based life
            'Crystalline': 0, 'Amorphous': 0,  # Silicon-Based life unlikely
            'Cold-Tolerant Fauna': 0.05, 'Cold-Tolerant Flora': 0.05,  # Some Ammonia-Based life possible
            'Gaseous': 0, 'Plasma': 0,  # Non-Solvent-Based life unlikely
            'Electromagnetic': 0.05, 'Quantum': 0.05,  # Some Energy Beings potential
            'Radiation-Resistant': 0.0025, 'Pressure-Resistant': 0.0025, 'Temperature-Resistant': 0.0025,  # Some extremophiles
        },
        "Carbon-rich": {
            'Aquatic': 0.30, 'Terrestrial': 0.35, 'Flora': 0.15,  # High probability for Carbon-Based life
            'Crystalline': 0, 'Amorphous': 0,  # Silicon-Based life unlikely
            'Cold-Tolerant Fauna': 0, 'Cold-Tolerant Flora': 0,  # Ammonia-Based life unlikely
            'Gaseous': 0, 'Plasma': 0,  # Non-Solvent-Based life unlikely
            'Electromagnetic': 0.05, 'Quantum': 0.05,  # Some potential for Energy Beings
            'Radiation-Resistant': 0.025, 'Pressure-Resistant': 0.025, 'Temperature-Resistant': 0.025,  # Some extremophiles
        },
        "Iron-rich": {
            'Aquatic': 0.0, 'Terrestrial': 0.10, 'Flora': 0.10, # Carbon-Based life less likely
            'Crystalline': 0.15, 'Amorphous': 0.15,  # Higher probability for Silicon-Based life
            'Cold-Tolerant Fauna': 0, 'Cold-Tolerant Flora': 0,  # Ammonia-Based life unlikely
            'Gaseous': 0, 'Plasma': 0,  # Non-Solvent-Based life unlikely
            'Electromagnetic': 0.05, 'Quantum': 0.05,  # Some Energy Beings potential
            'Radiation-Resistant': 0.05, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.05,  # Some extremophiles
        },
        "Helium-rich": {
            'Aquatic': 0.0, 'Terrestrial': 0.0, 'Flora': 0.0,
            'Crystalline': 0.001, 'Amorphous': 0.001,  # Lower probability for Silicon-Based life
            'Cold-Tolerant Fauna': 0, 'Cold-Tolerant Flora': 0,  # Ammonia-Based life unlikely
            'Gaseous': 0.25, 'Plasma': 0.25,  # Dominant Non-Solvent-Based life
            'Electromagnetic': 0.15, 'Quantum': 0.15,  # Significant presence of Energy Beings
            'Radiation-Resistant': 0.05, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0,  # Some Extremophiles
        },
        "Sulfuric Acid Cloud": {
            'Aquatic': 0.0, 'Terrestrial': 0.0, 'Flora': 0.0,
            'Crystalline': 0.001, 'Amorphous': 0.001,  # Lower probability for Silicon-Based life
            'Cold-Tolerant Fauna': 0, 'Cold-Tolerant Flora': 0,  # Ammonia-Based life unlikely
            'Gaseous': 0, 'Plasma': 0,  # Non-Solvent-Based life unlikely
            'Electromagnetic': 0.25, 'Quantum': 0.25,  # High probability for Energy Beings
            'Radiation-Resistant': 0.1, 'Pressure-Resistant': 0.1, 'Temperature-Resistant': 0,  # Some Extremophiles
        },
        "Chlorine-based Atmosphere": {
            'Aquatic': 0.0, 'Terrestrial': 0.0, 'Flora': 0.0,
            'Crystalline': 0.001, 'Amorphous': 0.001,  # Lower probability for Silicon-Based lif
            'Cold-Tolerant Fauna': 0, 'Cold-Tolerant Flora': 0,  # Ammonia-Based life unlikelye
            'Gaseous': 0.10, 'Plasma': 0.10,  # Some Non-Solvent-Based life possible
            'Electromagnetic': 0.20, 'Quantum': 0.20,  # Energy Beings likely
            'Radiation-Resistant': 0.05, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.05,  # Extremophiles
        },
        "Hydrocarbon Lakes": {
            'Aquatic': 0.001, 'Terrestrial': 0.00, 'Flora': 0.001,  # Some Carbon-Based life
            'Cold-Tolerant Fauna': 0.15, 'Cold-Tolerant Flora': 0.15,  # Suitable for Ammonia-Based life
            'Gaseous': 0.0, 'Plasma': 0.0,  # Some Non-Solvent-Based life possible
            'Crystalline': 0.001, 'Amorphous': 0.001,  # Lower probability for Silicon-Based life
            'Electromagnetic': 0.10, 'Quantum': 0.10,  # Energy Beings
            'Radiation-Resistant': 0.05, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.05,  # Extremophiles
        },
        "Supercritical Fluid": {
            'Aquatic': 0.0, 'Terrestrial': 0.0, 'Flora': 0.0,
            'Cold-Tolerant Fauna': 0.01, 'Cold-Tolerant Flora': 0.01,  # Ammonia-Based life possible
            'Gaseous': 0.0, 'Plasma': 0.0,  # Some Non-Solvent-Based life possible
            'Crystalline': 0.05, 'Amorphous': 0.05,  # Some Silicon-Based life
            'Electromagnetic': 0.3, 'Quantum': 0.3,  # Energy Beings
            'Radiation-Resistant': 0.05, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.05,  # Extremophiles
        },
        "Subsurface Ocean": {
            'Aquatic': 0.2, 'Terrestrial': 0.0, 'Flora': 0.0,  # Carbon-Based life forms
            'Cold-Tolerant Fauna': 0.1, 'Cold-Tolerant Flora': 0.1,  # Ammonia-Based life
            'Gaseous': 0.0, 'Plasma': 0.0,  # Some Non-Solvent-Based life possible
            'Crystalline': 0.005, 'Amorphous': 0.005,  # Silicon-Based life
            'Electromagnetic': 0.005, 'Quantum': 0.005,  # Energy Beings
            'Radiation-Resistant': 0.05, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.3,  # Extremophiles
        }
    }

    biome_biological_support = {
    "Forest": {
        "biological_diversity_quotient": 0.87,
        "habitable_landmass_percentage": 0.69
    },
    "Desert": {
        "biological_diversity_quotient": 0.25,
        "habitable_landmass_percentage": 0.48
    },
    "Ocean": {
        "biological_diversity_quotient": 0.85,
        "habitable_landmass_percentage": 0.68
    },
    "Tundra": {
        "biological_diversity_quotient": 0.45,
        "habitable_landmass_percentage": 0.3
    },
    "Grassland": {
        "biological_diversity_quotient": 0.9,
        "habitable_landmass_percentage": 0.62
    },
    "Wetlands": {
        "biological_diversity_quotient": 0.83,
        "habitable_landmass_percentage": 0.61
    },
    "Savanna": {
        "biological_diversity_quotient": 0.99,
        "habitable_landmass_percentage": 0.82
    },
    "Taiga": {
        "biological_diversity_quotient": 0.71,
        "habitable_landmass_percentage": 0.67
    },
    "Chaparral": {
        "biological_diversity_quotient": 0.78,
        "habitable_landmass_percentage": 0.76
    },
    "Temperate Deciduous Forest": {
        "biological_diversity_quotient": 0.75,
        "habitable_landmass_percentage": 0.87
    },
    "Temperate Rainforest": {
        "biological_diversity_quotient": 0.8,
        "habitable_landmass_percentage": 0.79
    },
    "Mediterranean": {
        "biological_diversity_quotient": 0.76,
        "habitable_landmass_percentage": 0.45
    },
    "Montane (Alpine)": {
        "biological_diversity_quotient": 0.74,
        "habitable_landmass_percentage": 0.5
    },
    "Coral Reefs": {
        "biological_diversity_quotient": 0.92,
        "habitable_landmass_percentage": 0.43
    },
    "Mangroves": {
        "biological_diversity_quotient": 0.81,
        "habitable_landmass_percentage": 0.55
    },
    "Silicon-based": {
        "biological_diversity_quotient": 0.58,
        "habitable_landmass_percentage": 0.31
    },
    "Ammonia-based": {
        "biological_diversity_quotient": 0.49,
        "habitable_landmass_percentage": 0.42
    },
    "Lava": {
        "biological_diversity_quotient": 0.8,
        "habitable_landmass_percentage": 0.61
    },
    "Ice": {
        "biological_diversity_quotient": 0.56,
        "habitable_landmass_percentage": 0.28
    },
    "Super-Earth Oceanic": {
        "biological_diversity_quotient": 0.61,
        "habitable_landmass_percentage": 0.23
    },
    "Carbon-rich": {
        "biological_diversity_quotient": 0.52,
        "habitable_landmass_percentage": 0.88
    },
    "Iron-rich": {
        "biological_diversity_quotient": 0.63,
        "habitable_landmass_percentage": 0.24
    },
    "Helium-rich": {
        "biological_diversity_quotient": 0.22,
        "habitable_landmass_percentage": 0.64
    },
    "Sulfuric Acid Cloud": {
        "biological_diversity_quotient": 0.57,
        "habitable_landmass_percentage": 0.74
    },
    "Chlorine-based Atmosphere": {
        "biological_diversity_quotient": 0.6,
        "habitable_landmass_percentage": 0.17
    },
    "Hydrocarbon Lakes": {
        "biological_diversity_quotient": 0.28,
        "habitable_landmass_percentage": 0.59
    },
    "Supercritical Fluid": {
        "biological_diversity_quotient": 0.69,
        "habitable_landmass_percentage": 0.39
    },
    "Subsurface Ocean": {
        "biological_diversity_quotient": 0.31,
        "habitable_landmass_percentage": 0.71
    }
}