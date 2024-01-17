import numpy as np
import pandas as pd
import math, time
from agentforge.ai.worldmodel.star import Star
from agentforge.ai.worldmodel.planet import Planet
from agentforge.ai.worldmodel.lifeform import Lifeform
from agentforge.ai.worldmodel.concept import Concept, normalize_rows, ensure_non_negative_and_normalize_row
from agentforge.ai.worldmodel.biome import Biome
from agentforge.ai.worldmodel.moon import Moon

class Galaxy:

    def __init__(self, metadata=None):
        self.metadata = metadata if metadata is not None else {}
        self.star = Star()
        self.planet = Planet()
        self.lifeform = Lifeform()
        self.biome = Biome()
        self.moon = Moon()

    async def generate(self):
        # From the macro to the micro, we build the world model
        self.systems = []
        self.has_life = []

        self.galaxy_concepts = {"Milky Way": Concept("Milky Way", "Galaxy")}
        galaxy_names = list(self.galaxy_concepts.keys())
        star_names = list(self.star.star_concepts.keys())
        planet_names = list(self.planet.planet_concepts.keys())
        biome_names = list(set(b for biomes in self.planet.planet_biome_connections.values() for b in biomes))

        for star_type, probability in self.star.star_probabilities.items():
            self.galaxy_concepts["Milky Way"].add_connection(self.star.star_concepts[star_type], probability)

        self.star.create_connections_for_star(self.planet)

        # Initialize DataFrames with float dtype
        gx_s_df = pd.DataFrame(0.0, index=galaxy_names, columns=star_names)
        sx_p_df = pd.DataFrame(0.0, index=star_names, columns=planet_names)
        px_b_df = pd.DataFrame(0.0, index=planet_names, columns=biome_names)
        bx_b_df = pd.DataFrame(0.0, index=biome_names, columns=self.lifeform.life_form_categories)

        # Step 1: Create GxS DataFrame
        gx_s_df = pd.DataFrame(0.0, index=galaxy_names, columns=star_names)
        for galaxy in galaxy_names:
            for connection in self.galaxy_concepts[galaxy].get_connections():
                gx_s_df.at[galaxy, connection['concept'].name] = connection['probability']

        # Step 2: Create SxP DataFrame
        sx_p_df = pd.DataFrame(0.0, index=star_names, columns=planet_names)
        for star in star_names:
            for connection in self.star.star_concepts[star].get_connections():
                sx_p_df.at[star, connection['concept'].name] = connection['probability']

        # Create the PxB DataFrame
        px_b_df = pd.DataFrame(0.0, index=planet_names, columns=biome_names)
        for planet in planet_names:
            for biome, probability in self.planet.planet_biome_connections.get(planet, {}).items():
                if biome in biome_names:
                    px_b_df.at[planet, biome] = probability

        # Initialize the Biome x Biology DataFrame
        bx_b_df = pd.DataFrame(0.0, index=biome_names, columns=self.lifeform.life_form_categories)

        # Populate the DataFrame with probabilities
        for biome in biome_names:
            for subcategory, probability in self.biome.biome_biology_probabilities.get(biome, {}).items():
                if subcategory in self.lifeform.life_form_categories:
                    bx_b_df.at[biome, subcategory] = probability

        # Create the biological matrix with row normalization
        biological_matrix_row_norm = self.lifeform.create_biological_matrix_row_normalization()

        # Initialize the Biology x Individual Characteristics DataFrame
        biology_x_individual_df = pd.DataFrame(0.0, index=biological_matrix_row_norm.index, columns=self.lifeform.life_form_characteristic_names)

        # Populate the DataFrame with normalized values
        for biology_type in biological_matrix_row_norm.index:
            for characteristic in self.lifeform.life_form_characteristic_names:
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
        for x in range(610):
            # Sample a star type based on galaxy
            star_probabilities = normalized_gx_s_df.iloc[0]
            star_type = np.random.choice(star_names, p=star_probabilities)

            # Find the index of the sampled star type
            star_index = star_names.index(star_type)

            # Create star specific information
            star_mass_range = self.star.star_concepts[star_type].metadata['mass_range_kg']
            star_mass_kg = np.random.uniform(star_mass_range[0], star_mass_range[1])

            star_age_range = self.star.star_concepts[star_type].metadata['age_range_Gyr']
            star_age_Gyr = np.random.uniform(star_age_range[0], star_age_range[1])

            disk_mass_range = self.star.star_concepts[star_type].metadata['disk_mass_percentage_of_solar_mass']
            disk_mass = np.random.uniform(disk_mass_range[0], disk_mass_range[1])

            # Estimate number of planets
            num_planets = self.planet.estimate_planet_count(star_mass_kg, disk_mass, star_age_Gyr, 1.0)

            solar_system_info = {
                "Star": star_type,
                "Star Information": self.star.star_concepts[star_type].metadata,
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
                planet_info, estimated_biomes, life_presence = self.planet.generate(planet_type, star_mass_kg, star_type)

                for n in range(estimated_biomes):
                    biome_type = np.random.choice(biome_names, p=normalized_px_b_df.iloc[planet_index])

                    biome_index = biome_names.index(biome_type)
                    
                    lifeforms = []
                    
                    if life_presence:
                        biological_probabilities = normalized_bx_b_df.iloc[biome_index]
                        biological_type = np.random.choice(self.lifeform.life_form_categories, p=biological_probabilities)

                        biological_index = self.lifeform.life_form_categories.index(biological_type)

                        life_form_characteristic_probabilities = normalized_bx_lf_df.iloc[biological_index]
                        adjusted_probabilities = ensure_non_negative_and_normalize_row(life_form_characteristic_probabilities)
                        life_form_characteristic_list = list(set(np.random.choice(self.lifeform.life_form_characteristic_names, p=adjusted_probabilities, size=5)))

                        bio_info = {
                            "Biological": biological_type,
                            "Biological Characteristics": self.lifeform.biologic_concepts[biological_type].metadata,
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

            self.systems.append(solar_system_info)

            if life_presence:
                # print(f"Life exists on this planet! after {x} iterations")
                # pretty_json = json.dumps(solar_system_info, indent=4)
                # print(pretty_json)

                self.has_life.append(solar_system_info)
                
                # Calculate overall probability
                # probability = calculate_life_probability(
                #     distance_to_star=estimated_au,  # in AU
                #     star_class=star_type,         # stable star
                #     atmospheric_composition=estimated_atmosphere_thickness,  # suitable atmosphere
                #     magnetic_field_strength=magnetic_field,  # in Gauss
                #     geological_activity=core_activity,       # active geology
                #     chemical_composition=check_essential_chemicals_for_life(atmosphere_composition),
                #     water_presence=water_presence,            # liquid water present
                #     orbital_stability=1,         # stable orbit
                #     moon_presence=1,             # moon present
                #     radiation_level=3,           # radiation level in Sieverts
                #     debug=True
                # )
                # break
        # print("we found life")
        # pretty_json = json.dumps(self.has_life, indent=4)
        # print(pretty_json)
        # print(len(self.has_life))
        # def find_invalid_floats(data, path=""):
        #     if isinstance(data, float):
        #         if math.isnan(data) or math.isinf(data):
        #             print(f"Invalid float at {path}: {data}")
        #             return True
        #     elif isinstance(data, dict):
        #         for key, value in data.items():
        #             find_invalid_floats(value, path + f".{key}")
        #     elif isinstance(data, list):
        #         for i, value in enumerate(data):
        #             find_invalid_floats(value, path + f"[{i}]")
        # invalid = find_invalid_floats(self.systems)
        # if invalid:
        #     print("Invalid floats found in systems")
        # # return {}
        return {"systems": self.systems, "has_life": self.has_life}
