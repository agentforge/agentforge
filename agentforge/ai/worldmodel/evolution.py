import random
from agentforge.ai.worldmodel.lifeform import Lifeform
from agentforge.ai.worldmodel.generator import SpeciesGenerator
import numpy as np
from collections import defaultdict
from agentforge.utils import logger
from agentforge.ai.worldmodel.species import Species
from agentforge.ai.worldmodel.predator import HuntReport
from agentforge.ai.worldmodel.genus import Genus

""" Evolution baby! A Genetic Algorithm for simulating evolution of lifeforms on a planet"""

HEALTH_CONSUMPTION_FACTOR = 0.1
MIN_DEATH_RATE = 0.01  # 5% minimal death rate
REPRODUCTION_MODIFIER = 0.1  # 1.0 is default
INITIAL_POPULATION = 100
MUTATION_RATE = 0.05
PLANT_GROWTH_FACTOR = 0.30
TOTAL_EPOCHS = 50
TOTAL_EVOLUTIONARY_STAGES = 3
HUNGER_LOSS = 0.025
SATIATED_LEVEL = 90
TOTAL_NUTRIENTS = 100.0
NUTRIENT_REFRESH_RATE = 0.1
MAX_POPULATION = 5000
MAX_HEALTH = 100.0

class EvolutionarySimulation:
    def __init__(self, planet_type, biome_type, uuid="default"):
        # Roll final states
        self.final_evolutionary_stage = self.roll_evolutionary_stage()
        self.current_milestone = self.roll_technological_milestone(self.final_evolutionary_stage),

        # Create the ecology model
        self.ecology = SpeciesGenerator(planet_type, uuid)
        self.life = Lifeform()
        self.genus = Genus()
        self.biome_type = biome_type
        self.total_population = 0
        self.dead_mass = 0 # for scavengers and decomposers
        prefix = self.primordial_biome_prefix()
        self.real_biome = prefix + ' ' + biome_type

        # Define initial conditions
        self.lifeforms = []  # List to store lifeform objects
        self.environment = {
            'Temperature': 20,
            'Gravity': 9.81,
            'Atmosphere Thickness': 1,
            'Water Coverage': 0.5,
            'Radiation': 0.5,
            'UV Index': 0.5,
            'Weather Pattern': 0.5,
            'Season': 0.5,
            'Water': TOTAL_NUTRIENTS,
            'Sunlight': 100,
            'Nutrients': TOTAL_NUTRIENTS
        }  # Dictionary to store environmental conditions
        self.current_epoch = 0
        self.total_epochs = 0 # point at which to evolve to next stage

        # Genetic Algorithm Parameters
        self.selection_criteria = {}  # Criteria for natural selection
        self.reproduction_rate = 0.1

        # Timescales
        self.epoch_duration = 100  # Example duration in arbitrary units

    environmental_effects = [
        # Temperature Impact
        lambda self, lifeform, bio_type: (-abs(self.environment['Temperature'] - 20) * (1 - lifeform["Thermal Resistance"] / 100)),

        # Gravity Impact on strength and endurance
        lambda self, lifeform, bio_type: (-abs(self.environment['Gravity'] - 9.81) * (1 - (lifeform["Strength"] + lifeform["Endurance"]) / 200)),

        # Gravity Impact on height and mass
        lambda self, lifeform, bio_type: (
            ((9.81 - self.environment['Gravity']) * lifeform["Height"] / 100) +
            ((9.81 - self.environment['Gravity']) * lifeform["Mass"] / 100)
        ),

        # Atmosphere Thickness Impact
        lambda self, lifeform, bio_type: (-abs(self.environment['Atmosphere Thickness'] - 1) * (1 - lifeform["Oxygen Utilization Efficiency"] / 100)),

        # Water Coverage Impact
        lambda self, lifeform, bio_type: (self.environment['Water Coverage'] * lifeform["Aquatic Adaptation"] / 100),

        # Radiation Impact
        lambda self, lifeform, bio_type: (-self.environment['Radiation'] * (1 - lifeform["Radiation Resistance"] / 100)),

        # Photosynthetic Ability Impact (for flora)
        lambda self, lifeform, bio_type: (self.environment['UV Index'] * lifeform["Photosynthetic Ability"] / 100) if bio_type == "Flora" else 0,

        # UV Index Impact
        lambda self, lifeform, bio_type: (-self.environment['UV Index'] * (1 - lifeform["Regeneration"] / 100)),

        # # Weather Patterns and Seasons Impact
        # lambda lifeform, weather_pattern: lifeform.update_health(-abs(weather_pattern - 0.5) * (1 - lifeform.traits["Adaptability"] / 100)),
    ]

    def run(self, lifeforms):
        # Unicellular stage
        self.evolutionary_stage_idx = 0
        self.evolutionary_stage = list(self.evolutionary_probability.keys())[self.evolutionary_stage_idx]
        
        self.lifeforms = self.create_initial_lifeforms(lifeforms)
        self.lifeforms = self.run_simulation(total_epochs=TOTAL_EPOCHS)
        
        # Complex stages
        for i in range(TOTAL_EVOLUTIONARY_STAGES-1):
            self.evolutionary_stage_idx += 1
            self.evolutionary_stage = list(self.evolutionary_probability.keys())[self.evolutionary_stage_idx]
            self.lifeforms = self.create_initial_lifeforms(self.lifeforms)
            self.lifeforms = self.run_simulation(total_epochs=TOTAL_EPOCHS)
            results = self.collect_data()
        return results
    
    def primordial_biome_prefix(self):
        ## First we generate initial species -- primordial single-celled organisms
        if self.biome_type in ["Forest", "Desert", "Ocean", "Tundra", "Grassland", "Wetlands", "Savanna", "Taiga", "Chaparral", "Temperate Deciduous Forest", "Temperate Rainforest", "Mediterranean", "Montane (Alpine)", "Coral Reefs", "Mangroves"]:
            return np.random.choice(['Primordial', 'Alien Primordial', 'Prebiotic'])
        else:
            return 'Alien Primordial'

    def create_initial_lifeforms(self, lifeforms):
        # Initial lifeform are generated from probability engine
        if self.evolutionary_stage_idx == 0:
            return self.initiate_life(lifeforms)
        else:
            # Mutate and evolve the next stage of life -- reset population for fairness
            self.mutate_lifeforms()
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
                # lifeform.role = lifeform.choose_role(self.evolutionary_stage_idx, lifeform.consumption_roles, lifeform)
                # lifeform.population = int(INITIAL_POPULATION * lifeform.consumption_pop_modifiers[lifeform.role])
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

            generative_data = self.ecology.generate(
                self.real_biome,
                self.evolutionary_stage,
                new_species.genus,
                new_species.role,
                new_species.behavioral_role,
                attributes=new_species.species_data["Life Form Attributes"],
            )
            # lifeform.update(generative_data)
            logger.info("generated species {}".format(generative_data))

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
            for effect in self.environmental_effects:
                for individual_idx in range(len(lifeform.individuals)):
                    genetics = lifeform.decode_genetics(lifeform.individuals[individual_idx][0], lifeform.genetic_base_line)
                    lifeform.individuals[individual_idx][1] += effect(self, genetics, lifeform.species_data['Biological Type'])
                    if lifeform.individuals[individual_idx][1] <= 0:
                        lifeform.individuals[individual_idx][1] = 0
                        lifeform.population -= 1

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
        self.environment['Water'] = min(TOTAL_NUTRIENTS, self.environment['Water'] + (TOTAL_NUTRIENTS * NUTRIENT_REFRESH_RATE))
        self.environment['Sunlight'] = TOTAL_NUTRIENTS # Sunlight always hits max each turn, limit represents canopy
        self.environment['Nutrients'] = min(TOTAL_NUTRIENTS, self.environment['Nutrients'] + (TOTAL_NUTRIENTS * NUTRIENT_REFRESH_RATE))

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

    def collect_data(self):
        # Collect and return data from the simulation
        return {
            "lifeforms": self.lifeforms,
            "environment": self.environment,
            "current_epoch": self.current_epoch,
            "final_evolutionary_stage": self.final_evolutionary_stage,
            "current_milestone": self.current_milestone
        }

    def analyze_outcomes(self):
        # Analyze the outcomes of the simulation
        pass  # Implement analysis logic

    def roll_technological_milestone(self, evolutionary_stage):
        # Iterate through each key and value
        if evolutionary_stage not in self.technological_milestones:
            return None
        milestones = self.technological_milestones[evolutionary_stage]['milestones']
        return milestones[np.random.randint(0, len(milestones))]
        
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
    
    evolutionary_probability = {
        'Single-celled organisms': 0.95,
        'Multi-celled organisms': 0.80,
        'Complex lifeforms': 0.75,
        'Primitive Civilization - Hunter Gatherers': 0.5, # early sentience evolves from complex lifeforms
        'Primitive Civilization - Tribal Societies': 0.45,
        'Classical Civilization - City States and Empires': 0.45,
        'Feudal Civilization - Medieval Era': 0.4,
        'Feudal Civilization - Renaissance': 0.35,
        'Industrial Civilization - Industrial Era': 0.35,
        'Industrial Civilization - Atomic Era': 0.3,
        'Information Civilization - Digital Era': 0.25,
        'Spacefaring Civilization - Homebound': 0.2,
        'Spacefaring Civilization - Multiplanetary': 0.15,
        'Interstellar Civilization': 0.1
    }

    # THIS IS CAPSTONE CONCEPTS FROM PRE-HISTORY TO SPACE AGE
    technological_milestones = {
        'Advanced Civilization - Early Societies': {
            'milestones': [
                'Development of Agriculture',
                'Invention of Writing',
                'Bronze Age Technology'
            ]
        },
        'Advanced Civilization - Classical Era': {
            'milestones': [
                'Philosophy and Early Science',
                'Aqueducts and Engineering',
                'Expansion of Trade and Cultural Exchange'
            ]
        },
        'Advanced Civilization - Medieval Era': {
            'milestones': [
                'Feudal Systems and Governance',
                'Architectural Advancements (e.g., Castles, Cathedrals)',
                'Early Navigational Tools and Exploration'
            ]
        },
        'Advanced Civilization - Renaissance': {
            'milestones': [
                'Revival of Arts and Sciences',
                'Invention of Printing Press',
                'Early Modern Philosophy and Humanism'
            ]
        },
        'Advanced Civilization - Industrial Era': {
            'milestones': [
                'Steam Engine',
                'Electricity Harnessing',
                'Assembly Line Manufacturing'
            ]
        },
        'Advanced Civilization - Atomic Era': {
            'milestones': [
                'Nuclear Fission',
                'Space Exploration Initiation',
                'Advanced Materials Science'
            ]
        },
        'Advanced Civilization - Information Era': {
            'milestones': [
                'Internet Inception',
                'Quantum Computing',
                'Genetic Engineering'
            ]
        },
        'Advanced Civilization - Digital Age': {
            'milestones': [
                'Widespread Artificial Intelligence',
                'Virtual Reality and Augmented Reality Integration',
                'Advanced Robotics and Automation'
            ]
        },
        'Early Spacefaring Civilization': {
            'milestones': [
                'Interplanetary Travel',
                'Orbital Infrastructure',
                'Advanced Propulsion Systems'
            ]
        },
        'Advanced Spacefaring Civilization': {
            'milestones': [
                'Permanent Extraterrestrial Colonies',
                'Asteroid Mining and Resource Exploitation',
                'Deep Space Exploration and Habitats'
            ]
        }
    }