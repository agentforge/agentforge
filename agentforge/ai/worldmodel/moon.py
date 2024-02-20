import random

class Moon:

    def determine_moon_properties(self, moon_type, planet_type, planet_size, planet_distance_from_star):
        """
        Determine the size, AU range, orbital stability, gravitational influence, and composition of a moon based on
        moon type, planet type, planet size, and planet's distance from its star.

        :param moon_type: Type of the moon.
        :param planet_type: Type of the planet.
        :param planet_size: Size of the planet (in kg).
        :param planet_distance_from_star: Distance of the planet from its star (in AU).
        :param exomoons_categories: Dictionary of moon categories with their properties.
        :return: Size, AU range, orbital stability, gravitational influence, and composition of the moon.
        """
        if moon_type not in self.exomoons_categories:
            return "Unknown moon type", None

        # Base properties from exomoons_categories
        moon_properties = self.exomoons_categories.get(moon_type, {})
        moon_size_range = moon_properties.get("size_range_kg", [0, 0])
        moon_stability = moon_properties.get("orbital_stability", 0)
        moon_au_range = moon_properties.get("au_range", [0, 0])
        moon_composition = moon_properties.get("composition", "Unknown")

        # Adjusting moon size
        moon_size_factor = (planet_size / 5.97e24) ** (1/3)  # Earth's mass as a reference
        moon_size = random.uniform(moon_size_range[0], moon_size_range[1]) * moon_size_factor

        # Adjusting orbital stability
        stability_factor = 1
        if planet_type in ["gasGiant", "hotJupiter"]:
            stability_factor *= 0.8  # Less stable due to strong gravitational interactions
        if moon_type == "Captured Moon":
            stability_factor *= 0.6  # Generally less stable orbits
        adjusted_stability = moon_stability * stability_factor

        # Adjusting AU range
        au_factor = (planet_size / 5.97e24) ** (1/3)  # Adjusting for volume
        moon_au = random.uniform(moon_au_range[0], moon_au_range[1]) * au_factor

        # Gravitational Influence
        # Assuming a basic gravitational influence calculation based on size and distance
        gravitational_influence = moon_size / (moon_au ** 2)

        # Adjust composition based on distance from the star
        if planet_distance_from_star > 2 and 'Icy' in moon_composition:
            moon_composition += ', potentially with subsurface ocean'

        return moon_size, moon_au, adjusted_stability, gravitational_influence, moon_composition


    exomoons_categories = {
        "Regular Moon": {
            "description": "Moons that orbit their parent planet in a regular, predictable manner.",
            "examples": ["Earth's Moon", "Phobos", "Deimos", "Europa", "Titan", "Triton", "Charon", "Nix", "Hydra"],
            "size_range_kg": [1e+16, 7.35e+22],
            "orbital_stability": 1,
            "au_range": [0.002, 0.5]  # General estimate for regular moons
        },
        "Irregular Moon": {
            "description": "Moons with eccentric orbits and diverse compositions, often found around gas giants.",
            "examples": ["S/2003 J12 (Jupiter)", "Aegir (Saturn)"],
            "size_range_kg": [1e+14, 1e+19],
            "orbital_stability": 0.5,
            "au_range": [0.2, 0.7]  # Estimating a wider range for irregular moons
        },
        "Captured Moon": {
            "description": "Moons that are believed to be captured from elsewhere, possibly from the Kuiper Belt or asteroid belt.",
            "examples": ["Triton (Neptune)"],
            "size_range_kg": [2.14e+22, 2.14e+22],
            "orbital_stability": 0.7,
            "au_range": [0.2, 0.5]  # Captured moons can have varied orbits
        },
        "Large Exomoon": {
            "description": "Hypothetical moons around exoplanets, likely to be large and potentially observable with future technology.",
            "examples": ["Hypothetical large exomoons orbiting gas giants in exoplanetary systems"],
            "size_range_kg": [1e+20, 1e+23],
            "orbital_stability": 0.8,
            "au_range": [0.1, 1.0]  # Hypothetical range for large exomoons
        },
        "Icy Moon": {
            "description": "Moons with significant ice content, potentially harboring subsurface oceans.",
            "examples": ["Europa (Jupiter)", "Enceladus (Saturn)"],
            "size_range_kg": [1e+19, 4.8e+22],
            "orbital_stability": 0.9,
            "au_range": [0.002, 0.5]  # Similar to regular moons
        },
        "Volcanically Active Moon": {
            "description": "Moons with active volcanism, contributing to dynamic and changing surfaces.",
            "examples": ["Io (Jupiter)"],
            "size_range_kg": [8.93e+22, 8.93e+22],
            "orbital_stability": 0.6,
            "au_range": [0.002, 0.5]  # Typically closer to their parent planets
        },
        "Double Planetary System": {
            "description": "Systems where a moon is large enough relative to its planet to form a double planet system.",
            "examples": ["Pluto-Charon system"],
            "size_range_kg": [1.52e+22, 1.52e+22],
            "orbital_stability": 1,
            "au_range": [0.002, 0.5]  # Orbit of Charon around Pluto as an example
        },
        "Hypothetical Habitable Moon": {
            "description": "Moons that might have conditions suitable for life, especially those with subsurface oceans or atmospheres.",
            "examples": ["Hypothetical moons around exoplanets with conditions suitable for life"],
            "size_range_kg": [1e+19, 1e+23],
            "orbital_stability": 0.9,
            "au_range": [0.1, 1.0]  # Estimating a range for potentially habitable exomoons
        }
    }