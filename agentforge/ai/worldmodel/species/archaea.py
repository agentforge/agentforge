class Archaea:
    def __init__(self) -> None:
        # Realistic Global Species Probabilities based on likelihood of life
        self.planet_probabilities = {
            'terrestrial': 0.7,   # Higher likelihood due to Earth-like conditions
            'superEarth': 0.6,    # Potentially habitable if conditions are right
            'mercuryLike': 0.05,  # Low likelihood due to extreme temperatures
            'marsLike': 0.4,      # Possible if water and atmosphere were present
            'gasGiant': 0.01,     # Very low likelihood due to lack of solid surface
            'hotJupiter': 0.01,   # Extremely low likelihood due to hostile conditions
            'neptunian': 0.02,    # Low likelihood, but possible in moons
            'ringedPlanet': 0.02, # Similar to gas giants, low likelihood
            'miniNeptune': 0.03,  # Low likelihood but potential in moons or upper atmosphere
            'plutoLike': 0.1,     # Low likelihood due to extreme cold and lack of atmosphere
            'ceresLike': 0.1,     # Low likelihood, small chance in subsurface oceans
            'oceanPlanet': 0.5,   # High likelihood if conditions are stable
            'venusLike': 0.2,     # Low likelihood due to extreme conditions
            'icy': 0.3            # Possible in subsurface oceans
        }
        self.biome_probabilities = {
            'Forest': 0.7,
            'Desert': 0.3,
            'Ocean': 0.8,
            'Tundra': 0.4,
            'Grassland': 0.6,
            'Wetlands': 0.5,
            'Savanna': 0.6,
            'Taiga': 0.5,
            'Chaparral': 0.4,
            'Temperate Deciduous Forest': 0.7,
            'Temperate Rainforest': 0.6,
            'Mediterranean': 0.4,
            'Montane (Alpine)': 0.3,
            'Coral Reefs': 0.7,
            'Mangroves': 0.6,
            'Silicon-based': 0.01,    # Hypothetical, extremely low probability
            'Ammonia-based': 0.02,    # Hypothetical, slightly higher but still low
            'Lava': 0.01,             # Very hostile, extremely low probability
            'Ice': 0.4,               # Possible in subsurface oceans
            'Super-Earth Oceanic': 0.6,
            'Carbon-rich': 0.2,
            'Iron-rich': 0.2,
            'Helium-rich': 0.01,      # Very unlikely due to lack of solid surface
            'Sulfuric Acid Cloud': 0.01, # Extremely hostile, very low probability
            'Chlorine-based Atmosphere': 0.01, # Extremely hostile, very low probability
            'Hydrocarbon Lakes': 0.02, # Hypothetical, low probability
            'Supercritical Fluid': 0.01, # Extremely hostile, very low probability
            'Subsurface Ocean': 0.4   # Potential for life if conditions are stable
        }
        
        # Specific Species Attributes
        self.life_form_class = "Unicellular"
        self.species_name = "Archaea"
        self.evolutionary_probabilities = {}
        self.evolutionary_stage = []
        
        # Randomized Attributes
        self.genetics = {}
        self.attributes = {}