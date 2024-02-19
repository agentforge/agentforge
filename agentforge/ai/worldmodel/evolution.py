import random
from agentforge.ai.worldmodel.lifeform import Lifeform
from agentforge.ai.worldmodel.generator import SpeciesGenerator
import numpy as np
from collections import defaultdict
from agentforge.utils import logger
from agentforge.ai.worldmodel.species import Species
from agentforge.ai.worldmodel.predator import HuntReport
from agentforge.ai.worldmodel.genus import Genus
from agentforge.ai.worldmodel.environment import Environment
from agentforge.interfaces import interface_interactor
from tqdm import tqdm
from copy import deepcopy
import uuid

""" Evolution baby! A Genetic Algorithm for simulating evolution of lifeforms on a planet"""

INITIAL_POPULATION = 100
TOTAL_EPOCHS = 50
HUNGER_LOSS = 0.025
SATIATED_LEVEL = 90
TOTAL_NUTRIENTS = 100.0
NUTRIENT_REFRESH_RATE = 0.1
MAX_POPULATION = 5000
NUM_GROUPS_AT_START = 5

class EvolutionarySimulation:
    def __init__(self, planet_type, biome_type, planet_id="default", normalized_bx_b_df=[], normalized_bx_lf_df=[]):
        # Roll final states
        self.final_evolutionary_stage = self.roll_evolutionary_stage()
        self.total_evolutionary_stages = list(self.evolutionary_probability.keys())[0:self.final_evolutionary_stage+1]
        # Create the ecology, species, and genus models
        self.ecology = SpeciesGenerator(planet_type, planet_id)
        self.life = Lifeform()
        self.genus = Genus()
        self.biome_type = biome_type
        self.total_population = 0
        self.dead_mass = 0 # for scavengers and decomposers
        self.evolutionary_stage_idx = 0
        self.real_biome = self.get_biome()
        self.db = interface_interactor.get_interface("db")
        self.planet_id = planet_id
        self.normalized_bx_b_df = normalized_bx_b_df
        self.normalized_bx_lf_df = normalized_bx_lf_df

        # Define initial conditions
        self.lifeforms = []  # List to store lifeform objects
        self.environment = Environment(TOTAL_NUTRIENTS)
        self.current_epoch = 0
        self.total_epochs = 0 # point at which to evolve to next stage

        # Genetic Algorithm Parameters
        self.selection_criteria = {}  # Criteria for natural selection
        self.reproduction_rate = 0.1

        # Timescales
        self.epoch_duration = 100  # Example duration in arbitrary units

    def run(self, lifeforms, biome_supported_species=10, total_epochs=TOTAL_EPOCHS):
        # Start at unicellular stage
        self.lifeforms = lifeforms
        for i, stage in enumerate(self.total_evolutionary_stages):
            print("STAGE: ", i, " ", list(self.evolutionary_probability.keys())[i])
            self.evolutionary_stage_idx = i
            self.evolutionary_stage = stage
            self.lifeforms = self.init_lifeforms(self.lifeforms, biome_supported_species)
            self.lifeforms = self.run_simulation(total_epochs=total_epochs)
            for i in tqdm(range(len(self.lifeforms)), desc="Saving species"):
                self.lifeforms[i].save(self.db, 'species')
        print("Evolution complete!")
        results = self.collect_data()
        return results
    
    def get_biome(self):
        if self.evolutionary_stage_idx == 0:
            prefix = self.primordial_biome_prefix()
            return prefix + ' ' + self.biome_type
        else:
            return self.biome_type
    
    def primordial_biome_prefix(self):
        ## First we generate initial species -- primordial single-celled organisms
        if self.biome_type in ["Forest", "Desert", "Ocean", "Tundra", "Grassland", "Wetlands", "Savanna", "Taiga", "Chaparral", "Temperate Deciduous Forest", "Temperate Rainforest", "Mediterranean", "Montane (Alpine)", "Coral Reefs", "Mangroves"]:
            return np.random.choice(['Primordial', 'Alien Primordial', 'Prebiotic'])
        else:
            return 'Alien Primordial'

    def init_lifeforms(self, lifeforms, biome_supported_species):        
        # Initial lifeform are generated from probability engine
        if self.evolutionary_stage_idx == 0:
            return self.initiate_life(lifeforms)
        else:
            # If we are into technological evolution skip huge evolutionary changes
            # The timescales are moving beyond that of biological evolution
            if self.evolutionary_stage_idx > self.final_evolutionary_stage:
                return lifeforms
            
            # Always mutate the lifeforms
            self.mutate_lifeforms()

            # With some probability we need to generate new lifeforms
            new_lifeforms = []
            species_probabilities = []
            new_species_required = max(biome_supported_species + np.random.randint(-3,3) + np.random.randint(0,3) * self.evolutionary_stage_idx - len(lifeforms), 0)
            if new_species_required > 0:
                for surviving_species in lifeforms:
                    species_probabilities.append(surviving_species.population)
                species_probabilities = np.array(species_probabilities)
                ### Edge case where all species are extinct
                if len(species_probabilities) == 0:
                    lifeforms = self.sample_lifeform(self.biome_type, biome_supported_species, self.normalized_bx_b_df, self.normalized_bx_lf_df)
                else:
                    next_species = np.random.choice(lifeforms, new_species_required, p=species_probabilities / species_probabilities.sum(), replace=True)
                    lifeforms.extend(next_species)
            for lifeform in lifeforms:
                new_lifeform = deepcopy(lifeform)
                ev_idx = self.roll_evolutionary_stage()
                next_evolutionary_stage = list(self.evolutionary_probability.keys())[ev_idx]
                new_lifeform.genus = self.genus.get_genus(lifeform.species_data["Biological Type"], next_evolutionary_stage)
                new_lifeform.ancestor = lifeform.uuid
                new_lifeform.uuid = str(uuid.uuid4())
                new_lifeform.biome = self.get_biome()
                new_lifeform.evolutionary_stage = ev_idx
                new_lifeform.population = 100
                new_lifeforms.append(new_lifeform)
                # TODO: SELECT NEW ROLES WITH PROBABILISTIC MATRIX

                # TODO: MOVE GENERATIVE CODE TO SPECIES CLASS and SIM
                if "Name" in lifeform.species_data and "Description" in lifeform.species_data:
                    previous_lifeform = "{} ({}) {}".format(lifeform.species_data["Name"], lifeform.genus, lifeform.species_data["Description"])
                else:
                    previous_lifeform = ""
                # generative_data = self.ecology.generate(
                #     self.real_biome,
                #     self.evolutionary_stage,
                #     lifeform.genus,
                #     lifeform.role,
                #     lifeform.behavioral_role,
                #     previous_species=previous_lifeform
                # )
                # lifeform.species_data.update(generative_data)
        return new_lifeforms

    # From the primordial goo emerges initial life
    def initiate_life(self, lifeforms):
        # logger.info("Creating {} initial lifeforms".format(len(lifeforms)))
        self.lifeforms = lifeforms
        species = []

        for lifeform in self.lifeforms:
            ### TODO: Better way to generate intial population
            new_species = Species(lifeform, self.evolutionary_stage_idx, planet_id=self.planet_id, biome=self.get_biome())

            # Determine new species role depending on environment and evolutionary stage
            if 'Flora' in lifeform['Biological Type']:
                new_species.role = 'Producers'
            else:
                new_species.role = new_species.choose_role(self.evolutionary_stage_idx, new_species.consumption_roles, species)
            new_species.genus = self.genus.get_genus(new_species.species_data["Biological Type"], self.evolutionary_stage)
            new_species.behavioral_role = new_species.choose_role(self.evolutionary_stage_idx, new_species.behavioral_roles, species)

            # generative_data = self.ecology.generate(
            #     self.real_biome,
            #     self.evolutionary_stage,
            #     new_species.genus,
            #     new_species.role,
            #     new_species.behavioral_role,
            #     attributes=new_species.species_data["Life Form Attributes"],
            # )
            # lifeform.update(generative_data)
            # logger.info("generated species {}".format(generative_data))

            new_species.population = int(INITIAL_POPULATION * new_species.consumption_pop_modifiers[new_species.role])
            self.total_population += new_species.population
            new_species.generate_population()
            # logger.info("initial_population {}".format(new_species.population))
            # logger.info("sample mass {}".format(new_species.individuals[0][2]['Mass']))
            species.append(new_species)
        return species

    def mutate_lifeforms(self):
        # Apply genetic mutations to lifeforms
        for lifeform in self.lifeforms:
            for individual in lifeform.individuals:
                individual['genes'] = lifeform.mutate(individual['genes'])

    def environmental_interaction(self):
        # Simulate environmental interaction with lifeforms
        for lifeform in self.lifeforms:
            lifeform = self.environment.interact(lifeform)

    def predation_consumption_loop(self):
        # Generate a list of (lifeform_index, individual_index) pairs
        index_pairs = []
        for lifeform_index, lifeform in enumerate(self.lifeforms):
            for individual_index in range(len(lifeform.individuals)):
                index_pairs.append((lifeform_index, individual_index))

        # Randomize the order of index pairs
        random.shuffle(index_pairs)

        # Iterate through lifeforms and individuals in randomized order
        hunt_report = HuntReport()
        to_remove = defaultdict(set)
        for lifeform_index, individual_index in index_pairs:
            # Access the lifeform and individual
            lifeform = self.lifeforms[lifeform_index]
            individual = lifeform.individuals[individual_index]
            ind_genetics = lifeform.decode_genetics(individual['genes'], lifeform.genetic_base_line())
            hunger_loss = HUNGER_LOSS * ind_genetics['Mass']  * ind_genetics['Resource Utilization'] / 100.0
            # Simulate food chain dynamics
            if lifeform.role == "Producers":
                self.environment = lifeform.autotropic_growth(individual, self.environment)
            elif lifeform.role in ["Primary Consumers", "Secondary Consumers", "Tertiary Consumers", "Omnivores"]:
                if individual['health'] >= SATIATED_LEVEL: #satiated
                    continue
                possible_prey = lifeform.identify_food(self.lifeforms)
                if len(possible_prey) == 0:
                    hunt_report.add_no_prey_at_all(lifeform.role)
                    individual['health'] -= hunger_loss
                    continue
                chosen_prey = lifeform.roll_for_prey_location(individual, possible_prey, self.total_population)
                if chosen_prey is None:
                    hunt_report.add_no_prey(lifeform.role)
                    individual['health'] -= hunger_loss
                    continue
                prey_ind, prey_idx = chosen_prey.get_weak_individuals()
                if prey_ind is None:
                    hunt_report.add_fail(lifeform.role)
                    individual['health'] -= hunger_loss
                    continue
                success = lifeform.roll_for_consumption(individual, prey_ind, chosen_prey)
                if not success:
                    hunt_report.add_fail_roll(lifeform.role)
                    individual['health'] -= hunger_loss
                    continue
                hunt_report.add_success(lifeform.role)
                dead_mass = lifeform.consume(individual, chosen_prey, prey_ind)

                if chosen_prey.role != "Producers": # Producers don't die, they just lose health
                    to_remove[chosen_prey].add(prey_idx)
                else:
                    prey_genetics = chosen_prey.decode_genetics(prey_ind['genes'], chosen_prey.genetic_base_line())
                    regen = (1- prey_genetics['Regeneration'] / 100.0)
                    chosen_prey.individuals[prey_idx]['health'] -= HUNGER_LOSS * prey_genetics['Mass'] * regen
                    if chosen_prey.individuals[prey_idx]['health'] <= 0:
                        chosen_prey.individuals[prey_idx]['health'] = 0
                        chosen_prey.population -= 1
                        to_remove[chosen_prey].add(prey_idx)

                self.dead_mass = dead_mass

            # Scavengers and Decomposers benefit from dead organisms
            elif lifeform.role in ["Scavengers", "Decomposers", "Detritivores"]:
                lifeform.consume_decomposing_matter()

            # Pollinators interact with plants
            elif lifeform.role == "Pollinators":
                lifeform.pollinate()

            # Parasites and Parasitoids impact hosts
            elif lifeform.role in ["Parasites", "Parasitoids"]:
                lifeform.parasitic_interaction()
            
            lifeform.individuals[individual_index] = individual

        # Remove dead individuals from the population
        for prey_lifeform, prey_set in to_remove.items():
            sorted_indices = sorted(prey_set, reverse=True)
            # Remove items from the original list using the sorted indices
            for index in sorted_indices:
                if 0 <= index < len(prey_lifeform.individuals):
                    del prey_lifeform.individuals[index]

        # logger.info("Consumption Report")    
        # logger.info(hunt_report)

    ### TODO: Implement natural events (floods, droughts, meteor impacts etc.)
    def natural_events(self):
        pass

    # Death comes for us all
    def natural_selection(self):
        suriviving_lifeforms = []
        for lifeform in self.lifeforms:
            if lifeform.population <= 0:
                continue
            lifeform.decrease_population_based_on_health()
            if lifeform.population > 0:
                suriviving_lifeforms.append(lifeform)
        self.lifeforms = suriviving_lifeforms

    def reproduce_lifeforms(self):
        for lifeform in self.lifeforms:
            # logger.info("reproducing {}! {}".format(lifeform.role, lifeform.population))
            if lifeform.population <= 0:
                continue
            if lifeform.population > MAX_POPULATION * lifeform.consumption_pop_modifiers[lifeform.role]:
                lifeform.reproduce(replace=True)
                continue
            lifeform.reproduce()
            # logger.info("after reproducing {}! {}".format(lifeform.role, lifeform.population))

    def update_environment(self):
        # Simulate environmental changes -- refresh resources
        self.environment.set('Water', min(TOTAL_NUTRIENTS, self.environment.get('Water') + (TOTAL_NUTRIENTS * NUTRIENT_REFRESH_RATE)))
        self.environment.set('Sunlight', TOTAL_NUTRIENTS) # Sunlight always hits max each turn, limit represents canopy)
        self.environment.set('Nutrients', min(TOTAL_NUTRIENTS, self.environment.get('Nutrients') + (TOTAL_NUTRIENTS * NUTRIENT_REFRESH_RATE)))

        self.total_population = 0
        for lifeform in self.lifeforms:
            self.total_population += lifeform.population

    def run_epoch(self):
        # Run a single epoch
        self.environmental_interaction()
        self.predation_consumption_loop()
        self.natural_events()
        self.mutate_lifeforms()
        self.natural_selection()
        self.reproduce_lifeforms()
        self.update_environment()
        self.current_epoch += 1

        # Don't continue evolving a dead world
        cont = False
        for lifeform in self.lifeforms:
            if lifeform.population > 0:
                cont = True
        if not cont:
            # logger.info("dead world...")
            return False

        # continue evolving
        return True

    def run_simulation(self, total_epochs):
        # Run the simulation for the specified number of epochs
        self.total_epochs = total_epochs
        for _ in tqdm(range(total_epochs), desc="Evolutionary Progress"):
            living_world = self.run_epoch()
            if not living_world:
                return []
        return self.lifeforms
    
    # Identify the species that achieves supremacy in the ecosystem
    @classmethod
    def identify_apex_species(cls, lifeforms):
            apex_species = None
            highest_score = -1  # Initialize with a value that will be lower than any possible score
            for species in lifeforms:
                if species.has_predator(lifeforms):
                    continue
                else:
                    average_health, max_health, min_health = species.analyze_health_statistics()

                    # Define a scoring mechanism for identifying the apex species
                    # This example simply multiplies average health by population for a basic score
                    species_health = min(average_health, 100.0) * species.population
                    species_genetics = 0.0
                    for trait in cls.apex_species_traits:
                        if trait in species.species_data['Genetic Profile']:
                            species_genetics += species.species_data['Genetic Profile'][trait]
                    species_score = ((species_health * 0.2) + (species_genetics * 0.8)) * species.evolutionary_stage
                    if species.species_data['Biological Type'] == "Flora" or species.species_data['Biological Type'] == "Aquatic":
                        species_score *= 0.5

                    if species_score > highest_score:
                        highest_score = species_score
                        apex_species = species

            if apex_species:
                print(f"Apex Species: {apex_species.genus}, {apex_species.species_data['Biological Type']}, {apex_species.role}")
                print(f"Average Health: {average_health}, Max Health: {max_health}, Min Health: {min_health}, Population: {apex_species.population}")
                return apex_species, highest_score
            else:
                print("No apex species identified.")
                return None, 0.0

    def collect_data(self):
        # Collect and return data from the simulation
        apex, species_score = EvolutionarySimulation.identify_apex_species(self.lifeforms)
        apex_id = None
        if apex:
            apex_id = apex.uuid
        return {
            "lifeforms": self.lifeforms,
            "environment": self.environment,
            "current_epoch": self.current_epoch,
            "final_evolutionary_stage": self.final_evolutionary_stage,
            "apex_species": apex_id,
            "apex_species_score": species_score,

        }

    def roll_evolutionary_stage(self):
        # Iterate through each key and value
        highestStage = None
        lowestProbability = 100
        idx = 0
        for _, probability in self.evolutionary_probability.items():
            # Roll based on each probability
            if np.random.rand() < probability and probability < lowestProbability:
                # Return the key (stage) that is true with the lowest probability
                highestStage = idx
                lowestProbability = probability
            idx += 1
        if highestStage is None:
            return 0
        return highestStage
    
    # Biological complexity path
    evolutionary_probability = {
        'Single-celled organisms': 0.95,
        'Multi-celled organisms': 0.80,
        'Complex lifeforms': 0.75,
    }

    apex_species_traits = [
        "Intelligence",  # Cognitive
        "Wisdom",        # Cognitive
        "Perception",    # Cognitive
        "Mental Fortitude",  # Cognitive
        "Dexterity",     # Physical
        "Endurance",     # Physical
        "Physical Fortitude",  # Physical
        "Social Cooperation",  # Social
        "Adaptability",  # Social
        "Navigation Skills",  # Integrative
        "Immune System Strength"  # Integrative
    ]