from .concept import Concept

class Biome:

    def __init__(self) -> None:
        
        # Create concepts for each planet type
        biome_concepts = {}
        for biome_type in self.biomes:
            biome_concepts[biome_type] = Concept(biome_type, "Biome")

        # Extracting unique biology subcategories from biome_biology_probabilities
        unique_biology_subcategories = list(set(subcat for biomes in self.biome_biology_probabilities.values() for subcat in biomes))

        # Update biome_concepts with connections to biology subcategories including probabilities
        for biome_type, subcategory_probs in self.biome_biology_probabilities.items():
            for subcategory, probability in subcategory_probs.items():
                biome_concepts[biome_type].add_connection(subcategory, probability)


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
            'Crystalline': 0.01, 'Amorphous': 0.01,
            'Cold-Tolerant Fauna': 0.02, 'Cold-Tolerant Flora': 0.03,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.02, 'Quantum': 0.02,
            'Robotic': 0.05, 'AI': 0.05,
            'Radiation-Resistant': 0.02, 'Pressure-Resistant': 0.02, 'Temperature-Resistant': 0.02,
            'Mixed-Traits Fauna': 0.03, 'Mixed-Traits Flora': 0.03
        },
        "Desert": {
            'Aquatic': 0.00, 'Terrestrial': 0.25, 'Flora': 0.15,
            'Crystalline': 0.02, 'Amorphous': 0.02,
            'Cold-Tolerant Fauna': 0.01, 'Cold-Tolerant Flora': 0.01,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.03, 'Quantum': 0.03,
            'Robotic': 0.15, 'AI': 0.15,
            'Radiation-Resistant': 0.10, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.05,
            'Mixed-Traits Fauna': 0.02, 'Mixed-Traits Flora': 0.02
        },
        "Ocean": {
            'Aquatic': 0.30, 'Terrestrial': 0.00, 'Flora': 0.25,
            'Crystalline': 0.00, 'Amorphous': 0.00,
            'Cold-Tolerant Fauna': 0.05, 'Cold-Tolerant Flora': 0.05,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.05, 'Quantum': 0.05,
            'Robotic': 0.05, 'AI': 0.05,
            'Radiation-Resistant': 0.03, 'Pressure-Resistant': 0.03, 'Temperature-Resistant': 0.03,
            'Mixed-Traits Fauna': 0.04, 'Mixed-Traits Flora': 0.04
            },
        "Tundra": {
            'Aquatic': 0.05, 'Terrestrial': 0.15, 'Flora': 0.10,
            'Crystalline': 0.01, 'Amorphous': 0.01,
            'Cold-Tolerant Fauna': 0.20, 'Cold-Tolerant Flora': 0.20,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.02, 'Quantum': 0.02,
            'Robotic': 0.05, 'AI': 0.05,
            'Radiation-Resistant': 0.10, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.05,
            'Mixed-Traits Fauna': 0.03, 'Mixed-Traits Flora': 0.03
            },
        "Grassland": {
            'Aquatic': 0.03, 'Terrestrial': 0.25, 'Flora': 0.25,
            'Crystalline': 0.01, 'Amorphous': 0.01,
            'Cold-Tolerant Fauna': 0.02, 'Cold-Tolerant Flora': 0.02,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.02, 'Quantum': 0.02,
            'Robotic': 0.08, 'AI': 0.08,
            'Radiation-Resistant': 0.05, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.05,
            'Mixed-Traits Fauna': 0.05, 'Mixed-Traits Flora': 0.05
            },
        "Wetlands": {
            'Aquatic': 0.20, 'Terrestrial': 0.15, 'Flora': 0.20,
            'Crystalline': 0.01, 'Amorphous': 0.01,
            'Cold-Tolerant Fauna': 0.03, 'Cold-Tolerant Flora': 0.03,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.03, 'Quantum': 0.03,
            'Robotic': 0.06, 'AI': 0.06,
            'Radiation-Resistant': 0.04, 'Pressure-Resistant': 0.04, 'Temperature-Resistant': 0.04,
            'Mixed-Traits Fauna': 0.04, 'Mixed-Traits Flora': 0.04
            },
        "Savanna": {
            'Aquatic': 0.02, 'Terrestrial': 0.30,'Flora': 0.20,
            'Crystalline': 0.01, 'Amorphous': 0.01,
            'Cold-Tolerant Fauna': 0.01, 'Cold-Tolerant Flora': 0.01,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.02, 'Quantum': 0.02,
            'Robotic': 0.10, 'AI': 0.10,
            'Radiation-Resistant': 0.05, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.05,
            'Mixed-Traits Fauna': 0.05, 'Mixed-Traits Flora': 0.05
            },
        "Taiga": {
            'Aquatic': 0.03, 'Terrestrial': 0.20, 'Flora': 0.25,
            'Crystalline': 0.01, 'Amorphous': 0.01,
            'Cold-Tolerant Fauna': 0.15, 'Cold-Tolerant Flora': 0.15,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.02, 'Quantum': 0.02,
            'Robotic': 0.05, 'AI': 0.05,
            'Radiation-Resistant': 0.07, 'Pressure-Resistant': 0.07, 'Temperature-Resistant': 0.07,
            'Mixed-Traits Fauna': 0.03, 'Mixed-Traits Flora': 0.03
            },
        "Chaparral": {
            'Aquatic': 0.01, 'Terrestrial': 0.30, 'Flora': 0.20,
            'Crystalline': 0.02, 'Amorphous': 0.02,
            'Cold-Tolerant Fauna': 0.01, 'Cold-Tolerant Flora': 0.01,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.03, 'Quantum': 0.03,
            'Robotic': 0.12, 'AI': 0.12,
            'Radiation-Resistant': 0.06, 'Pressure-Resistant': 0.06, 'Temperature-Resistant': 0.06,
            'Mixed-Traits Fauna': 0.05, 'Mixed-Traits Flora': 0.05
            },
        "Temperate Deciduous Forest": {
            'Aquatic': 0.10, 'Terrestrial': 0.20, 'Flora': 0.25,
            'Crystalline': 0.01, 'Amorphous': 0.01,
            'Cold-Tolerant Fauna': 0.05, 'Cold-Tolerant Flora': 0.05,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.03, 'Quantum': 0.03,
            'Robotic': 0.07, 'AI': 0.07,
            'Radiation-Resistant': 0.04, 'Pressure-Resistant': 0.04, 'Temperature-Resistant': 0.04,
            'Mixed-Traits Fauna': 0.06, 'Mixed-Traits Flora': 0.06
        },
        "Temperate Rainforest": {
            'Aquatic': 0.15, 'Terrestrial': 0.15, 'Flora': 0.20,
            'Crystalline': 0.01, 'Amorphous': 0.01,
            'Cold-Tolerant Fauna': 0.06, 'Cold-Tolerant Flora': 0.06,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.04, 'Quantum': 0.04,
            'Robotic': 0.05, 'AI': 0.05,
            'Radiation-Resistant': 0.03, 'Pressure-Resistant': 0.03,
            'Temperature-Resistant': 0.03, 'Pressure-Resistant': 0.0, 'Temperature-Resistant': 0.0,
            'Mixed-Traits Fauna': 0.06, 'Mixed-Traits Flora': 0.06
        },
        "Mediterranean": {
            'Aquatic': 0.10, 'Terrestrial': 0.20, 'Flora': 0.25,
            'Crystalline': 0.02, 'Amorphous': 0.02,
            'Cold-Tolerant Fauna': 0.02, 'Cold-Tolerant Flora': 0.02,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.05, 'Quantum': 0.05,
            'Robotic': 0.08, 'AI': 0.08,
            'Radiation-Resistant': 0.05, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.05,
            'Mixed-Traits Fauna': 0.05, 'Mixed-Traits Flora': 0.05
        },
        "Montane (Alpine)": {
            'Aquatic': 0.05, 'Terrestrial': 0.20, 'Flora': 0.25, 
            'Crystalline': 0.01, 'Amorphous': 0.01, 
            'Cold-Tolerant Fauna': 0.10, 'Cold-Tolerant Flora': 0.10, 
            'Gaseous': 0.00, 'Plasma': 0.00, 
            'Electromagnetic': 0.02, 'Quantum': 0.02, 
            'Robotic': 0.02, 'AI': 0.02, 
            'Radiation-Resistant': 0.05, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.10,
            'Mixed-Traits Fauna': 0.05, 'Mixed-Traits Flora': 0.05
        },
        "Coral Reefs": {
            'Aquatic': 0.30, 'Terrestrial': 0.00, 'Flora': 0.20,
            'Crystalline': 0.00, 'Amorphous': 0.00,
            'Cold-Tolerant Fauna': 0.00, 'Cold-Tolerant Flora': 0.00,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.05, 'Quantum': 0.05,
            'Robotic': 0.05, 'AI': 0.05,
            'Radiation-Resistant': 0.05, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.05,
            'Mixed-Traits Fauna': 0.10, 'Mixed-Traits Flora': 0.10
        },
        "Mangroves": {
            'Aquatic': 0.15, 'Terrestrial': 0.15, 'Flora': 0.20,
            'Crystalline': 0.01, 'Amorphous': 0.01,
            'Cold-Tolerant Fauna': 0.05, 'Cold-Tolerant Flora': 0.05,
            'Gaseous': 0.00, 'Plasma': 0.00,
            'Electromagnetic': 0.05, 'Quantum': 0.05,
            'Robotic': 0.10, 'AI': 0.10,
            'Radiation-Resistant': 0.05, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.05,
            'Mixed-Traits Fauna': 0.05, 'Mixed-Traits Flora': 0.05
        },
        "Silicon-based": {
            'Aquatic': 0.0, 'Terrestrial': 0.0, 'Flora': 0.0,
            'Crystalline': 0.35, 'Amorphous': 0.35,  # Dominant Silicon-Based life forms
            'Cold-Tolerant Fauna': 0, 'Cold-Tolerant Flora': 0,
            'Gaseous': 0.05, 'Plasma': 0.05,  # Possible Non-Solvent-Based life forms
            'Electromagnetic': 0.05, 'Quantum': 0.05,  # Some potential for Energy Beings
            'Robotic': 0.05, 'AI': 0.05,  # Artificial life forms
            'Radiation-Resistant': 0, 'Pressure-Resistant': 0, 'Temperature-Resistant': 0,
            'Mixed-Traits Fauna': 0, 'Mixed-Traits Flora': 0
        },
        "Ammonia-based": {
            'Aquatic': 0.0, 'Terrestrial': 0.0, 'Flora': 0.0,
            'Cold-Tolerant Fauna': 0.4, 'Cold-Tolerant Flora': 0.4,  # Dominant Ammonia-Based life forms
            'Crystalline': 0, 'Amorphous': 0,
            'Gaseous': 0, 'Plasma': 0,
            'Electromagnetic': 0.05, 'Quantum': 0.05,  # Some potential for Energy Beings
            'Robotic': 0.025, 'AI': 0.025,  # Artificial life forms
            'Radiation-Resistant': 0.025, 'Pressure-Resistant': 0.025, 'Temperature-Resistant': 0.025,
            'Mixed-Traits Fauna': 0, 'Mixed-Traits Flora': 0
        },
        "Lava": {
            'Aquatic': 0.0, 'Terrestrial': 0.0, 'Flora': 0.0,
            'Crystalline': 0.05, 'Amorphous': 0.05,  # Silicon-Based life forms in harsh conditions
            'Cold-Tolerant Fauna': 0, 'Cold-Tolerant Flora': 0,
            'Gaseous': 0, 'Plasma': 0,
            'Electromagnetic': 0.05, 'Quantum': 0.05,  # Some potential for Energy Beings
            'Robotic': 0.25, 'AI': 0.25,  # High probability for Artificial life forms
            'Radiation-Resistant': 0.1, 'Pressure-Resistant': 0.1, 'Temperature-Resistant': 0.1,  # Extremophiles suited for harsh lava conditions
            'Mixed-Traits Fauna': 0, 'Mixed-Traits Flora': 0
        },
        "Ice": {
            'Aquatic': 0.15, 'Terrestrial': 0.10, 'Flora': 0.05,  # Some Carbon-Based life possible
            'Cold-Tolerant Fauna': 0.15, 'Cold-Tolerant Flora': 0.15,  # Suitable for Ammonia-Based life
            'Crystalline': 0, 'Amorphous': 0,  # Silicon-Based life unlikely
            'Gaseous': 0, 'Plasma': 0,  # Non-Solvent-Based life unlikely
            'Electromagnetic': 0.05, 'Quantum': 0.05,  # Potential for Energy Beings
            'Robotic': 0.10, 'AI': 0.10,  # Artificial life forms adaptable
            'Radiation-Resistant': 0.10, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.05,  # Extremophiles adapted to cold
            'Mixed-Traits Fauna': 0, 'Mixed-Traits Flora': 0  # Hybrid life unlikely
        },
        "Super-Earth Oceanic": {
            'Aquatic': 0.35, 'Terrestrial': 0.20, 'Flora': 0.15,  # Dominant Carbon-Based life
            'Crystalline': 0, 'Amorphous': 0,  # Silicon-Based life unlikely
            'Cold-Tolerant Fauna': 0.05, 'Cold-Tolerant Flora': 0.05,  # Some Ammonia-Based life possible
            'Gaseous': 0, 'Plasma': 0,  # Non-Solvent-Based life unlikely
            'Electromagnetic': 0.05, 'Quantum': 0.05,  # Some Energy Beings potential
            'Robotic': 0.025, 'AI': 0.025,  # Artificial life forms
            'Radiation-Resistant': 0.025, 'Pressure-Resistant': 0.025, 'Temperature-Resistant': 0.025,  # Some extremophiles
            'Mixed-Traits Fauna': 0, 'Mixed-Traits Flora': 0  # Hybrid life unlikely
        },
        "Carbon-rich": {
            'Aquatic': 0.40, 'Terrestrial': 0.25, 'Flora': 0.15,  # High probability for Carbon-Based life
            'Crystalline': 0, 'Amorphous': 0,  # Silicon-Based life unlikely
            'Cold-Tolerant Fauna': 0, 'Cold-Tolerant Flora': 0,  # Ammonia-Based life unlikely
            'Gaseous': 0, 'Plasma': 0,  # Non-Solvent-Based life unlikely
            'Electromagnetic': 0.05, 'Quantum': 0.05,  # Some potential for Energy Beings
            'Robotic': 0.025, 'AI': 0.025,  # Artificial life forms
            'Radiation-Resistant': 0.025, 'Pressure-Resistant': 0.025, 'Temperature-Resistant': 0.025,  # Some extremophiles
            'Mixed-Traits Fauna': 0, 'Mixed-Traits Flora': 0  # Hybrid life unlikely
        },
        "Iron-rich": {
            'Aquatic': 0.0, 'Terrestrial': 0.10, 'Flora': 0.10, # Carbon-Based life less likely
            'Crystalline': 0.15, 'Amorphous': 0.15,  # Higher probability for Silicon-Based life
            'Cold-Tolerant Fauna': 0, 'Cold-Tolerant Flora': 0,  # Ammonia-Based life unlikely
            'Gaseous': 0, 'Plasma': 0,  # Non-Solvent-Based life unlikely
            'Electromagnetic': 0.05, 'Quantum': 0.05,  # Some Energy Beings potential
            'Robotic': 0.15, 'AI': 0.15,  # Higher probability for Artificial life
            'Radiation-Resistant': 0.05, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.05,  # Some extremophiles
            'Mixed-Traits Fauna': 0, 'Mixed-Traits Flora': 0  # Hybrid life less likely
        },
        "Helium-rich": {
            'Aquatic': 0.0, 'Terrestrial': 0.0, 'Flora': 0.0,
            'Crystalline': 0.001, 'Amorphous': 0.001,  # Lower probability for Silicon-Based life
            'Cold-Tolerant Fauna': 0, 'Cold-Tolerant Flora': 0,  # Ammonia-Based life unlikely
            'Gaseous': 0.25, 'Plasma': 0.25,  # Dominant Non-Solvent-Based life
            'Electromagnetic': 0.15, 'Quantum': 0.15,  # Significant presence of Energy Beings
            'Robotic': 0.05, 'AI': 0.05,  # Some Artificial life
            'Radiation-Resistant': 0.05, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0,  # Some Extremophiles
            'Mixed-Traits Fauna': 0, 'Mixed-Traits Flora': 0  # Hybrid life unlikely
        },
        "Sulfuric Acid Cloud": {
            'Aquatic': 0.0, 'Terrestrial': 0.0, 'Flora': 0.0,
            'Crystalline': 0.001, 'Amorphous': 0.001,  # Lower probability for Silicon-Based life
            'Cold-Tolerant Fauna': 0, 'Cold-Tolerant Flora': 0,  # Ammonia-Based life unlikely
            'Gaseous': 0, 'Plasma': 0,  # Non-Solvent-Based life unlikely
            'Electromagnetic': 0.25, 'Quantum': 0.25,  # High probability for Energy Beings
            'Robotic': 0.15, 'AI': 0.15,  # Artificial life adapted to harsh conditions
            'Radiation-Resistant': 0.1, 'Pressure-Resistant': 0.1, 'Temperature-Resistant': 0,  # Some Extremophiles
            'Mixed-Traits Fauna': 0, 'Mixed-Traits Flora': 0  # Hybrid life unlikely
        },
        "Chlorine-based Atmosphere": {
            'Aquatic': 0.0, 'Terrestrial': 0.0, 'Flora': 0.0,
            'Crystalline': 0.001, 'Amorphous': 0.001,  # Lower probability for Silicon-Based lif
            'Cold-Tolerant Fauna': 0, 'Cold-Tolerant Flora': 0,  # Ammonia-Based life unlikelye
            'Gaseous': 0.10, 'Plasma': 0.10,  # Some Non-Solvent-Based life possible
            'Electromagnetic': 0.20, 'Quantum': 0.20,  # Energy Beings likely
            'Robotic': 0.15, 'AI': 0.15,  # Artificial life forms
            'Radiation-Resistant': 0.05, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.05,  # Extremophiles
            'Mixed-Traits Fauna': 0, 'Mixed-Traits Flora': 0  # Hybrid life unlikely
        },
        "Hydrocarbon Lakes": {
            'Aquatic': 0.10, 'Terrestrial': 0.05, 'Flora': 0.05,  # Some Carbon-Based life
            'Cold-Tolerant Fauna': 0.15, 'Cold-Tolerant Flora': 0.15,  # Suitable for Ammonia-Based life
            'Gaseous': 0.0, 'Plasma': 0.0,  # Some Non-Solvent-Based life possible
            'Crystalline': 0.001, 'Amorphous': 0.001,  # Lower probability for Silicon-Based life
            'Electromagnetic': 0.10, 'Quantum': 0.10,  # Energy Beings
            'Robotic': 0.10, 'AI': 0.10,  # Artificial life forms
            'Radiation-Resistant': 0.05, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.05,  # Extremophiles
            'Mixed-Traits Fauna': 0, 'Mixed-Traits Flora': 0  # Hybrid life
        },
        "Supercritical Fluid": {
            'Aquatic': 0.0, 'Terrestrial': 0.0, 'Flora': 0.0,
            'Cold-Tolerant Fauna': 0.1, 'Cold-Tolerant Flora': 0.1,  # Ammonia-Based life possible
            'Gaseous': 0.0, 'Plasma': 0.0,  # Some Non-Solvent-Based life possible
            'Crystalline': 0.05, 'Amorphous': 0.05,  # Some Silicon-Based life
            'Electromagnetic': 0.1, 'Quantum': 0.1,  # Energy Beings
            'Robotic': 0.05, 'AI': 0.05,  # Artificial life forms
            'Radiation-Resistant': 0.05, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.05,  # Extremophiles
            'Mixed-Traits Fauna': 0.05, 'Mixed-Traits Flora': 0.05  # Hybrid life forms
        },
        "Subsurface Ocean": {
            'Aquatic': 0.2, 'Terrestrial': 0.1, 'Flora': 0.1,  # Carbon-Based life forms
            'Cold-Tolerant Fauna': 0.1, 'Cold-Tolerant Flora': 0.1,  # Ammonia-Based life
            'Gaseous': 0.0, 'Plasma': 0.0,  # Some Non-Solvent-Based life possible
            'Crystalline': 0.05, 'Amorphous': 0.05,  # Silicon-Based life
            'Electromagnetic': 0.05, 'Quantum': 0.05,  # Energy Beings
            'Robotic': 0.05, 'AI': 0.05,  # Artificial life forms
            'Radiation-Resistant': 0.05, 'Pressure-Resistant': 0.05, 'Temperature-Resistant': 0.05,  # Extremophiles
            'Mixed-Traits Fauna': 0.05, 'Mixed-Traits Flora': 0.05  # Hybrid life forms
        }
    }
