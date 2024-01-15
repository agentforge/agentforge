import numpy as np
from scipy.special import softmax
import pandas as pd
import json, math

class Concept:
    def __init__(self, name, category, metadata=None):
        self.name = name
        self.category = category
        self.connections = []
        self.metadata = metadata if metadata is not None else {}

    def add_connection(self, concept_name, probability):
        self.connections.append({'concept': concept_name, 'probability': probability})

    def remove_connection(self, concept_name):
        self.connections = [c for c in self.connections if c['concept'] != concept_name]

    def get_connections(self):
        return self.connections

    def update_metadata(self, key, value):
        """
        Update the metadata of the concept.
        :param key: The key in the metadata dictionary.
        :param value: The value to be added/updated.
        """
        self.metadata[key] = value

    def __repr__(self):
        return f"Concept(name={self.name}, category={self.category}, connections={self.connections}, metadata={self.metadata})"


# Star probabilities
star_probabilities = {
    'Class O': 0.03,  # Blue Giants
    'Class B': 0.06,  # Blue-White Stars
    'Class A': 0.10,  # White Stars
    'Class F': 0.10,  # Yellow-White Stars
    'Class G': 0.15,  # Yellow Stars (like our Sun)
    'Class K': 0.10,  # Orange Stars
    'Class M': 0.15,  # Red Dwarfs
    'Red Giant': 0.10,  # Red Giants
    'White Dwarf': 0.05,  # White Dwarfs
    'Neutron Star': 0.05,  # Neutron Stars
    'Wolf-Rayet Star': 0.04,  # Wolf-Rayet Stars
    'Class L': 0.04,  # Brown Dwarfs (Class L)
    'Class T': 0.01,  # Methane Dwarfs
    'Class Y': 0.01  # Cool Brown Dwarfs
}

# Base magnetic field strengths for different planet types (in Gauss)
base_magnetic_fields = {
    'terrestrial': 0.5, 'superEarth': 1.0, 'mercuryLike': 0.1, 
    'marsLike': 0.2, 'gasGiant': 10.0, 'hotJupiter': 20.0, 
    'neptunian': 5.0, 'ringedPlanet': 4.0, 'miniNeptune': 3.0, 
    'plutoLike': 0.05, 'ceresLike': 0.03, 'oceanPlanet': 0.6, 
    'venusLike': 0.4, 'icy': 0.2
}

# Star type impact factor for a magnetic field (simplified estimation)
star_type_impact = {
    'Class O': 0.8, 'Class B': 0.9, 'Class A': 1.0, 
    'Class F': 1.1, 'Class G': 1.2, 'Class K': 1.1, 
    'Class M': 1.0, 'Red Giant': 0.7, 'White Dwarf': 0.6, 
    'Neutron Star': 0.5, 'Wolf-Rayet Star': 0.7, 
    'Class L': 1.0, 'Class T': 1.0, 'Class Y': 1.0
}

# Star types metadata with additional details
star_metadata = {
    'Class O': {
        "temperature": "30,000 K or more",
        "luminosity": "Extremely luminous",
        "mass_range": "16+ solar masses",
        "mass_range_kg": f"{16 * 1.989e30} kg or more",
        "characteristics": "Short-lived, emit significant UV radiation",
        "color_range": "Blue",
        "radiation_type": "High UV",
        "other_features": "Likely to end in supernova"
    },
    'Class B': {
        "temperature": "10,000–30,000 K",
        "luminosity": "Very luminous",
        "mass_range": "2.1–16 solar masses",
        "mass_range_kg": f"{2.1 * 1.989e30} to {16 * 1.989e30} kg",
        "characteristics": "Blue-white stars, hotter than the Sun",
        "color_range": "Blue-white",
        "radiation_type": "UV",
        "other_features": "Often part of multiple star systems"
    },
    'Class A': {
        "temperature": "7,500–10,000 K",
        "luminosity": "Moderately luminous",
        "mass_range": "1.4–2.1 solar masses",
        "mass_range_kg": f"{1.4 * 1.989e30} to {2.1 * 1.989e30} kg",
        "characteristics": "Strong hydrogen lines in their spectra",
        "color_range": "White",
        "radiation_type": "Visible light with some UV",
        "other_features": "Shorter lifespan than smaller stars, often have debris disks"
    },
    'Class F': {
        "temperature": "6,000–7,500 K",
        "luminosity": "Bright",
        "mass_range": "1.04–1.4 solar masses",
        "mass_range_kg": f"{1.04 * 1.989e30} to {1.4 * 1.989e30} kg",
        "characteristics": "Often have complex planetary systems",
        "color_range": "Yellowish-white",
        "radiation_type": "Visible light",
        "other_features": "Longer lifespan than Class A and B stars, stable burning phase"
    },
    'Class G': {
        "temperature": "5,200–6,000 K",
        "luminosity": "Similar to or slightly brighter than the Sun",
        "mass_range": "0.8–1.04 solar masses",
        "mass_range_kg": f"{0.8 * 1.989e30} to {1.04 * 1.989e30} kg",
        "characteristics": "Stable and suitable for supporting life on orbiting planets",
        "color_range": "Yellow",
        "radiation_type": "Visible light",
        "other_features": "Includes the Sun, likely to have planetary systems with potential for life"
    },
     'Class K': {
        "temperature": "3,700–5,200 K",
        "luminosity": "Less luminous than the Sun",
        "mass_range": "0.45–0.8 solar masses",
        "mass_range_kg": f"{0.45 * 1.989e30} to {0.8 * 1.989e30} kg",
        "characteristics": "Often have complex magnetic activity",
        "color_range": "Orange",
        "radiation_type": "Visible light, some infrared",
        "other_features": "Longer lifespan, can have stable planetary systems"
    },
    'Class M': {
        "temperature": "2,400–3,700 K",
        "luminosity": "Very low",
        "mass_range": "0.08–0.45 solar masses",
        "mass_range_kg": f"{0.08 * 1.989e30} to {0.45 * 1.989e30} kg",
        "characteristics": "Most common stars in the universe, fully convective",
        "color_range": "Red",
        "radiation_type": "Visible light, some infrared",
        "other_features": "Very long lifespan, often hosts planets"
    },
    'Red Giant': {
        "temperature": "3,500–5,000 K (varies)",
        "luminosity": "Very high",
        "mass_range": "Typically 0.3–8 solar masses (in main sequence)",
        "mass_range_kg": f"{0.3 * 1.989e30} to {8 * 1.989e30} kg",
        "characteristics": "Expanded outer layers, cooler surface",
        "color_range": "Red",
        "radiation_type": "Visible light, strong infrared",
        "other_features": "End-of-life stage for many stars, expands and cools"
    },
    'White Dwarf': {
        "temperature": "Up to 100,000 K initially, cooling over time",
        "luminosity": "Low, but high for its size",
        "mass_range": "Up to 1.4 solar masses (Chandrasekhar limit)",
        "mass_range_kg": f"Up to {1.4 * 1.989e30} kg",
        "characteristics": "Very dense, no fusion occurring",
        "color_range": "White, fading to blue then red over time",
        "radiation_type": "Visible light, ultraviolet when young",
        "other_features": "Final evolutionary state of stars like our Sun"
    },
    'Neutron Star': {
        "temperature": "Up to millions of K",
        "luminosity": "High in X-rays and gamma rays",
        "mass_range": "1.4 to 2.16 solar masses",
        "mass_range_kg": f"{1.4 * 1.989e30} to {2.16 * 1.989e30} kg",
        "characteristics": "Extremely dense, often result from supernova explosions",
        "color_range": "Not visible in normal light spectrum",
        "radiation_type": "X-rays and gamma rays",
        "other_features": "Strong magnetic fields, rapid rotation"
    },
    'Wolf-Rayet Star': {
        "temperature": "25,000–50,000 K",
        "luminosity": "Extremely luminous",
        "mass_range": "20+ solar masses",
        "mass_range_kg": f"Over {20 * 1.989e30} kg",
        "characteristics": "Losing mass rapidly through powerful stellar winds",
        "color_range": "Blue, often obscured by dust",
        "radiation_type": "Visible light, ultraviolet",
        "other_features": "Short-lived, precursor to supernovae or black holes"
    },
    'Class L': {
        "temperature": "1,300–2,500 K",
        "luminosity": "Very low",
        "mass_range": "15 to 75 times the mass of Jupiter",
        "mass_range_kg": f"{15 * 1.898e27} to {75 * 1.898e27} kg (Jupiter masses)",
        "characteristics": "Too massive to be planets, but not massive enough to sustain hydrogen fusion",
        "color_range": "Reddish to magenta",
        "radiation_type": "Infrared",
        "other_features": "Lack of visible light, presence of metals and dust clouds"
    },
    'Class T': {
        "temperature": "500–1,300 K",
        "luminosity": "Very low",
        "mass_range": "12 to 15 times the mass of Jupiter",
        "mass_range_kg": f"{12 * 1.898e27} to {15 * 1.898e27} kg (Jupiter masses)",
        "characteristics": "Presence of methane in the atmosphere",
        "color_range": "Magenta",
        "radiation_type": "Infrared",
        "other_features": "Cooler than Class L, distinct methane absorption lines"
    },
    'Class Y': {
        "temperature": "Below 500 K",
        "luminosity": "Extremely low",
        "mass_range": "Less than 12 times the mass of Jupiter",
        "mass_range_kg": f"Less than {12 * 1.898e27} kg (Jupiter masses)",
        "characteristics": "Coolest of the brown dwarfs",
        "color_range": "Dark red to magenta",
        "radiation_type": "Infrared, possibly radio",
        "other_features": "Atmospheres may contain water clouds"
    }
}

star_temperature_factors = {
    'Class O': 1.6,   # Blue Giants - Extremely hot and luminous
    'Class B': 1.5,   # Blue-White Stars - Very hot and luminous
    'Class A': 1.3,   # White Stars - Hotter and more luminous than the Sun
    'Class F': 1.2,   # Yellow-White Stars - Slightly hotter than the Sun
    'Class G': 1.0,   # Yellow Stars (like our Sun) - Baseline
    'Class K': 0.9,   # Orange Stars - Cooler than the Sun
    'Class M': 0.8,   # Red Dwarfs - Cool and dim
    'Red Giant': 1.4, # Red Giants - Vary greatly, but often very bright and large
    'White Dwarf': 0.6, # White Dwarfs - Hot but very small and less luminous overall
    'Neutron Star': 0.7, # Neutron Stars - Extremely dense and hot, but small and distant
    'Wolf-Rayet Star': 1.7, # Wolf-Rayet Stars - Extremely hot and luminous
    'Class L': 0.5,   # Brown Dwarfs (Class L) - Cooler and fainter
    'Class T': 0.4,   # Methane Dwarfs - Even cooler and fainter
    'Class Y': 0.3    # Cool Brown Dwarfs - Among the coolest of star-like objects
}

# Base AU values for different types of planets
base_au = {
    'terrestrial': 1.0,
    'superEarth': 1.2,
    'mercuryLike': 0.4,
    'marsLike': 1.5,
    'gasGiant': 5.2,
    'hotJupiter': 0.05,
    'neptunian': 30.1,
    'ringedPlanet': 9.5,
    'miniNeptune': 2.5,
    'plutoLike': 39.5,
    'ceresLike': 2.8,
    'oceanPlanet': 1.0,
    'venusLike': 0.7,
    'icy': 15.0
}

# Star type scaling factors (for AU calculations)
star_type_scaling = {
    'Class O': 2.0,
    'Class B': 1.5,
    'Class A': 1.2,
    'Class F': 1.1,
    'Class G': 1.0,
    'Class K': 0.9,
    'Class M': 0.8,
    'Red Giant': 1.5,
    'White Dwarf': 0.5,
    'Neutron Star': 0.4,
    'Wolf-Rayet Star': 2.0,
    'Class L': 0.7,
    'Class T': 0.6,
    'Class Y': 0.5
}

# Habitable zone varies by star type; these are rough estimates
habitable_zone = {
    'Class O': (2, 10),       # Blue Giants
    'Class B': (1.5, 9),      # Blue-White Stars
    'Class A': (1.2, 5),      # White Stars
    'Class F': (0.8, 2.5),    # Yellow-White Stars
    'Class G': (0.7, 1.5),    # Yellow Stars (like our Sun)
    'Class K': (0.4, 1.2),    # Orange Stars
    'Class M': (0.2, 0.7),    # Red Dwarfs
    'Red Giant': (10, 100),   # Red Giants (wider range due to larger size and luminosity)
    'White Dwarf': (0.01, 0.1), # White Dwarfs (smaller and less luminous)
    'Neutron Star': (0.1, 0.5), # Neutron Stars (habitable zone is speculative)
    'Wolf-Rayet Star': (5, 20), # Wolf-Rayet Stars (extremely hot and luminous)
    'Class L': (0.05, 0.3),    # Brown Dwarfs (Class L)
    'Class T': (0.02, 0.15),   # Methane Dwarfs
    'Class Y': (0.01, 0.1)     # Cool Brown Dwarfs
}

base_star_life_probabilities = {
    'Class O': 0.01,  # Blue Giants - Very hot and short-lived
    'Class B': 0.02,  # Blue-White Stars - Still quite hot and short-lived
    'Class A': 0.05,  # White Stars - Bright and relatively stable
    'Class F': 0.07,  # Yellow-White Stars - Stable and suitable for life
    'Class G': 0.20,  # Yellow Stars (like our Sun) - Ideal for life
    'Class K': 0.15,  # Orange Stars - Stable and long-lived
    'Class M': 0.10,  # Red Dwarfs - Long-lived but with habitability challenges
    'Red Giant': 0.01,  # Red Giants - Not stable environments for life
    'White Dwarf': 0.01,  # White Dwarfs - Remnants of stars, not suitable for life
    'Neutron Star': 0.00,  # Neutron Stars - Extreme environments, unlikely for life
    'Wolf-Rayet Star': 0.00,  # Wolf-Rayet Stars - Massive, short-lived, and unstable
    'Class L': 0.04,  # Brown Dwarfs (Class L) - Cooler, but potential for life exists
    'Class T': 0.03,  # Methane Dwarfs - Challenging but possible for life
    'Class Y': 0.02  # Cool Brown Dwarfs - Low luminosity, but potential exists
}


star_type_masses = {
    "Class O": {
        "mass_range_kg": [32 * 1.989e30, np.inf],
        "age_range_Gyr": [0.001, 10],
        "disk_mass_percentage_of_solar_mass": [10, 50]
    },
    "Class B": {
        "mass_range_kg": [4.2 * 1.989e30, 32 * 1.989e30],
        "age_range_Gyr": [0.01, 0.1],
        "disk_mass_percentage_of_solar_mass": [2, 20]
    },
    "Class A": {
        "mass_range_kg": [2.8 * 1.989e30, 4.2 * 1.989e30],
        "age_range_Gyr": [0.1, 2],
        "disk_mass_percentage_of_solar_mass": [1, 5]
    },
    "Class F": {
        "mass_range_kg": [2.08 * 1.989e30, 2.8 * 1.989e30],
        "age_range_Gyr": [2, 4],
        "disk_mass_percentage_of_solar_mass": [0.5, 3]
    },
    "Class G": {
        "mass_range_kg": [1.6 * 1.989e30, 2.08 * 1.989e30],
        "age_range_Gyr": [4, 10],
        "disk_mass_percentage_of_solar_mass": [0.1, 1]
    },
    "Class K": {
        "mass_range_kg": [0.9 * 1.989e30, 1.6 * 1.989e30],
        "age_range_Gyr": [10, 30],
        "disk_mass_percentage_of_solar_mass": [0.05, 0.5]
    },
    "Class M": {
        "mass_range_kg": [0.16 * 1.989e30, 0.9 * 1.989e30],
        "age_range_Gyr": [30, 100],
        "disk_mass_percentage_of_solar_mass": [0.01, 0.1]
    },
    "Red Giant": {
        "mass_range_kg": [0.6 * 1.989e30, 16 * 1.989e30],
        "age_range_Gyr": [0.1, 10],
        "disk_mass_percentage_of_solar_mass": [0.5, 10]
    },
    "White Dwarf": {
        "mass_range_kg": [0, 2.8 * 1.989e30],
        "age_range_Gyr": [0, 10],
        "disk_mass_percentage_of_solar_mass": [0, 0.1]
    },
    "Neutron Star": {
        "mass_range_kg": [2.8 * 1.989e30, 4.32 * 1.989e30],
        "age_range_Gyr": [0, 13.8],
        "disk_mass_percentage_of_solar_mass": [0, 0.1]
    },
    "Wolf-Rayet Star": {
        "mass_range_kg": [40 * 1.989e30, np.inf],
        "age_range_Gyr": [0.001, 0.5],
        "disk_mass_percentage_of_solar_mass": [5, 50]
    },
    "Class L": {
        "mass_range_kg": [2.985 * 1.898e27, 14.925 * 1.898e27],
        "age_range_Gyr": [0.1, 15],
        "disk_mass_percentage_of_solar_mass": [0, 0.05]
    },
    "Class T": {
        "mass_range_kg": [2.3976 * 1.898e27, 2.985 * 1.898e27],
        "age_range_Gyr": [0.1, 15],
        "disk_mass_percentage_of_solar_mass": [0, 0.05]
    },
    "Class Y": {
        "mass_range_kg": [0, 2.3976 * 1.898e27],
        "age_range_Gyr": [0.1, 15],
        "disk_mass_percentage_of_solar_mass": [0, 0.05]
    }
}

# Planet types
planet_types = ['terrestrial', 'superEarth', 'mercuryLike', 'marsLike', 'gasGiant', 'hotJupiter', 
                'neptunian', 'ringedPlanet', 'miniNeptune', 'plutoLike', 'ceresLike', 'oceanPlanet', 'venusLike', 'icy']

active_core_planets = ['terrestrial', 'superEarth', 'marsLike', 'gasGiant', 'hotJupiter', 'neptunian', 'ringedPlanet', 'oceanPlanet']
inactive_core_planets = ['mercuryLike', 'plutoLike', 'ceresLike', 'icy', 'venusLike', 'miniNeptune']

class_o_planet_probability = {
    'terrestrial': 0.05,  # Lower probability due to harsh conditions near the star
    'superEarth': 0.05,
    'mercuryLike': 0.05,
    'marsLike': 0.05,
    'gasGiant': 0.15,  # Higher probability, especially for those formed in distant orbits
    'hotJupiter': 0.15,  # Possible if migrated inward from outer regions
    'neptunian': 0.10,
    'ringedPlanet': 0.10,
    'miniNeptune': 0.10,
    'plutoLike': 0.05,  # Possible in distant orbits
    'ceresLike': 0.05,
    'oceanPlanet': 0.02,  # Lower probability due to intense radiation
    'venusLike': 0.03,
    'icy': 0.05  # Possible in distant, cooler orbits
}

class_b_planet_probability = {
    'terrestrial': 0.07,  # Slightly higher probability than Class O, but still challenging due to star's brightness and heat
    'superEarth': 0.07,
    'mercuryLike': 0.07,
    'marsLike': 0.07,
    'gasGiant': 0.13,  # Likely to form in the outer regions and might migrate inward
    'hotJupiter': 0.13,  # Possible close to the star
    'neptunian': 0.09,
    'ringedPlanet': 0.09,
    'miniNeptune': 0.09,
    'plutoLike': 0.06,  # Possible in distant orbits
    'ceresLike': 0.06,
    'oceanPlanet': 0.03,  # Possible but challenging due to star's radiation
    'venusLike': 0.05,
    'icy': 0.06  # Possible in distant, cooler orbits
}

class_a_planet_probability = {
    'terrestrial': 0.08,  # Higher probability than Class O and B, but still challenging due to star's brightness and heat
    'superEarth': 0.08,
    'mercuryLike': 0.08,
    'marsLike': 0.08,
    'gasGiant': 0.12,  # Likely to form in the outer regions and might migrate inward
    'hotJupiter': 0.12,  # Possible close to the star
    'neptunian': 0.08,
    'ringedPlanet': 0.08,
    'miniNeptune': 0.08,
    'plutoLike': 0.07,  # Possible in distant orbits
    'ceresLike': 0.07,
    'oceanPlanet': 0.04,  # Possible but challenging due to star's radiation
    'venusLike': 0.06,
    'icy': 0.06  # Possible in distant, cooler orbits
}

class_f_planet_probability = {
    'terrestrial': 0.10,  # Moderate probability, better conditions than hotter stars but still challenging
    'superEarth': 0.10,
    'mercuryLike': 0.10,
    'marsLike': 0.10,
    'gasGiant': 0.11,  # Likely to form in outer regions and might migrate inward
    'hotJupiter': 0.11,  # Possible close to the star
    'neptunian': 0.09,
    'ringedPlanet': 0.09,
    'miniNeptune': 0.09,
    'plutoLike': 0.08,  # Possible in distant orbits
    'ceresLike': 0.08,
    'oceanPlanet': 0.05,  # Moderate probability due to further habitable zone
    'venusLike': 0.07,
    'icy': 0.08  # Possible in distant, cooler orbits
}

class_g_planet_probability = {
    'terrestrial': 0.15,  # Higher probability due to moderate conditions
    'superEarth': 0.15,
    'mercuryLike': 0.10,
    'marsLike': 0.10,
    'gasGiant': 0.10,  # Possible, especially in the outer orbits
    'hotJupiter': 0.05,  # Less likely if not migrated from outer orbits
    'neptunian': 0.10,
    'ringedPlanet': 0.10,
    'miniNeptune': 0.08,
    'plutoLike': 0.07,  # Possible in distant orbits
    'ceresLike': 0.07,
    'oceanPlanet': 0.10,  # Higher probability due to potential for liquid water in habitable zone
    'venusLike': 0.08,
    'icy': 0.05  # Possible in distant, cooler orbits
}

class_k_planet_probability = {
    'terrestrial': 0.18,  # Moderate to high probability due to stable conditions
    'superEarth': 0.18,
    'mercuryLike': 0.12,
    'marsLike': 0.12,
    'gasGiant': 0.08,  # Possible, especially in the outer orbits
    'hotJupiter': 0.04,  # Less likely if not migrated from outer orbits
    'neptunian': 0.07,
    'ringedPlanet': 0.07,
    'miniNeptune': 0.06,
    'plutoLike': 0.06,  # Possible in distant orbits
    'ceresLike': 0.06,
    'oceanPlanet': 0.12,  # Moderate probability due to potential for liquid water in habitable zone
    'venusLike': 0.07,
    'icy': 0.06  # Possible in distant, cooler orbits
}

class_m_planet_probability = {
    'terrestrial': 0.10,  # Moderate probability, but dependent on star activity
    'superEarth': 0.10,
    'mercuryLike': 0.05,
    'marsLike': 0.05,
    'gasGiant': 0.05,  # Less likely due to smaller star size
    'hotJupiter': 0.03,  # Less likely
    'neptunian': 0.07,
    'ringedPlanet': 0.07,
    'miniNeptune': 0.07,
    'plutoLike': 0.10,  # Possible in distant orbits
    'ceresLike': 0.10,
    'oceanPlanet': 0.08,  # Possible if in the habitable zone
    'venusLike': 0.07,
    'icy': 0.06  # Possible in distant, cooler orbits
}

red_giant_planet_probability = {
    'terrestrial': 0.02,  # Lower probability due to the star's expansion potentially engulfing closer planets
    'superEarth': 0.05,  # Possible, especially in orbits that have moved outwards due to the star's expansion
    'mercuryLike': 0.01,  # Lower probability, as these planets might be engulfed or sterilized
    'marsLike': 0.02,  # Similar to terrestrial, lower probability due to potential engulfment
    'gasGiant': 0.20,  # Higher probability, especially if they have migrated outward
    'hotJupiter': 0.10,  # Possible if they have migrated closer to the star
    'neptunian': 0.15,  # Higher probability in outer orbits
    'ringedPlanet': 0.15,  # Similar to gas giants, likely to be found in outer orbits
    'miniNeptune': 0.10,  # Likely in outer orbits, away from the intense radiation and heat of the star
    'plutoLike': 0.05,  # Possible in very distant orbits
    'ceresLike': 0.03,  # Possible, but less likely due to size and distance factors
    'oceanPlanet': 0.03,  # Possible if in the new habitable zone due to the star's expansion
    'venusLike': 0.01,  # Lower probability due to close proximity to the star
    'icy': 0.05  # Possible, especially if they were previously outside the habitable zone but now within it
}

white_dwarf_planet_probability = {
    'terrestrial': 0.15,  # Possible, especially if they survived the red giant phase of the star
    'superEarth': 0.10,  # Similar to terrestrial, but slightly less common
    'mercuryLike': 0.20,  # Higher probability, as they can survive close to the dense white dwarf
    'marsLike': 0.10,  # Similar to terrestrial planets
    'gasGiant': 0.05,  # Lower probability due to their potential disruption during the star's red giant phase
    'hotJupiter': 0.02,  # Unlikely due to the star's previous expansion and loss of outer layers
    'neptunian': 0.03,  # Similar reasons as gas giants
    'ringedPlanet': 0.03,  # Possible, but less likely due to the star's evolution
    'miniNeptune': 0.05,  # Could exist in outer orbits
    'plutoLike': 0.10,  # Higher probability in distant orbits
    'ceresLike': 0.08,  # Likely to be found in distant orbits
    'oceanPlanet': 0.05,  # Possible if they are in the right zone for liquid water
    'venusLike': 0.02,  # Less likely due to proximity to the white dwarf
    'icy': 0.10  # Possible in distant, cooler orbits
}

neutron_star_planet_probability = {
    'terrestrial': 0.01,  # Very low probability due to the star's intense gravity and harsh conditions
    'superEarth': 0.01,
    'mercuryLike': 0.02,  # Slightly higher probability, but still low due to extreme conditions
    'marsLike': 0.01,
    'gasGiant': 0.05,  # Possible, especially if formed before the star became a neutron star
    'hotJupiter': 0.03,  # Unlikely due to the star's previous evolution
    'neptunian': 0.04,
    'ringedPlanet': 0.03,  # Possible, but less likely due to extreme conditions
    'miniNeptune': 0.03,
    'plutoLike': 0.10,  # Higher probability in distant orbits
    'ceresLike': 0.08,
    'oceanPlanet': 0.01,  # Very low probability due to high radiation and intense gravity
    'venusLike': 0.01,
    'icy': 0.07  # Possible in distant, cooler orbits
}

wolf_rayet_planet_probability = {
    'terrestrial': 0.0001,  # Extremely low probability due to the star's intense radiation and stellar winds
    'superEarth': 0.0001,
    'mercuryLike': 0.0001,  # Extremely low probability due to harsh conditions
    'marsLike': 0.0001,
    'gasGiant': 0.0001,  # Very unlikely due to the star's evolution and intense radiation
    'hotJupiter': 0.0001,  # Extremely unlikely due to the intense conditions
    'neptunian': 0.0001,
    'ringedPlanet': 0.0001,  # Very low probability due to extreme conditions
    'miniNeptune': 0.0001,
    'plutoLike': 0.0001,  # Extremely low probability, even in distant orbits
    'ceresLike': 0.0001,
    'oceanPlanet': 0.0001,  # Almost non-existent probability due to high radiation
    'venusLike': 0.0001,
    'icy': 0.0001  # Extremely low probability, even in distant, cooler orbits
}

class_l_planet_probability = {
    'terrestrial': 0.05,  # Possible, especially if formed in stable zones around the star
    'superEarth': 0.05,
    'mercuryLike': 0.05,  # Likely to exist closer to the star
    'marsLike': 0.05,
    'gasGiant': 0.05,  # Possible, but might be challenging due to the star's low mass and luminosity
    'hotJupiter': 0.05,  # Possible if migrated inward from outer regions
    'neptunian': 0.05,
    'ringedPlanet': 0.05,  # Can exist but less likely due to the star's lower mass
    'miniNeptune': 0.05,
    'plutoLike': 0.05,  # Likely in distant orbits
    'ceresLike': 0.05,
    'oceanPlanet': 0.05,  # Can exist if in the habitable zone
    'venusLike': 0.05,
    'icy': 0.05  # Likely in distant orbits
}

class_t_planet_probability = {
    'terrestrial': 0.25,  # Higher probability due to silicate-rich environments
    'superEarth': 0.20,  # Common as larger silicate worlds
    'mercuryLike': 0.05,  # Possible, especially for smaller, inner planets
    'marsLike': 0.10,  # Likely, given temperate conditions on many Class T worlds
    'gasGiant': 0.02,  # Less common in silicate-rich environments
    'hotJupiter': 0.01,  # Rare, as Class T systems favor terrestrial planets
    'neptunian': 0.02,  # Uncommon in these star systems
    'ringedPlanet': 0.03,  # Possible, particularly for outer planets
    'miniNeptune': 0.02,  # Less likely in silicate-rich systems
    'plutoLike': 0.05,  # Possible in distant orbits
    'ceresLike': 0.05,  # Plausible for smaller bodies in the system
    'oceanPlanet': 0.15,  # Higher probability due to abundant surface water on many Class T worlds
    'venusLike': 0.05,  # Possible, especially for planets closer to the star
    'icy': 0.05  # Possible in distant, cooler orbits
}

class_y_planet_probability = {
    'terrestrial': 0.01,  # Very low probability due to the star's low mass and cool temperature
    'superEarth': 0.01,
    'mercuryLike': 0.01,
    'marsLike': 0.01,
    'gasGiant': 0.05,  # Somewhat higher probability, given the star's low temperature
    'hotJupiter': 0.00,  # Extremely unlikely due to the star's low mass and temperature
    'neptunian': 0.02,
    'ringedPlanet': 0.02,
    'miniNeptune': 0.02,
    'plutoLike': 0.10,  # Higher probability, especially in distant orbits
    'ceresLike': 0.10,
    'oceanPlanet': 0.00,  # Highly unlikely due to the star's cool temperature
    'venusLike': 0.00,
    'icy': 0.55  # Very high probability, suitable for the star's cool temperature
}

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

planet_biome_connections = {
    'terrestrial': {"Forest": 0.1, "Desert": 0.1, "Ocean": 0.1, "Tundra": 0.1, "Grassland": 0.1, "Wetlands": 0.1, "Savanna": 0.1, "Taiga": 0.1, "Chaparral": 0.05, "Temperate Deciduous Forest": 0.05, "Temperate Rainforest": 0.05, "Mediterranean": 0.05, "Montane (Alpine)": 0.05},
    'superEarth': {"Super-Earth Oceanic": 0.2, "Forest": 0.1, "Desert": 0.1, "Ocean": 0.1, "Savanna": 0.1, "Carbon-rich": 0.1, "Iron-rich": 0.3},
    'mercuryLike': {"Lava": 0.5, "Desert": 0.4, "Iron-rich": 0.1},
    'marsLike': {"Desert": 0.4, "Tundra": 0.3, "Subsurface Ocean": 0.3},
    'gasGiant': {"Helium-rich": 0.4, "Ammonia-based": 0.4, "Hydrocarbon Lakes": 0.2},
    'hotJupiter': {"Helium-rich": 0.4, "Ammonia-based": 0.3, "Sulfuric Acid Cloud": 0.3},
    'neptunian': {"Ocean": 0.3, "Ice": 0.4, "Supercritical Fluid": 0.3},
    'ringedPlanet': {"Helium-rich": 0.3, "Coral Reefs": 0.3, "Mangroves": 0.4},
    'miniNeptune': {"Ocean": 0.3, "Ice": 0.3, "Ammonia-based": 0.4},
    'plutoLike': {"Tundra": 0.3, "Ice": 0.4, "Subsurface Ocean": 0.3},
    'ceresLike': {"Desert": 0.3, "Ice": 0.4, "Subsurface Ocean": 0.3},
    'oceanPlanet': {"Ocean": 0.4, "Coral Reefs": 0.3, "Mangroves": 0.2, "Super-Earth Oceanic": 0.1},
    'venusLike': {"Sulfuric Acid Cloud": 0.6, "Chlorine-based Atmosphere": 0.4},
    'icy': {"Ice": 0.5, "Tundra": 0.3, "Subsurface Ocean": 0.2}
}

# Base number of biomes based on planet type
base_biomes = {
    'terrestrial': 5,
    'superEarth': 7,
    'mercuryLike': 1,
    'marsLike': 2,
    'gasGiant': 3,
    'hotJupiter': 2,
    'neptunian': 3,
    'ringedPlanet': 4,
    'miniNeptune': 3,
    'plutoLike': 2,
    'ceresLike': 1,
    'oceanPlanet': 5,
    'venusLike': 2,
    'icy': 3
}

# Baseline atmospheric compositions for different planet types
baseline_compositions = {
    'terrestrial': {'N2': 0.8, 'O2': 0.2},
    'gasGiant': {'H2': 0.9, 'He': 0.1},
    'superEarth': {'CO2': 0.6, 'N2': 0.2, 'O2': 0.2},
    'oceanPlanet': {'N2': 0.7, 'O2': 0.2, 'H2O': 0.1},
    'mercuryLike': {'Na': 0.7, 'O2': 0.2},
    'marsLike': {'CO2': 0.95, 'N2': 0.03},
    'hotJupiter': {'H2': 0.85, 'He': 0.15},
    'neptunian': {'H2': 0.8, 'He': 0.19},
    'ringedPlanet': {'H2': 0.88, 'He': 0.12},
    'miniNeptune': {'H2': 0.6, 'He': 0.4},
    'plutoLike': {'CH4': 0.5, 'N2': 0.4},
    'ceresLike': {'H2O': 0.7, 'CO2': 0.2},
    'venusLike': {'CO2': 0.96, 'N2': 0.03},
    'icy': {'H2O': 0.9, 'CO2': 0.1}
}

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

# Galaxy concepts
galaxy_concepts = {"Milky Way": Concept("Milky Way", "Galaxy")}

# Create concepts for each star class
star_concepts = {}
for star_class, probability in star_probabilities.items():
    star_concepts[star_class] = Concept(star_class, "Star")
    galaxy_concepts["Milky Way"].add_connection(star_concepts[star_class], probability)

# Create Concept instances for each star type and update metadata
for star_type, probability in star_probabilities.items():
    star_concept = Concept(star_type, "Star")
    if star_type in star_metadata:
        for key, value in star_metadata[star_type].items():
            star_concept.update_metadata(key, value)
        for key, value in star_type_masses[star_type].items():
            star_concept.update_metadata(key, value)
    star_concepts[star_type] = star_concept

# Create concepts for each planet type
planet_concepts = {}
for planet_type in planet_types:
    planet_concepts[planet_type] = Concept(planet_type, "Planet")

def add_planet_connections_to_star(star_class, planet_probabilities):
    for planet_type, probability in planet_probabilities.items():
        star_concepts[star_class].add_connection(planet_concepts[planet_type], probability)

# Now call this function for each star class and its corresponding planet probabilities
add_planet_connections_to_star('Class O', class_o_planet_probability)
add_planet_connections_to_star('Class B', class_b_planet_probability)
add_planet_connections_to_star('Class A', class_a_planet_probability)
add_planet_connections_to_star('Class F', class_f_planet_probability)
add_planet_connections_to_star('Class G', class_g_planet_probability)
add_planet_connections_to_star('Class K', class_k_planet_probability)
add_planet_connections_to_star('Class M', class_m_planet_probability)
add_planet_connections_to_star('Red Giant', red_giant_planet_probability)
add_planet_connections_to_star('White Dwarf', white_dwarf_planet_probability)
add_planet_connections_to_star('Neutron Star', neutron_star_planet_probability)
add_planet_connections_to_star('Wolf-Rayet Star', wolf_rayet_planet_probability)
add_planet_connections_to_star('Class L', class_l_planet_probability)
add_planet_connections_to_star('Class T', class_t_planet_probability)
add_planet_connections_to_star('Class Y', class_y_planet_probability)

# Create concepts for each planet type
biome_concepts = {}
for biome_type in biomes:
    biome_concepts[biome_type] = Concept(biome_type, "Biome")

# Update planet_concepts with connections to biomes including probabilities
for planet_type, biome_probs in planet_biome_connections.items():
    for biome, probability in biome_probs.items():
        planet_concepts[planet_type].add_connection(biome, probability)

# Extracting unique biology subcategories from biome_biology_probabilities
unique_biology_subcategories = list(set(subcat for biomes in biome_biology_probabilities.values() for subcat in biomes))

# Create concepts for each planet type
biologic_concepts = {}
for biologic_type in unique_biology_subcategories:
    biologic_concepts[biologic_type] = Concept(biologic_type, "Biological")
    if biologic_type in life_form_metadata:
        for key, value in life_form_metadata[biologic_type].items():
            biologic_concepts[biologic_type].update_metadata(key, value)

# Update biome_concepts with connections to biology subcategories including probabilities
for biome_type, subcategory_probs in biome_biology_probabilities.items():
    for subcategory, probability in subcategory_probs.items():
        biome_concepts[biome_type].add_connection(subcategory, probability)

def create_biological_matrix_row_normalization(biological_types, characteristics):
    """
    Create a matrix for biological types with characteristics based on base and standard deviation values.
    Then apply normalization across each row to convert these values into normalized scores.

    :param biological_types: Dictionary of biological types with characteristics' base and std values
    :param characteristics: List of characteristics to consider
    :return: DataFrame representing the biological characteristics matrix with normalized scores
    """
    # Initialize a DataFrame to hold the matrix values
    matrix_df = pd.DataFrame(index=biological_types.keys(), columns=characteristics)

    # Populate the DataFrame with generated values
    for bio_type, bio_chars in biological_types.items():
        for char in characteristics:
            base, std = bio_chars.get(char, {}).get('base', 0), bio_chars.get(char, {}).get('std', 0)
            matrix_df.at[bio_type, char] = np.random.normal(base, std) if std > 0 else base

    # Replace any NaN values with 0 and apply row-wise normalization
    matrix_df.fillna(0, inplace=True)

    # Adjust normalization to avoid division by zero
    row_sums = matrix_df.sum(axis=1)
    row_sums[row_sums == 0] = 1  # Replace 0 sums with 1 to avoid division by zero
    normalized_matrix = matrix_df.div(row_sums, axis=0)

    return normalized_matrix

def ensure_non_negative_and_normalize_row(row):
    """
    Ensure that all values in the DataFrame row are non-negative and normalize the row.

    :param row: A row from a pandas DataFrame.
    :return: A row with non-negative values that sum to 1.
    """
    # Set negative values to zero
    row[row < 0] = 0

    # Normalize the row to sum to 1
    row_sum = row.sum()
    if row_sum > 0:
        row = row / row_sum
    else:
        # If the sum is zero, assign equal probabilities
        row = pd.Series(1.0 / len(row), index=row.index)
    
    return row

def normalize_rows(matrix_df):
    """
    Normalize the rows of a DataFrame so that each row sums to 1.

    :param matrix_df: The DataFrame to normalize.
    :return: The normalized DataFrame.
    """
    matrix_np = matrix_df.to_numpy()  # Convert to numpy array for multi-dimensional indexing
    row_sums = matrix_np.sum(axis=1, keepdims=True)
    # Avoid division by zero
    row_sums[row_sums == 0] = 1
    return pd.DataFrame(matrix_np / row_sums, index=matrix_df.index, columns=matrix_df.columns)

def estimate_planet_count(star_mass, disk_mass, star_age, environmental_factor):
    """
    Estimate the number of planets in a star system based on various factors.

    Parameters:
    star_mass (float): Mass of the star in solar masses.
    disk_mass (float): Mass of the protoplanetary disk in relation to the star mass.
    star_age (float): Age of the star in billions of years.
    environmental_factor (float): A factor representing environmental influences (e.g., nearby stars, interstellar clouds).

    Returns:
    int: Estimated number of planets in the star system.
    """

    # Base number of planets from disk mass - more massive disks can form more planets.
    base_planets = disk_mass * 10

    # Modify based on star mass - larger stars can have more massive disks but shorter lifespans.
    if star_mass > 1.5:  # more massive than 1.5 solar masses
        base_planets *= 0.8  # fewer stable planets due to shorter star lifespan
    elif star_mass < 0.5:  # less massive than 0.5 solar masses
        base_planets *= 0.6  # smaller disks and potentially less planet formation

    # Age factor - older systems might lose planets or have more stable systems.
    if star_age > 4.5:  # older than the Sun
        base_planets *= 0.9
    elif star_age < 1:  # very young
        base_planets *= 1.1  # potential for more planets, still in formation

    # Environmental factors can add variability.
    base_planets *= environmental_factor

    # Ensure the result is an integer and within realistic bounds.
    estimated_planets = max(1, min(int(base_planets), 15))

    return estimated_planets

def calculate_life_probability(distance_to_star, star_class, atmospheric_composition, magnetic_field_strength, geological_activity, chemical_composition, water_presence, orbital_stability, moon_presence, radiation_level, debug=False):
    """
    Calculate the probability of life on a planet based on various factors.

    Parameters:
    distance_to_star (float): Distance from the star in AU (Astronomical Units).
    star_class (str): Class of the star (e.g., 'Class M', 'Red Giant').
    atmospheric_composition (str): Suitability of atmospheric composition ('none', 'thin', 'thick').
    magnetic_field_strength (float): Strength of the planet's magnetic field in Gauss.
    geological_activity (int): Presence of geological activity (1 for active, 0 for inactive).
    chemical_composition (int): Presence of essential chemicals for life (1 for present, 0 for absent).
    water_presence (int): Presence of liquid water (1 for present, 0 for absent).
    orbital_stability (int): Stability of the planet's orbit (1 for stable, 0 for unstable).
    moon_presence (int): Presence of natural satellites (1 for present, 0 for absent).
    radiation_level (float): Radiation level in Sieverts.

    Returns:
    float: Probability of life existing on the planet (0 to 1).
    """

    # Habitable zone calculation (simplified)
    habitable_zone_factor = math.exp(-((distance_to_star - 1) ** 2) / 0.1)

    # Star type factor
    star_type_factor = base_star_life_probabilities.get(star_class, 0)

    # Atmospheric composition factor
    atmospheric_factor = 0 if atmospheric_composition == 'none' else 1
    if atmospheric_composition == 'thick':
        atmospheric_factor = 1.2
    elif atmospheric_composition == 'thin':
        atmospheric_factor = 0.9

    # Magnetic field factor
    magnetic_field_factor = 1 / (1 + math.exp(-(magnetic_field_strength - 25)))

    # Geological activity factor
    geological_factor = 0 if geological_activity == 0 else 1

    # Chemical composition factor
    chemical_factor = 0 if chemical_composition == 0 else 1

    # Water presence factor
    water_factor = 0 if water_presence == 0 else 1

    # Orbital stability factor
    orbital_stability_factor = 0 if orbital_stability == 0 else 1

    # Moon presence factor
    moon_factor = 0.1 if moon_presence == 0 else 1

    # Radiation level factor
    radiation_factor = 1 / (1 + math.exp((radiation_level - 5)))

    # Calculate overall probability

    probability = (habitable_zone_factor * star_type_factor * atmospheric_factor * magnetic_field_factor * geological_factor * chemical_factor * water_factor * orbital_stability_factor * moon_factor * radiation_factor)
    if debug:
        print("Factors contributing to habitability:")
        print(f" - Habitable Zone Factor: {habitable_zone_factor}")
        print(f" - Star Type Factor: {star_type_factor}")
        print(f" - Atmospheric Factor: {atmospheric_factor}")
        print(f" - Magnetic Field Factor: {magnetic_field_factor}")
        print(f" - Geological Factor: {geological_factor}")
        print(f" - Chemical Factor: {chemical_factor}")
        print(f" - Water Factor: {water_factor}")
        print(f" - Orbital Stability Factor: {orbital_stability_factor}")
        print(f" - Moon Factor: {moon_factor}")
        print(f" - Radiation Factor: {radiation_factor}")
        print(f"Calculated Probability of Habitability: {probability:.4f}")

    return probability

def estimate_biomes(planet_type, atmospheric_composition, water_presence, geological_activity, temperature_range):
    """
    Estimate the number of biomes on a planet based on planet type and other factors.

    Parameters:
    planet_type (str): Type of the planet.
    atmospheric_composition (int): Suitability of atmospheric composition (1 for suitable, 0 for unsuitable).
    water_presence (int): Presence of liquid water (1 for present, 0 for absent).
    geological_activity (int): Presence of geological activity (1 for active, 0 for inactive).
    temperature_range (float): Range of temperature on the planet's surface.

    Returns:
    int: Estimated number of distinct biomes on the planet.
    """

    num_biomes = base_biomes.get(planet_type, 0)

    # Modify based on atmospheric composition
    if atmospheric_composition:
        num_biomes += 1

    # Modify based on water presence
    if water_presence:
        num_biomes += 2

    # Modify based on geological activity
    if geological_activity:
        num_biomes += 1

    # Modify based on temperature range
    if temperature_range > 100:  # Wide temperature range
        num_biomes += 2
    elif temperature_range > 50:  # Moderate temperature range
        num_biomes += 1

    # Ensure the result is within a realistic range
    num_biomes = max(1, min(num_biomes, 10))

    return num_biomes

def estimate_au_from_star(planet_type, star_type, star_mass_kg):
    """
    Estimate the average distance (in Astronomical Units, AU) of a planet from its star based on the planet type, 
    star type, and star mass in kilograms.

    Parameters:
    planet_type (str): Type of the planet.
    star_type (str): Type of the star.
    star_mass_kg (float): Mass of the star in kilograms.

    Returns:
    float: Estimated average distance from the star in AU.
    """

    # Solar mass in kilograms (for conversion)
    solar_mass_kg = 1.989 * 10**30

    # Convert star mass to solar masses
    star_mass_in_solar_masses = star_mass_kg / solar_mass_kg

    # Adjust base AU value based on star type
    adjusted_au = base_au[planet_type] * star_type_scaling.get(star_type, 1.0)

    # Further adjust AU based on star mass (linear scaling)
    mass_adjustment_factor = star_mass_in_solar_masses
    final_au = adjusted_au * mass_adjustment_factor

    return final_au

def estimate_planet_temperature(planet_type, distance_au, atmospheric_composition, star_type):
    """
    Estimate the average day and night temperatures of a planet.

    Parameters:
    planet_type (str): Type of the planet.
    distance_au (float): Distance from the star in AU.
    atmospheric_composition (str): Type of the planet's atmosphere.
    star_type (str): Type of the star.

    Returns:
    tuple: Estimated average day and night temperatures in Celsius.
    """

    star_factor = star_temperature_factors.get(star_type, 1.0)

    # Estimate base temperature using inverse square law (simplified)
    base_temp = 280 / distance_au ** 0.5 * star_factor

    # Adjust base temperature for planet type
    if planet_type in ['gasGiant', 'hotJupiter', 'neptunian']:
        base_temp *= 1.1  # Higher base temperature for gas giants
    elif planet_type in ['terrestrial', 'superEarth', 'oceanPlanet']:
        base_temp *= 1.0  # Standard for terrestrial planets
    else:
        base_temp *= 0.9  # Lower for smaller or less dense planets

    # Atmospheric adjustment
    if atmospheric_composition == 1:
        greenhouse_effect = 1.2
    elif atmospheric_composition == 0:
        greenhouse_effect = 0.9
    else:
        greenhouse_effect = 1.0

    adjusted_temp = base_temp * greenhouse_effect

    # Estimate day-night temperature variation
    if planet_type in ['terrestrial', 'superEarth', 'oceanPlanet']:
        day_night_variation = 40  # Higher variation for solid surfaces
    else:
        day_night_variation = 20  # Lower variation for gas giants

    day_temp = adjusted_temp + day_night_variation / 2
    night_temp = adjusted_temp - day_night_variation / 2

    # Convert temperatures to Celsius
    day_temp_celsius = day_temp - 273.15
    night_temp_celsius = night_temp - 273.15

    return (day_temp_celsius, night_temp_celsius)

def estimate_atmosphere(planet_type, distance_au, star_type):
    """
    Estimate the atmospheric composition and thickness based on the planet type, distance from the star, and star type.

    Parameters:
    planet_type (str): Type of the planet.
    distance_au (float): Distance from the star in AU.
    star_type (str): Type of the star.

    Returns:
    str: Estimated atmospheric composition and thickness.
    """

    # Default atmospheric composition and thickness
    atmosphere = "none"

    # Planet type-based assumptions
    if planet_type in ['gasGiant', 'hotJupiter', 'neptunian', 'ringedPlanet', 'miniNeptune']:
        atmosphere = "thick"
    elif planet_type in ['terrestrial', 'superEarth', 'oceanPlanet']:
        if distance_au < 0.5:
            atmosphere = np.random.choice(["thin", "none"], p=[0.9, 0.1])
        elif 0.5 <= distance_au <= 1.5:
            atmosphere = "thick"
        else:
            atmosphere = np.random.choice(["thin", "none"], p=[0.8, 0.2])
    elif planet_type in ['mercuryLike', 'plutoLike', 'ceresLike', 'icy']:
        atmosphere = np.random.choice(["thin", "none"], p=[0.2, 0.8])
    elif planet_type in ['venusLike']:
        atmosphere = np.random.choice(["thick", "thin"], p=[0.8, 0.2])
    elif planet_type in ['marsLike']:
        atmosphere = np.random.choice(["none", "thin"], p=[0.2, 0.8])
    
    # Adjustments based on star type
    if star_type in ['Class O', 'Class B']:
        atmosphere = "none"

    return atmosphere

def estimate_atmospheric_composition(planet_type, distance_au, atmosphere_thickness):
    """
    Estimate the atmospheric composition of a planet, considering the distance from the star (AU).

    Parameters:
    planet_type (str): Type of the planet.
    distance_au (float): Distance from the star in AU.
    atmosphere_thickness (str): Thickness of the atmosphere ('Thin', 'Moderate', 'Thick', 'None').

    Returns:
    dict: Estimated atmospheric composition as a dictionary of molecules and their relative percentages.
    """

    # Return an empty dictionary if there is no atmosphere
    if atmosphere_thickness == 'none':
        return {}

    # Select the baseline composition for the given planet type
    composition = baseline_compositions.get(planet_type, {'N2': 0.8, 'O2': 0.2})

    if atmosphere_thickness == 'thick':
        # Increase the variety and complexity for thick atmospheres
        composition['CO2'] = composition.get('CO2', 0) + np.random.uniform(0, 0.1)
        composition['CH4'] = np.random.uniform(0, 0.05)
    elif atmosphere_thickness == 'thin':
        # Reduce the complexity for thin atmospheres
        dominant_gas = max(composition, key=composition.get)
        composition = {dominant_gas: 1.0}

    # Adjustments based on distance from the star (AU)
    if distance_au < 0.5:
        # Closer to the star, more likely to have thinner atmospheres with less volatile compounds
        composition = {k: v * np.random.uniform(0.7, 1.0) for k, v in composition.items()}
    elif distance_au > 1.5:
        # Farther from the star, atmospheres might retain more volatile compounds
        composition = {k: v * np.random.uniform(1.0, 1.3) for k, v in composition.items()}

    # Normalize percentages to sum to 1
    total_percentage = sum(composition.values())
    for gas in composition:
        composition[gas] /= total_percentage

    return composition

def check_essential_chemicals_for_life(atmospheric_composition):
    """
    Check if the essential chemicals for known life are present in the given atmospheric composition.

    Parameters:
    atmospheric_composition (dict): Atmospheric composition as a dictionary of molecules and their relative percentages.

    Returns:
    bool: True if essential chemicals are present, False otherwise.
    """

    # Essential chemicals for known life
    essential_chemicals = ['N2', 'O2', 'CO2', 'H2O']

    # Check if any of the essential chemicals are present in the atmosphere
    for chemical in essential_chemicals:
        if chemical in atmospheric_composition and atmospheric_composition[chemical] > 0:
            return True

    return False

def estimate_water_presence_and_coverage(planet_type, distance_au, temperature_range, star_type, atmospheric_thickness, magnetic_field_strength, geological_activity, volcanism, core_activity):
    """
    Estimate the presence and surface coverage of water on a planet, considering various factors.

    Parameters:
    planet_type (str): Type of the planet.
    distance_au (float): Distance from the star in AU.
    temperature_range (tuple): Temperature range (min, max) in Celsius.
    star_type (str): Type of the star.
    atmospheric_composition (dict): Atmospheric composition.
    magnetic_field_strength (float): Strength of the planet's magnetic field.
    geological_activity (float): Measure of geological activity.
    volcanism (float): Measure of volcanic activity.
    core_activity (float): Measure of core activity.

    Returns:
    tuple: (bool, float) indicating whether water is present and the estimated percentage of surface coverage.
    """
    max_temp, min_temp = temperature_range
    water_presence = False
    water_coverage = 0.0

    # print(f" - Planet Type: {planet_type}")
    # print(f"{habitable_zone[star_type][0]} <= {distance_au} <= {habitable_zone[star_type][1]}")
    # print(f"({max_temp > 0} and {min_temp < 100})")

    # Check if planet is within the habitable zone of the star
    if habitable_zone[star_type][0] <= distance_au <= habitable_zone[star_type][1] and (max_temp > 0 and min_temp < 100):
        water_presence = True

        # Estimate water coverage based on planet type and other factors
        if planet_type == 'oceanPlanet':
            water_coverage = np.random.uniform(70, 100)
        elif planet_type in ['terrestrial', 'superEarth']:
            water_coverage = np.random.uniform(50, 70)
        elif planet_type in ['gasGiant', 'hotJupiter', 'neptunian']:
            water_presence = False
        else:
            # Basic estimation for unknown types, considering geological and volcanic activity
            if geological_activity > 0.5 and volcanism > 0.5:
                water_coverage = np.random.uniform(30, 50)
        
        # Adjust water coverage based on atmospheric composition and magnetic field
        if atmospheric_thickness == 'thick' or magnetic_field_strength > 5:
            water_coverage = min(water_coverage * 1.1, 100)  # Increase coverage but cap at 100%

        # Consider core activity which might influence geological heating
        if core_activity > 0.5:
            water_coverage = min(water_coverage * 1.2, 100)  # Increase coverage but cap at 100%

    return water_presence, water_coverage

def determine_core_activity(planet_type):
    """
    Determine the activity of the molten core based on the planet type.

    :param planet_type: Type of the planet.
    :return: Activity status of the core ('alive' or 'dead').
    """

    if planet_type in active_core_planets:
        return 1
    elif planet_type in inactive_core_planets:
        return 0
    else:
        # For uncertain or unknown types, assign randomly based on general probability
        return np.random.choice(['alive', 'dead'])
    
def estimate_magnetic_field(star_type, distance_au, core_activity, planet_type):
    """
    Estimate the magnetic field strength of a planet.

    :param star_type: Type of the star.
    :param distance_au: Distance from the star in AU.
    :param core_activity: Activity status of the core ('alive' or 'dead').
    :param planet_type: Type of the planet.
    :return: Estimated magnetic field strength in Gauss.
    """

    # Adjustments based on distance from the star
    distance_factor = 1 / (distance_au ** 0.5)

    # Adjustments based on core activity
    core_activity_factor = 2 if core_activity == 1 else 0.5

    # Factor in the star type's impact on the planet's magnetic field
    star_impact_factor = star_type_impact.get(star_type, 1.0)  # Default to 1.0 if star type is unknown

    # Calculate the estimated magnetic field strength
    base_field = base_magnetic_fields.get(planet_type, 0.1)  # Default to a low value if unknown type
    magnetic_field_strength = base_field * distance_factor * core_activity_factor * star_impact_factor

    return magnetic_field_strength * 10.0 # Convert to Gauss

def estimate_orbital_period(distance_au, star_mass_kg):
    """
    Estimate the orbital period of a planet based on its distance from the star and the star's mass in kilograms.

    Parameters:
    distance_au (float): Average distance from the star in Astronomical Units.
    star_mass_kg (float): Mass of the star in kilograms.

    Returns:
    float: Estimated orbital period in Earth years.
    """
    # Constants
    G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2
    solar_mass_kg = 1.989e30  # Mass of the Sun in kilograms

    # Convert AU to meters (1 AU = 1.496e+11 meters)
    distance_meters = distance_au * 1.496e+11

    # Calculate the orbital period in seconds using Kepler's Third Law
    # P^2 = 4 * pi^2 * a^3 / (G * M)
    orbital_period_seconds = ((4 * 3.14159 ** 2 * distance_meters ** 3) / (G * star_mass_kg)) ** 0.5

    # Convert the orbital period from seconds to years
    orbital_period_years = orbital_period_seconds / (365.25 * 24 * 60 * 60)

    return orbital_period_years

def estimate_volcanic_activity(core_activity, magnetic_field_strength, planet_type, planetary_age, distance_au, nearby_planet_masses=[]):
    """
    Estimate the level of volcanic activity on a planet, considering tidal heating and solar radiation effects.

    Parameters:
    core_activity (str): Activity level of the planet's core ('High', 'Moderate', 'Low', 'Inactive').
    magnetic_field_strength (float): Strength of the planet's magnetic field in Gauss.
    planet_type (str): Type of the planet ('Terrestrial', 'Gas Giant', etc.).
    planetary_age (float): Age of the planet in billions of years.
    distance_au (float): Distance from the star in Astronomical Units.
    nearby_planet_masses (list): Masses of nearby planets in solar masses (for calculating tidal heating).

    Returns:
    str: Estimated level of volcanic activity ('High', 'Moderate', 'Low', 'Inactive').
    """
    # Tidal heating factor
    tidal_heating = False
    if nearby_planet_masses and distance_au < 1.0:
        tidal_heating = True  # Assuming significant tidal heating for close planets in multi-planet systems

    # Solar radiation factor
    solar_radiation_effect = False
    if distance_au < 0.5:
        solar_radiation_effect = True  # Increased effect for planets very close to their star

    # Basic logic to determine volcanic activity
    if core_activity == 0 or planet_type not in ['Terrestrial', 'Gas Giant']:
        return 0

    if core_activity == 1 or magnetic_field_strength > 25 or tidal_heating:
        return 1

    if core_activity == 1 or (magnetic_field_strength > 10 and planetary_age < 4) or solar_radiation_effect:
        return 0.5

    return 0.25

# Create probability matrices for each connection
galaxy_names = list(galaxy_concepts.keys())
star_names = list(star_concepts.keys())
planet_names = list(planet_concepts.keys())
biome_names = list(set(b for biomes in planet_biome_connections.values() for b in biomes))
life_form_characteristic_names = list(set(b for biomes in life_form_characteristics.values() for b in biomes))

# Initialize DataFrames with float dtype
gx_s_df = pd.DataFrame(0.0, index=galaxy_names, columns=star_names)
sx_p_df = pd.DataFrame(0.0, index=star_names, columns=planet_names)
px_b_df = pd.DataFrame(0.0, index=planet_names, columns=biome_names)
bx_b_df = pd.DataFrame(0.0, index=biome_names, columns=unique_biology_subcategories)

# Step 1: Create GxS DataFrame
gx_s_df = pd.DataFrame(0.0, index=galaxy_names, columns=star_names)
for galaxy in galaxy_names:
    for connection in galaxy_concepts[galaxy].get_connections():
        gx_s_df.at[galaxy, connection['concept'].name] = connection['probability']

# Step 2: Create SxP DataFrame
sx_p_df = pd.DataFrame(0.0, index=star_names, columns=planet_names)
for star in star_names:
    for connection in star_concepts[star].get_connections():
        sx_p_df.at[star, connection['concept'].name] = connection['probability']

# Create the PxB DataFrame
px_b_df = pd.DataFrame(0.0, index=planet_names, columns=biome_names)
for planet in planet_names:
    for biome, probability in planet_biome_connections.get(planet, {}).items():
        if biome in biome_names:
            px_b_df.at[planet, biome] = probability

# Initialize the Biome x Biology DataFrame
bx_b_df = pd.DataFrame(0.0, index=biome_names, columns=unique_biology_subcategories)

# Populate the DataFrame with probabilities
for biome in biome_names:
    for subcategory, probability in biome_biology_probabilities.get(biome, {}).items():
        if subcategory in unique_biology_subcategories:
            bx_b_df.at[biome, subcategory] = probability

# Create the biological matrix with row normalization
biological_matrix_row_norm = create_biological_matrix_row_normalization(life_form_characteristics, life_form_characteristic_names)

# Initialize the Biology x Individual Characteristics DataFrame
biology_x_individual_df = pd.DataFrame(0.0, index=biological_matrix_row_norm.index, columns=life_form_characteristic_names)

# Populate the DataFrame with normalized values
for biology_type in biological_matrix_row_norm.index:
    for characteristic in life_form_characteristic_names:
        biology_x_individual_df.at[biology_type, characteristic] = biological_matrix_row_norm.at[biology_type, characteristic]

# Normalize rows of GxS, SxP, PxB, and BxBio DataFrames
normalized_gx_s_df = normalize_rows(gx_s_df)
normalized_sx_p_df = normalize_rows(sx_p_df)
normalized_px_b_df = normalize_rows(px_b_df)
normalized_bx_b_df = normalize_rows(bx_b_df)
normalized_bx_lf_df = normalize_rows(biology_x_individual_df)

# Multiply normalized GxS, SxP, PxB, and BxBio DataFrames to get GxBio DataFrame
gx_p_df = normalized_gx_s_df.dot(normalized_sx_p_df)
gx_b_df = gx_p_df.dot(normalized_px_b_df)
gx_bb_df = gx_b_df.dot(normalized_bx_b_df)
gx_bl_df = gx_bb_df.dot(normalized_bx_lf_df)

# print(gx_bb_df)
# print(gx_b_df)
# print(gx_p_df)
# print(gx_bl_df)

for x in range(10000):
    # Sample a star type based on galaxy
    star_probabilities = normalized_gx_s_df.iloc[0]
    star_type = np.random.choice(star_names, p=star_probabilities)

    # Find the index of the sampled star type
    star_index = star_names.index(star_type)

    # Create star specific information
    star_mass_range = star_concepts[star_type].metadata['mass_range_kg']
    if np.isinf(star_mass_range[1]):
        # Use an alternative distribution here. 
        # Example: Exponential distribution with mean = star_mass_range[0]
        star_mass_kg = np.random.exponential(star_mass_range[0])
    else:
        star_mass_kg = np.random.uniform(star_mass_range[0], star_mass_range[1])

    star_age_range = star_concepts[star_type].metadata['age_range_Gyr']
    star_age_Gyr = np.random.uniform(star_age_range[0], star_age_range[1])

    disk_mass_range = star_concepts[star_type].metadata['disk_mass_percentage_of_solar_mass']
    disk_mass = np.random.uniform(disk_mass_range[0], disk_mass_range[1])

    # Estimate number of planets
    num_planets = estimate_planet_count(star_mass_kg, disk_mass, star_age_Gyr, 1.0)

    solar_system_info = {
        "Star": star_type,
        "Star Information": star_concepts[star_type].metadata,
        "Star Mass (kg)": star_mass_kg,
        "Star Age (Gyr)": star_age_Gyr,
        "Number of Planets": num_planets,
        "Disk Mass": disk_mass,
        "Planets": []
    }

    # Sample a planet type based on star type
    planet_probabilities = normalized_sx_p_df.iloc[star_index]
    for n in range(num_planets):

        planet_type = np.random.choice(planet_names, p=planet_probabilities)

        # Find the index of the sampled planet type
        planet_index = planet_names.index(planet_type)

        estimated_au = estimate_au_from_star(planet_type, star_type, star_mass_kg)

        core_activity = determine_core_activity(planet_type)

        # Sample atmosphere thickness
        estimated_atmosphere_thickness = estimate_atmosphere(planet_type, estimated_au, star_type)

        estimated_temperatures = estimate_planet_temperature(planet_type, estimated_au, estimated_atmosphere_thickness, star_type)

        temperature_temp_range = estimated_temperatures[0] - estimated_temperatures[1]

        # Sample atmosphere composition
        atmosphere_composition = estimate_atmospheric_composition(planet_type, estimated_au, estimated_atmosphere_thickness)

        magnetic_field = estimate_magnetic_field(
            star_type,
            estimated_au,
            core_activity,
            planet_type
        )
        magnetic_field_strength_tesla = magnetic_field / 10000.0

        # Updated function call with the new parameters
        water_presence, water_coverage = estimate_water_presence_and_coverage(
            planet_type, 
            estimated_au, 
            estimated_temperatures, 
            star_type,
            estimated_atmosphere_thickness,
            magnetic_field_strength_tesla,
            1, #geological_activity,
            1, #volcanism,
            core_activity
        )

        # Special setting atmospheric composition for water presence
        if water_presence:
            atmosphere_composition['H2O'] = np.random.uniform(0.05, 0.1)

        estimated_biomes = estimate_biomes(
            planet_type,
            estimated_atmosphere_thickness,
            water_presence,
            core_activity,
            temperature_temp_range
        )

        orbital_period = estimate_orbital_period(estimated_au, star_mass_kg)
        orbital_period_days = orbital_period * 365.25

        # Example usage of the function
        probability = calculate_life_probability(
            distance_to_star=estimated_au,  # in AU
            star_class=star_type,         # stable star
            atmospheric_composition=estimated_atmosphere_thickness,  # suitable atmosphere
            magnetic_field_strength=magnetic_field,  # in Gauss
            geological_activity=core_activity,       # active geology
            chemical_composition=check_essential_chemicals_for_life(atmosphere_composition),
            water_presence=water_presence,            # liquid water present
            orbital_stability=1,         # stable orbit
            moon_presence=1,             # moon present
            radiation_level=3            # radiation level in Sieverts
        )

        # print("TESTING EARTH")
        # print(calculate_life_probability(
        #     distance_to_star=1,  # in AU
        #     star_class="Class G",         # stable star
        #     atmospheric_composition='thick',  # suitable atmosphere
        #     magnetic_field_strength=30,  # in Gauss
        #     geological_activity=1,       # active geology
        #     chemical_composition=check_essential_chemicals_for_life(atmosphere_composition),
        #     water_presence=True,            # liquid water present
        #     orbital_stability=1,         # stable orbit
        #     moon_presence=1,             # moon present
        #     radiation_level=3            # radiation level in Sieverts
        # ))

        if np.random.rand() <= probability:
            life_presence = True
        else:
            life_presence = False

        planet_info = {
            "Planet Type": planet_type,
            "AU": estimated_au,
            "Life Probability": probability,
            "Life Presence": life_presence,
            "Temperature Range (day/night)": estimated_temperatures,
            "Biomes": {},
            "Atmosphere Thickness": estimated_atmosphere_thickness,
            "Atmospheric Composition": atmosphere_composition,
            "Water Presence": water_presence,
            "Water Coverage": water_coverage,
            "Core Activity": core_activity,
            "Magnetic Field (Gauss)": magnetic_field,
            "Orbital Period (year)": orbital_period,
            "Orbital Period (days)": orbital_period_days
        }

        for n in range(estimated_biomes):
            biome_type = np.random.choice(biome_names, p=normalized_px_b_df.iloc[planet_index])

            biome_index = biome_names.index(biome_type)
            
            lifeforms = []
            
            if life_presence:
                biological_probabilities = normalized_bx_b_df.iloc[biome_index]
                biological_type = np.random.choice(unique_biology_subcategories, p=biological_probabilities)

                biological_index = unique_biology_subcategories.index(biological_type)

                life_form_characteristic_probabilities = normalized_bx_lf_df.iloc[biological_index]
                adjusted_probabilities = ensure_non_negative_and_normalize_row(life_form_characteristic_probabilities)
                life_form_characteristic_list = list(set(np.random.choice(life_form_characteristic_names, p=adjusted_probabilities, size=5)))

                bio_info = {
                    "Biological": biological_type,
                    "Biological Characteristics": biologic_concepts[biological_type].metadata,
                    "Life Form Characteristics": life_form_characteristic_list
                }

                lifeforms.append(bio_info)

            biome_info = {
                "Biome Type": biome_type,
                "Lifeforms": lifeforms,
            }

            if biome_type not in planet_info["Biomes"]:
                planet_info["Biomes"][biome_type] = {}

            planet_info["Biomes"][biome_type].update(biome_info)

        solar_system_info["Planets"].append(planet_info)

    if life_presence:
        print(f"Life exists on this planet! after {x} iterations")
        pretty_json = json.dumps(solar_system_info, indent=4)
        print(pretty_json)
        
        # Calculate overall probability
        probability = calculate_life_probability(
            distance_to_star=estimated_au,  # in AU
            star_class=star_type,         # stable star
            atmospheric_composition=estimated_atmosphere_thickness,  # suitable atmosphere
            magnetic_field_strength=magnetic_field,  # in Gauss
            geological_activity=core_activity,       # active geology
            chemical_composition=check_essential_chemicals_for_life(atmosphere_composition),
            water_presence=water_presence,            # liquid water present
            orbital_stability=1,         # stable orbit
            moon_presence=1,             # moon present
            radiation_level=3,           # radiation level in Sieverts
            debug=True
        )
        break

    # Pretty print the JSON representation of the solar system
    # pretty_json = json.dumps(solar_system_info, indent=4)
    # print(pretty_json)