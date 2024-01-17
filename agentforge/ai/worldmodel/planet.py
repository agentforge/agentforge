import random, math
import numpy as np
from .star import Star
from .moon import Moon
from .concept import Concept

class Planet:

    def __init__(self):
        self.star = Star()
        self.moon = Moon()

        # Create concepts for each planet type
        self.planet_concepts = {}
        for planet_type in self.planet_types:
            self.planet_concepts[planet_type] = Concept(planet_type, "Planet")

        # Update planet_concepts with connections to biomes including probabilities
        for planet_type, biome_probs in self.planet_biome_connections.items():
            for biome, probability in biome_probs.items():
                self.planet_concepts[planet_type].add_connection(biome, probability)

    def generate(self, planet_type, star_mass_kg, star_type):
        moon_cnt = self.estimate_moons(planet_type)
        moons = []
        for _ in range(moon_cnt):
            moon_type = self.determine_moon_type(planet_type)            
            moon_size, moon_au, moon_stability, moon_grav, moon_composition = self.moon.determine_moon_properties(
                moon_type, 
                planet_type, 
                star_mass_kg, 
                1
            )
            moons.append({
                "Type": moon_type,
                "Size (kg)": moon_size,
                "Distance (AU)": moon_au,
                "Stability": moon_stability,
                "Gravitational Influence": moon_grav,
                "Composition": moon_composition,
            })

        estimated_au = self.estimate_au_from_star(planet_type, star_type, star_mass_kg)

        core_activity = self.determine_core_activity(planet_type)

        # Sample atmosphere thickness
        estimated_atmosphere_thickness = self.estimate_atmosphere(planet_type, estimated_au, star_type)

        estimated_temperatures = self.estimate_planet_temperature(planet_type, estimated_au, estimated_atmosphere_thickness, star_type)

        temperature_temp_range = estimated_temperatures[0] - estimated_temperatures[1]

        # Sample atmosphere composition
        atmosphere_composition = self.estimate_atmospheric_composition(planet_type, estimated_au, estimated_atmosphere_thickness)

        magnetic_field = self.estimate_magnetic_field(
            core_activity,
            planet_type
        )
        magnetic_field_strength_tesla = magnetic_field / 10000.0

        # Updated function call with the new parameters
        water_presence, water_coverage = self.estimate_water_presence_and_coverage(
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

        estimated_biomes = self.estimate_biomes(
            planet_type,
            estimated_atmosphere_thickness,
            water_presence,
            core_activity,
            temperature_temp_range
        )

        orbital_period = self.estimate_orbital_period(estimated_au, star_mass_kg)
        orbital_period_days = orbital_period * 365.25

        # Example usage of the function
        probability = self.calculate_life_probability(
            distance_to_star=estimated_au,  # in AU
            star_class=star_type,         # stable star
            atmospheric_composition=estimated_atmosphere_thickness,  # suitable atmosphere
            magnetic_field_strength=magnetic_field,  # in Gauss
            geological_activity=core_activity,       # active geology
            chemical_composition=self.check_essential_chemicals_for_life(atmosphere_composition),
            water_presence=water_presence,            # liquid water present
            orbital_stability=1,         # stable orbit
            moon_presence=moon_cnt != 0, # moon present
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
            "Orbital Period (days)": orbital_period_days,
            "Moons": moons,
        }

        return planet_info, estimated_biomes, life_presence


    def calculate_life_probability(self, distance_to_star, star_class, atmospheric_composition, magnetic_field_strength, geological_activity, chemical_composition, water_presence, orbital_stability, moon_presence, radiation_level, debug=False):
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
        star_type_factor = self.star.base_star_life_probabilities.get(star_class, 0)

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

    def estimate_au_from_star(self, planet_type, star_type, star_mass_kg):
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
        adjusted_au = self.base_au[planet_type] * self.star_type_scaling.get(star_type, 1.0)

        # Further adjust AU based on star mass (linear scaling)
        mass_adjustment_factor = star_mass_in_solar_masses
        final_au = adjusted_au * mass_adjustment_factor

        return final_au

    def estimate_planet_temperature(self, planet_type, distance_au, atmospheric_composition, star_type):
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

        star_factor = self.star.star_temperature_factors.get(star_type, 1.0)

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

    def estimate_atmosphere(self, planet_type, distance_au, star_type):
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

    def estimate_atmospheric_composition(self, planet_type, distance_au, atmosphere_thickness):
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
        composition = self.baseline_compositions.get(planet_type, {'N2': 0.8, 'O2': 0.2})

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

    def check_essential_chemicals_for_life(self, atmospheric_composition):
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

    def estimate_water_presence_and_coverage(self, planet_type, distance_au, temperature_range, star_type, atmospheric_thickness, magnetic_field_strength, geological_activity, volcanism, core_activity):
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
        if self.star.habitable_zone[star_type][0] <= distance_au <= self.star.habitable_zone[star_type][1] and (max_temp > 0 and min_temp < 100):
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

    def determine_core_activity(self, planet_type):
        """
        Determine the activity of the molten core based on the planet type.

        :param planet_type: Type of the planet.
        :return: Activity status of the core ('alive' or 'dead').
        """

        if planet_type in self.active_core_planets:
            return 1
        elif planet_type in self.inactive_core_planets:
            return 0
        else:
            # For uncertain or unknown types, assign randomly based on general probability
            return np.random.choice(['alive', 'dead'])
        
    def estimate_magnetic_field(self, core_activity, planet_type):
        """
        Estimate the magnetic field strength of a planet.

        :param core_activity: Activity status of the core ('alive' or 'dead').
        :param planet_type: Type of the planet.
        :return: Estimated magnetic field strength in Gauss.
        """

        # Core activity factor
        core_activity_factor = 2 if core_activity == 1 else 0.5

        # Calculate the estimated magnetic field strength
        base_field = self.base_magnetic_fields.get(planet_type, 0.1)  # Default if unknown type
        magnetic_field_strength = base_field * core_activity_factor

        return magnetic_field_strength

    def estimate_orbital_period(self, distance_au, star_mass_kg):
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

    def estimate_volcanic_activity(self, core_activity, magnetic_field_strength, planet_type, planetary_age, distance_au, nearby_planet_masses=[]):
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
        if core_activity == 0 or planet_type not in ['terrestrial', 'gasGiant']:
            return 0

        if core_activity == 1 or magnetic_field_strength > 25 or tidal_heating:
            return 1

        if core_activity == 1 or (magnetic_field_strength > 10 and planetary_age < 4) or solar_radiation_effect:
            return 0.5

        return 0.25

    def estimate_moons(self, planet_type):
        """
        Estimate the number of moons for a given planet type.

        :param planet_type: Type of the planet.
        :return: Estimated number of moons.
        """
        if planet_type == 'terrestrial':
            # Randomly decide if a terrestrial planet has moons, with a maximum of 2
            num_moons = random.choice([0, 0, 1, 1, 2])  # More chances for 0 or 1 moon

        elif planet_type in ['gasGiant', 'hotJupiter']:
            # Gas giants and hot Jupiters can have a large number of moons
            num_moons = random.randint(0, 80)  # A broad range, reflecting Jupiter/Saturn-like systems

        elif planet_type in ['superEarth', 'neptunian', 'miniNeptune']:
            # These types might have a moderate number of moons
            num_moons = random.randint(0, 10)

        elif planet_type in ['ringedPlanet', 'oceanPlanet', 'venusLike', 'icy', 'marsLike', 'mercuryLike', 'plutoLike', 'ceresLike']:
            # Other types: a small number or no moons, but keeping possibilities open
            num_moons = random.randint(0, 3)

        else:
            # Default case for unknown or unspecified planet types
            num_moons = random.randint(0, 5)  # A conservative range

        return num_moons

    def determine_moon_type(self, planet_type):
        """
        Determine the type of moon based on the planet type.

        :param planet_type: Type of the planet (e.g., 'terrestrial', 'gasGiant', etc.).
        :param planet_moon_probabilities: Dictionary of moon type probabilities for each planet type.
        :return: The determined moon type.
        """
        if planet_type not in self.planet_moon_probabilities:
            return "Unknown moon type"

        moon_types = self.planet_moon_probabilities[planet_type]
        moon_type = random.choices(list(moon_types.keys()), list(moon_types.values()), k=1)[0]
        return moon_type

    def estimate_biomes(self, planet_type, atmospheric_composition, water_presence, geological_activity, temperature_range):
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

        num_biomes = self.base_biomes.get(planet_type, 0)

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

    def estimate_planet_count(self, star_mass, disk_mass, star_age, environmental_factor):
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

    # Planet types
    planet_types = ['terrestrial', 'superEarth', 'mercuryLike', 'marsLike', 'gasGiant', 'hotJupiter', 
                    'neptunian', 'ringedPlanet', 'miniNeptune', 'plutoLike', 'ceresLike', 'oceanPlanet', 'venusLike', 'icy']

    # Planet type/moon probabilities
    planet_moon_probabilities = {
        "terrestrial": {
            "Regular Moon": 0.7,
            "Irregular Moon": 0.2,
            "Captured Moon": 0.1,
            "Large Exomoon": 0.0,
            "Icy Moon": 0.2,
            "Volcanically Active Moon": 0.1,
            "Double Planetary System": 0.0,
            "Hypothetical Habitable Moon": 0.1
        },
        "superEarth": {
            "Regular Moon": 0.6,
            "Irregular Moon": 0.3,
            "Captured Moon": 0.2,
            "Large Exomoon": 0.2,
            "Icy Moon": 0.3,
            "Volcanically Active Moon": 0.2,
            "Double Planetary System": 0.1,
            "Hypothetical Habitable Moon": 0.2
        },
        "mercuryLike": {
            "Regular Moon": 0.1,
            "Irregular Moon": 0.2,
            "Captured Moon": 0.3,
            "Large Exomoon": 0.0,
            "Icy Moon": 0.1,
            "Volcanically Active Moon": 0.0,
            "Double Planetary System": 0.0,
            "Hypothetical Habitable Moon": 0.1
        },
        "marsLike": {
            "Regular Moon": 0.5,
            "Irregular Moon": 0.3,
            "Captured Moon": 0.2,
            "Large Exomoon": 0.0,
            "Icy Moon": 0.2,
            "Volcanically Active Moon": 0.1,
            "Double Planetary System": 0.0,
            "Hypothetical Habitable Moon": 0.1
        },
        "gasGiant": {
            "Regular Moon": 0.4,
            "Irregular Moon": 0.4,
            "Captured Moon": 0.3,
            "Large Exomoon": 0.5,
            "Icy Moon": 0.4,
            "Volcanically Active Moon": 0.3,
            "Double Planetary System": 0.2,
            "Hypothetical Habitable Moon": 0.3
        },
        "hotJupiter": {
            "Regular Moon": 0.2,
            "Irregular Moon": 0.3,
            "Captured Moon": 0.4,
            "Large Exomoon": 0.6,
            "Icy Moon": 0.2,
            "Volcanically Active Moon": 0.1,
            "Double Planetary System": 0.1,
            "Hypothetical Habitable Moon": 0.2
        },
        "neptunian": {
            "Regular Moon": 0.3,
            "Irregular Moon": 0.3,
            "Captured Moon": 0.4,
            "Large Exomoon": 0.2,
            "Icy Moon": 0.5,
            "Volcanically Active Moon": 0.2,
            "Double Planetary System": 0.1,
            "Hypothetical Habitable Moon": 0.3
        },
        "ringedPlanet": {
            "Regular Moon": 0.4,
            "Irregular Moon": 0.4,
            "Captured Moon": 0.3,
            "Large Exomoon": 0.1,
            "Icy Moon": 0.5,
            "Volcanically Active Moon": 0.2,
            "Double Planetary System": 0.2,
            "Hypothetical Habitable Moon": 0.2
        },
        "miniNeptune": {
            "Regular Moon": 0.3,
            "Irregular Moon": 0.3,
            "Captured Moon": 0.2,
            "Large Exomoon": 0.4,
            "Icy Moon": 0.4,
            "Volcanically Active Moon": 0.1,
            "Double Planetary System": 0.1,
            "Hypothetical Habitable Moon": 0.3
        },
        "plutoLike": {
            "Regular Moon": 0.5,
            "Irregular Moon": 0.3,
            "Captured Moon": 0.2,
            "Large Exomoon": 0.0,
            "Icy Moon": 0.4,
            "Volcanically Active Moon": 0.1,
            "Double Planetary System": 0.3,
            "Hypothetical Habitable Moon": 0.2
        },
        "ceresLike": {
            "Regular Moon": 0.2,
            "Irregular Moon": 0.4,
            "Captured Moon": 0.3,
            "Large Exomoon": 0.1,
            "Icy Moon": 0.2,
            "Volcanically Active Moon": 0.0,
            "Double Planetary System": 0.0,
            "Hypothetical Habitable Moon": 0.1
        },
        "oceanPlanet": {
            "Regular Moon": 0.6,
            "Irregular Moon": 0.2,
            "Captured Moon": 0.1,
            "Large Exomoon": 0.3,
            "Icy Moon": 0.5,
            "Volcanically Active Moon": 0.2,
            "Double Planetary System": 0.1,
            "Hypothetical Habitable Moon": 0.4
        },
        "venusLike": {
            "Regular Moon": 0.1,
            "Irregular Moon": 0.3,
            "Captured Moon": 0.4,
            "Large Exomoon": 0.0,
            "Icy Moon": 0.1,
            "Volcanically Active Moon": 0.0,
            "Double Planetary System": 0.0,
            "Hypothetical Habitable Moon": 0.1
        },
        "icy": {
            "Regular Moon": 0.3,
            "Irregular Moon": 0.4,
            "Captured Moon": 0.2,
            "Large Exomoon": 0.2,
            "Icy Moon": 0.6,
            "Volcanically Active Moon": 0.1,
            "Double Planetary System": 0.2,
            "Hypothetical Habitable Moon": 0.3
        }
    }

    active_core_planets = ['terrestrial', 'superEarth', 'marsLike', 'gasGiant', 'hotJupiter', 'neptunian', 'ringedPlanet', 'oceanPlanet']
    inactive_core_planets = ['mercuryLike', 'plutoLike', 'ceresLike', 'icy', 'venusLike', 'miniNeptune']

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


    # Base magnetic field strengths for different planet types (in Gauss)
    base_magnetic_fields = {
        'terrestrial': 30,  # Earth-like
        'superEarth': 45,   # Larger and potentially more active than Earth
        'mercuryLike': 1,   # Mercury-like, weak magnetic field
        'marsLike': 1.5,    # Mars-like, weak magnetic field
        'gasGiant': 10000,  # Jupiter-like
        'hotJupiter': 11000, # Similar to gas giants but potentially stronger due to higher temperatures
        'neptunian': 4000,  # Neptune-like
        'ringedPlanet': 9500, # Similar to gas giants, like Saturn
        'miniNeptune': 3000, # Smaller than Neptune, but with significant magnetic field
        'plutoLike': 0.5,   # Pluto-like, very weak magnetic field
        'ceresLike': 0.1,   # Ceres-like, asteroid with negligible magnetic field
        'oceanPlanet': 35,  # Planets covered by oceans, possibly Earth-like in magnetic field
        'venusLike': 0.005, # Venus-like, extremely weak magnetic field
        'icy': 2            # Ice-covered planets, weak magnetic field
    }