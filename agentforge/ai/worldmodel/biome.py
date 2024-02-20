import math, json, os
from .concept import Concept, ensure_non_negative_and_normalize_row
from .lifeform import Lifeform
from agentforge.ai.worldmodel.evolution import EvolutionarySimulation
import numpy as np

SPECIES_CNT = 35

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
        biome_supported_species = math.ceil(SPECIES_CNT * biome_quotient)
        lifeforms = self.sample_lifeform(biome_type, biome_supported_species, normalized_bx_b_df, normalized_bx_lf_df)

        print("evolving life {} for {} ({})".format(len(lifeforms), planet_info['id'], biome_type))
        origin_of_species = EvolutionarySimulation(
            planet_info['Planet Type'],
            biome_type,
            planet_info['id'],
            normalized_bx_b_df,
            normalized_bx_lf_df
        )
        evolutionary_report = origin_of_species.run(lifeforms, biome_supported_species)

        # Now update the planet/biome with the new life forms
        return evolutionary_report
    
    def sample_lifeform(self, biome_type, biome_supported_species,normalized_bx_b_df, normalized_bx_lf_df):
        lifeforms = []
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
        return lifeforms
    data_dir = os.environ.get("WORLDGEN_DATA_DIR", "./")
    # Biomes + Probabilities for life form subcategories in different biomes
    biomes = json.loads(open(data_dir + "biomes.json").read())
    biome_biology_probabilities = json.loads(open(data_dir + "biology_biome_probabilities.json").read())
    biome_biological_support = json.loads(open(data_dir + "biome_biological_support.json").read())