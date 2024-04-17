import pandas as pd
import numpy as np
from agentforge.ai.worldmodel.concept import Concept, normalize_rows
from agentforge.ai.worldmodel.lifeform import Lifeform
from agentforge.ai.worldmodel.star import Star
from agentforge.ai.worldmodel.planet import Planet
from agentforge.ai.worldmodel.biome import Biome

class UniverseProbability:
  def __init__(self) -> None:
    self.star = Star()
    self.planet = Planet()
    self.biome = Biome()
    self.lifeform = Lifeform()
    self.galaxy_concepts = {"Milky Way": Concept("Milky Way", "Galaxy")}
    self.galaxy_names = list(self.galaxy_concepts.keys())
    self.star_names = list(self.star.star_concepts.keys())
    self.planet_names = list(self.planet.planet_concepts.keys())
    self.biome_names = list(self.biome.biome_concepts.keys())

  def setup(self):
    # Add connections to the Milky Way galaxy
    for star_type, probability in self.star.star_probabilities.items():
        self.galaxy_concepts["Milky Way"].add_connection(self.star.star_concepts[star_type], probability)
    
    # Add connections to each Star Type
    self.star.create_connections_for_star(self.planet)

    # Initialize DataFrames with float dtype
    self.gx_s_df = pd.DataFrame(0.0, index=self.galaxy_names, columns=self.star_names)
    self.sx_p_df = pd.DataFrame(0.0, index=self.star_names, columns=self.planet_names)
    self.px_b_df = pd.DataFrame(0.0, index=self.planet_names, columns=self.biome_names)
    self.bx_b_df = pd.DataFrame(0.0, index=self.biome_names, columns=self.lifeform.life_form_categories)

    # Step 1: Create GxS DataFrame -- Galaxy to Star
    for galaxy in self.galaxy_names:
        for connection in self.galaxy_concepts[galaxy].get_connections():
            self.gx_s_df.at[galaxy, connection['concept'].name] = connection['probability']

    # Step 2: Create SxP DataFrame -- Star to planet
    for star in self.star_names:
        for connection in self.star.star_concepts[star].get_connections():
            self.sx_p_df.at[star, connection['concept'].name] = connection['probability']

    # Create the PxB DataFrame -- Planet to Biome
    for planet in self.planet_names:
        for biome, probability in self.planet.planet_biome_connections.get(planet, {}).items():
            if biome in self.biome_names:
                self.px_b_df.at[planet, biome] = probability

    # Initialize the Biome x Biology DataFrame
    for biome in self.biome_names:
        for subcategory, probability in self.biome.biome_biology_probabilities.get(biome, {}).items():
            if subcategory in self.lifeform.life_form_categories:
                self.bx_b_df.at[biome, subcategory] = probability

    # Create the biological matrix with row normalization
    biological_matrix_row_norm = self.lifeform.create_biological_matrix_row_normalization()

    # Initialize the Biology x Individual Characteristics DataFrame
    self.biology_x_individual_df = pd.DataFrame(0.0, index=biological_matrix_row_norm.index, columns=self.lifeform.life_form_characteristic_names)

    # Populate the DataFrame with normalized values
    for biology_type in biological_matrix_row_norm.index:
        for characteristic in self.lifeform.life_form_characteristic_names:
            self.biology_x_individual_df.at[biology_type, characteristic] = biological_matrix_row_norm.at[biology_type, characteristic]

    # Normalize rows of GxS, SxP, PxB, and BxBio DataFrames
    self.normalized_gx_s_df = normalize_rows(self.gx_s_df)
    self.normalized_sx_p_df = normalize_rows(self.sx_p_df)
    self.normalized_px_b_df = normalize_rows(self.px_b_df)
    self.normalized_bx_b_df = normalize_rows(self.bx_b_df)
    self.normalized_bx_lf_df = normalize_rows(self.biology_x_individual_df)

    # Multiply normalized GxS, SxP, PxB, and BxBio DataFrames to get GxBio DataFrame
    self.gx_p_df = self.normalized_gx_s_df.dot(self.normalized_sx_p_df)
    self.gx_b_df = self.gx_p_df.dot(self.normalized_px_b_df)
    self.gx_bb_df = self.gx_b_df.dot(self.normalized_bx_b_df)
    self.gx_bl_df = self.gx_bb_df.dot(self.normalized_bx_lf_df)

    return {
        "gx_s_df": self.gx_s_df,
        "sx_p_df": self.sx_p_df,
        "px_b_df": self.px_b_df,
        "bx_b_df": self.bx_b_df,
        "biology_x_individual_df": self.biology_x_individual_df,
        "normalized_gx_s_df": self.normalized_gx_s_df,
        "normalized_sx_p_df": self.normalized_sx_p_df,
        "normalized_px_b_df": self.normalized_px_b_df,
        "normalized_bx_b_df": self.normalized_bx_b_df,
        "normalized_bx_lf_df": self.normalized_bx_lf_df,
        "gx_p_df": self.gx_p_df,
        "gx_b_df": self.gx_b_df,
        "gx_bb_df": self.gx_bb_df,
        "gx_bl_df": self.gx_bl_df
    }
