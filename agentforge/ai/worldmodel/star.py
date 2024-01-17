import numpy as np
from .concept import Concept
class Star:

    def __init__(self):
        # Create concepts for each star class
        self.star_concepts = {}
        for star_class in self.star_probabilities.keys():
            self.star_concepts[star_class] = Concept(star_class, "Star")

        # Create Concept instances for each star type and update metadata
        for star_type in self.star_probabilities.keys():
            star_concept = Concept(star_type, "Star")
            if star_type in self.star_metadata:
                for key, value in self.star_metadata[star_type].items():
                    star_concept.update_metadata(key, value)
                for key, value in self.star_type_masses[star_type].items():
                    star_concept.update_metadata(key, value)
            self.star_concepts[star_type] = star_concept

    def create_connections_for_star(self, planet):
            
        def add_planet_connections_to_star(star_class, planet_probabilities):
            for planet_type, probability in planet_probabilities.items():
                self.star_concepts[star_class].add_connection(planet.planet_concepts[planet_type], probability)

        # Now call this function for each star class and its corresponding planet probabilities
        add_planet_connections_to_star('Class O', self.class_o_planet_probability)
        add_planet_connections_to_star('Class B', self.class_b_planet_probability)
        add_planet_connections_to_star('Class A', self.class_a_planet_probability)
        add_planet_connections_to_star('Class F', self.class_f_planet_probability)
        add_planet_connections_to_star('Class G', self.class_g_planet_probability)
        add_planet_connections_to_star('Class K', self.class_k_planet_probability)
        add_planet_connections_to_star('Class M', self.class_m_planet_probability)
        add_planet_connections_to_star('Red Giant', self.red_giant_planet_probability)
        add_planet_connections_to_star('White Dwarf', self.white_dwarf_planet_probability)
        add_planet_connections_to_star('Neutron Star', self.neutron_star_planet_probability)
        add_planet_connections_to_star('Wolf-Rayet Star', self.wolf_rayet_planet_probability)
        add_planet_connections_to_star('Class L', self.class_l_planet_probability)
        add_planet_connections_to_star('Class T', self.class_t_planet_probability)
        add_planet_connections_to_star('Class Y', self.class_y_planet_probability)

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
            "mass_range_kg": [32 * 1.989e30, 2.9835000000000002e+32],
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
            "mass_range_kg": [40 * 1.989e30, 2.9835000000000002e+32],
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