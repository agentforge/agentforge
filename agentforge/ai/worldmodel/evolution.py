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
    def __init__(self, planet_type, biome_type, uuid="default"):
        # Roll final states
        self.final_evolutionary_stage = self.roll_evolutionary_stage()
        # self.current_milestone = self.roll_technological_milestone(self.final_evolutionary_stage),
        self.total_evolutionary_stages = len(self.evolutionary_probability.keys())
        # Create the ecology, species, and genus models
        self.ecology = SpeciesGenerator(planet_type, uuid)
        self.life = Lifeform()
        self.genus = Genus()
        self.biome_type = biome_type
        self.total_population = 0
        self.dead_mass = 0 # for scavengers and decomposers
        prefix = self.primordial_biome_prefix()
        self.real_biome = prefix + ' ' + biome_type
        self.db = interface_interactor.get_interface("db")

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

    def run(self, lifeforms):
        # Start at unicellular stage
        self.evolutionary_stage_idx = 0
        self.lifeforms = lifeforms

        for i in range(self.total_evolutionary_stages):
            self.evolutionary_stage_idx = i
            self.evolutionary_stage = list(self.evolutionary_probability.keys())[i]
            self.lifeforms = self.init_lifeforms(self.lifeforms)
            self.lifeforms = self.run_simulation(total_epochs=TOTAL_EPOCHS)
            for lifeform in self.lifeforms:
                lifeform.save(self.db, 'species')
            results = self.collect_data()
        return results
    
    def primordial_biome_prefix(self):
        ## First we generate initial species -- primordial single-celled organisms
        if self.biome_type in ["Forest", "Desert", "Ocean", "Tundra", "Grassland", "Wetlands", "Savanna", "Taiga", "Chaparral", "Temperate Deciduous Forest", "Temperate Rainforest", "Mediterranean", "Montane (Alpine)", "Coral Reefs", "Mangroves"]:
            return np.random.choice(['Primordial', 'Alien Primordial', 'Prebiotic'])
        else:
            return 'Alien Primordial'

    def init_lifeforms(self, lifeforms):        
        # Initial lifeform are generated from probability engine
        if self.evolutionary_stage_idx == 0:
            return self.initiate_life(lifeforms)
        else: # Mutate and evolve the next stage of life -- reset population for fairness
            # Always mutate the lifeforms
            self.mutate_lifeforms()
            
            # If we are into technological evolution skip huge evolutionary changes
            # The timescales are moving beyond that of biological evolution
            if self.evolutionary_stage_idx >= 3:
                return lifeforms
            
            # With some probability we need to generate new lifeforms
            for lifeform in lifeforms:
                # Get existing information to create evolution chain
                if "Name" in lifeform.species_data and "Description" in lifeform.species_data:
                    previous_lifeform = "{} ({}) {}".format(lifeform.species_data["Name"], lifeform.genus, lifeform.species_data["Description"])
                else:
                    previous_lifeform = ""

                lifeform.genus = self.genus.get_genus(lifeform.species_data["Biological Type"], self.evolutionary_stage)
                generative_data = self.ecology.generate(
                    self.real_biome,
                    self.evolutionary_stage,
                    lifeform.genus,
                    lifeform.role,
                    lifeform.behavioral_role,
                    previous_species=previous_lifeform
                )
                lifeform.species_data.update(generative_data)
                # TODO: SELECT ROLES WITH PROBABILISTIC MATRIX
        return lifeforms

    # From the primordial goo emerges initial life
    def initiate_life(self, lifeforms):
        logger.info("Creating {} initial lifeforms".format(len(lifeforms)))
        self.lifeforms = lifeforms
        species = []

        for lifeform in self.lifeforms:
            ### TODO: Better way to generate intial population
            new_species = Species(lifeform, self.evolutionary_stage_idx)

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
            logger.info("initial_population {}".format(new_species.population))
            logger.info("sample mass {}".format(new_species.individuals[0][2]['Mass']))
            species.append(new_species)
        return species

    def mutate_lifeforms(self):
        # Apply genetic mutations to lifeforms
        for lifeform in self.lifeforms:
            for individual in lifeform.individuals:
                individual[0] = lifeform.mutate(individual[0])

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

        dead_pool = []

        # Iterate through lifeforms and individuals in randomized order
        hunt_report = HuntReport()
        to_remove = defaultdict(set)
        for lifeform_index, individual_index in index_pairs:
            # Access the lifeform and individual
            lifeform = self.lifeforms[lifeform_index]
            individual = lifeform.individuals[individual_index]
            hunger_loss = HUNGER_LOSS  * individual[2]['Mass']  * individual[2]['Resource Utilization'] / 100.0
            # Simulate food chain dynamics
            if lifeform.role == "Producers":
                self.environment = lifeform.autotropic_growth(individual, self.environment)
            elif lifeform.role in ["Primary Consumers", "Secondary Consumers", "Tertiary Consumers", "Omnivores"]:
                if individual[1] >= SATIATED_LEVEL: #satiated
                    continue
                possible_prey = lifeform.identify_food(self.lifeforms)
                if len(possible_prey) == 0:
                    hunt_report.add_no_prey_at_all(lifeform.role)
                    individual[1] -= hunger_loss
                    continue
                chosen_prey = lifeform.roll_for_prey_location(individual, possible_prey, self.total_population)
                if chosen_prey is None:
                    hunt_report.add_no_prey(lifeform.role)
                    individual[1] -= hunger_loss
                    continue
                prey_ind, prey_idx = chosen_prey.get_weak_individuals()
                if prey_ind is None:
                    hunt_report.add_fail(lifeform.role)
                    individual[1] -= hunger_loss
                    continue
                success = lifeform.roll_for_consumption(individual, prey_ind)
                if not success:
                    hunt_report.add_fail_roll(lifeform.role)
                    individual[1] -= hunger_loss
                    continue
                hunt_report.add_success(lifeform.role)
                dead_mass = lifeform.consume(individual, chosen_prey, prey_ind)

                if chosen_prey.role != "Producers": # Producers don't die, they just lose health
                    to_remove[chosen_prey].add(prey_idx)
                else:
                    regen = (1- chosen_prey.individuals[prey_idx][2]['Regeneration'] / 100.0)
                    chosen_prey.individuals[prey_idx][1] -= HUNGER_LOSS * chosen_prey.individuals[prey_idx][2]['Mass'] * regen
                    if chosen_prey.individuals[prey_idx][1] <= 0:
                        chosen_prey.individuals[prey_idx][1] = 0
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

        logger.info("Consumption Report")    
        logger.info(hunt_report)

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
            logger.info("dead world...")
            return False

        # continue evolving
        return True

    def run_simulation(self, total_epochs):
        # Run the simulation for the specified number of epochs
        self.total_epochs = total_epochs
        for _ in range(total_epochs):
            logger.info("Epoch: {}".format(self.current_epoch))
            living_world = self.run_epoch()
            for i in self.lifeforms:
                if i.population:
                    logger.info(i.analyze_health_statistics())
            logger.info(self.environment)
            if not living_world:
                return []
        return self.lifeforms
    
    # Identify the species that achieves supremacy in the ecosystem
    def identify_apex_species(self):
            apex_species = None
            highest_score = -1  # Initialize with a value that will be lower than any possible score

            for species in self.lifeforms:
                genus, biological_type, role, average_health, max_health, min_health, population = species.analyze_health_statistics()
                
                # Define a scoring mechanism for identifying the apex species
                # This example simply multiplies average health by population for a basic score
                species_score = average_health * population

                if species_score > highest_score:
                    highest_score = species_score
                    apex_species = species

            if apex_species:
                print(f"Apex Species: {apex_species.genus}, {apex_species.species_data['Biological Type']}, {apex_species.role}")
                print(f"Average Health: {average_health}, Max Health: {max_health}, Min Health: {min_health}, Population: {population}")
                return apex_species
            else:
                print("No apex species identified.")
                return None

    def collect_data(self):
        # Collect and return data from the simulation
        return {
            "lifeforms": self.lifeforms,
            "environment": self.environment,
            "current_epoch": self.current_epoch,
            "final_evolutionary_stage": self.final_evolutionary_stage,
            "apex_species": self.identify_apex_species()
        }
        
    def roll_evolutionary_stage(self):
        # Iterate through each key and value
        highestStage = None
        for stage, probability in self.evolutionary_probability.items():
            # Roll based on each probability
            if np.random.rand() < probability:
                # Return the key (stage) that is true with the lowest probability
                highestStage = stage
        if highestStage is None:
            return "No evolutionary stage reached"
        return highestStage
    
    # Biological complexity path
    evolutionary_probability = {
        'Single-celled organisms': 0.95,
        'Multi-celled organisms': 0.80,
        'Complex lifeforms': 0.75,
    }
