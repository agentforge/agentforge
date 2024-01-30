import random
from agentforge.ai.worldmodel.lifeform import Lifeform
from agentforge.ai.worldmodel.generator import SpeciesGenerator
import numpy as np
from collections import defaultdict
from agentforge.utils import logger


""" Evolution baby! A Genetic Algorithm for simulating evolution of lifeforms on a planet

bio_info = {
    "Biological": biological_type,
    "Biological Characteristics": self.lifeform.biologic_concepts[biological_type].metadata,
    "Life Form Attributes": life_form_characteristic_list,
    "Evolutionary Stage": final_evolutionary_stage,
    "Technological Milestone": self.lifeform.roll_technological_milestone(final_evolutionary_stage),
    "Genetic Profile": self.lifeform.sample_genetic_profile(biological_type),
}

"""

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

class HuntReportData:
    def __init__(self):
        self.success = 0
        self.fail = 0
        self.fail_roll = 0
        self.no_prey = 0
        self.no_prey_at_all = 0

    def __str__(self):
        return "success: {} fail: {} fail_roll: {} no_prey: {} no_prey_at_all: {}".format(self.success, self.fail, self.fail_roll, self.no_prey, self.no_prey_at_all)

    def __repr__(self):
        return self.__str__()

class HuntReport:
    def __init__(self):
        self.hunt_report = {}
    
    def add_success(self, role):
        if role not in self.hunt_report:
            self.hunt_report[role] = HuntReportData()
        self.hunt_report[role].success += 1
    
    def add_fail(self, role):
        if role not in self.hunt_report:
            self.hunt_report[role] = HuntReportData()
        self.hunt_report[role].fail += 1

    def add_fail_roll(self, role):
        if role not in self.hunt_report:
            self.hunt_report[role] = HuntReportData()
        self.hunt_report[role].fail_roll += 1

    def add_no_prey(self, role):
        if role not in self.hunt_report:
            self.hunt_report[role] = HuntReportData()
        self.hunt_report[role].no_prey += 1
    
    def add_no_prey_at_all(self, role):
        if role not in self.hunt_report:
            self.hunt_report[role] = HuntReportData()
        self.hunt_report[role].no_prey_at_all += 1

    def __str__(self):
        return str(self.hunt_report)

    def __repr__(self):
        return self.__str__()

class Species:
    def __init__(self, species_data, evolutionary_stage, health=100):
        self.species_data = species_data
        self.genetic_base_line = species_data["Genetic Profile"]
        self.reproduction_type = self.determine_reproduction(evolutionary_stage)
        self.individuals = []  # List to store individual lifeforms

    def generate_population(self, health=100):
        encoded_genetics =  self.encode_genetics(self.genetic_base_line)
        logger.info("Generating {}".format(self.population))
        for x in range(self.population):
            encoded_genetics = self.mutate(encoded_genetics)
            # Create initial individuals
            self.individuals.append([
                encoded_genetics,
                health,
                self.genetic_base_line
            ])

        logger.info(len(self.individuals))

    def analyze_health_statistics(self):
        # Extract health values from the array
        health_values = np.array([individual[1] for individual in self.individuals], dtype=float)

        # Check if health_values is empty
        if health_values.size == 0:
            return 0, 0, 0  # Return default values for average, max, and min health

        # Calculate average, max, and min health
        average_health = np.mean(health_values) if health_values.size > 0 else 0
        max_health = np.max(health_values) if health_values.size > 0 else 0
        min_health = np.min(health_values) if health_values.size > 0 else 0

        return self.genus, self.species_data['Biological Type'], self.role, round(average_health,2), round(max_health,2), round(min_health,2), self.population

    def __str__(self):
        return self.species_data['Name'] + "\n" + self.species_data['Type'] + "\n" + self.species_data['Description'] + "\n" + self.role + "\n" + self.behavioral_role + " \nAverage Health:" + str(self.analyze_health_statistics()) + " \nPopulation:" + str(round(self.population, 2)) + " " + self.reproduction_type

    def __repr__(self):
        return self.__str__()
    
    def decrease_population_based_on_health(self):
        survived_individuals = []
        death_rates = []

        for individual in self.individuals:
            # Death rate increases as health decreases, with a more gradual distribution
            health_based_death_rate = (1-(individual[2]["Longevity"]/100.0)) + 0.45 * ((100 - individual[1]) / 100)

            # Calculate total death rate, ensuring it doesn't exceed the maximum
            total_death_rate = min(health_based_death_rate, MIN_DEATH_RATE)
            death_rates.append(total_death_rate)

            # Determine if individual survives based on the death rate
            if random.random() > total_death_rate and individual[1] > 0:
                survived_individuals.append(individual)

        # Update individuals and population
        killed = len(self.individuals) - len(survived_individuals)
        death_rate_percentage = 0
        if len(death_rates) > 0:
            death_rate_percentage = sum(death_rates) / len(death_rates)
        logger.info("{} {} killed {}%".format(self.role, killed, death_rate_percentage))
        self.individuals = survived_individuals
        self.population = len(self.individuals)

    """
    ECOLOGICAL ROLES

    Primary Consumers (Herbivores): Feed directly on producers (e.g., deer, grasshoppers).
    Secondary Consumers (Carnivores): Predators that feed on herbivores (e.g., lions, wolves).
    Tertiary Consumers: Predators that feed on secondary consumers (e.g., eagles, large sharks).
    Omnivores: Organisms that consume both plants and animals (e.g., bears, humans).
    Scavengers: Feed on dead animals and plant material (e.g., vultures, hyenas).
    Decomposers: Break down dead organic material, returning nutrients to the ecosystem (e.g., fungi, bacteria).
    Detritivores: Consume decomposing organic matter (e.g., earthworms, dung beetles).
    Pollinators: Facilitate plant reproduction by transferring pollen (e.g., bees, butterflies, certain birds and bats).
    Parasites: Live on or in a host organism, benefiting at the host's expense without immediate lethality (e.g., ticks, tapeworms).
    Parasitoids: Insects that lay eggs in or on a host, eventually leading to the host's death (e.g., certain wasps).
    """
    consumption_roles =  [
        ["Producers", 0.75, 1.0, 1.0],
        ["Primary Consumers", 0.5, 1.0, 1.0],
        ["Secondary Consumers", 0.1, 0.8, 1.0],
        ["Tertiary Consumers", 0.0, 0.5, 1.0],
        ["Omnivores", 0.0, 0.6, 1.0],
        # ["Scavengers", 0.1, 0.7, 1.0],
        # ["Decomposers", 0.8, 1.0, 1.0],
        # ["Detritivores", 0.0, 0.7, 1.0],
        # ["Pollinators", 0.0, 0.4, 0.9],
        # ["Parasites", 0.3, 0.9, 1.0],
        # ["Parasitoids", 0.0, 0.3, 0.8],
    ]

    consumption_pop_modifiers = {
        "Producers": 1.0,
        "Primary Consumers": 0.3,
        "Secondary Consumers": 0.15,
        "Tertiary Consumers": 0.05,
        "Omnivores": 0.3,
        "Scavengers": 0.25,
        "Decomposers": 0.25,
        "Detritivores": 0.25,
        "Pollinators": 0.25,
        "Parasites": 0.25,
        "Parasitoids": 0.25,
    }

    # Behavior roles can influence some of the simulation outcomes
    behavioral_roles = [
        ["Mutualists", 0.1, 0.6, 1.0],
        ["Symbiotic Partners", 0.1, 0.5, 1.0],
        ["Competitors", 0.3, 0.9, 1.0],
        ["Indicator Species", 0.0, 0.3, 0.7],
        ["Engineer Species", 0.0, 0.2, 0.4],
        ["Migratory Species", 0.0, 0.4, 1.0],
        ["Territorial Defenders", 0.0, 0.5, 1.0],
        ["Nocturnal Species", 0.0, 0.3, 1.0],
        ["Diurnal Species", 0.0, 0.3, 1.0],
        ["Eco-Sensitive Species", 0.0, 0.2, 0.5]
    ]

    # Probability matrix for sexual and asexual reproduction
    reproduction_probabilities = [
        [0.3, 0.7],  # Unicellular
        [0.7, 0.3],  # Multicellular
        [0.9, 0.1]   # Complex Life
    ]

    def determine_reproduction(self, evolutionary_stage):
        reproduction_types = ["Sexual", "Asexual"]
        probabilities = self.reproduction_probabilities[evolutionary_stage]

        # Choose reproduction type based on probabilities
        reproduction_type = np.random.choice(reproduction_types, p=probabilities)
        return reproduction_type

    def choose_role(self, evolutionary_stage, role_source, species):
        roles = [role[0] for role in role_source]
        probabilities = [role[evolutionary_stage + 1] for role in role_source]

        # # Find the last role in the list that exists in the species
        # existing_roles = [s.role for s in species]
        # for i, role in enumerate(roles):
        #     last_role_index = None
        #     if role in existing_roles:
        #         last_role_index = i

        # # If such a role is found, increase the index of the next role, if it doesn't exceed the length of roles
        # if last_role_index is not None and last_role_index + 1 < len(roles):
        #     next_index = last_role_index + 1
        #     probabilities[next_index] *= 100  # Significantly increase the probability of the next role

        # Normalize probabilities to sum to 1
        total = sum(probabilities)
        normalized_probabilities = [p / total for p in probabilities]

        return np.random.choice(roles, p=normalized_probabilities)

    def encode_genetics(self, traits, single_trait_length=13):
        # Assuming equal distribution of length for each trait

        def to_binary(value, max_length):
            # Adjust the value for two decimal places
            adjusted_value = round(value * 100)  # e.g., 99.99 becomes 9999

            # Normalize value to fit in the binary range
            # The maximum value is now 10000 instead of 100 to account for two decimal places
            normalized = int(adjusted_value / 10000 * (2**max_length - 1))

            # Convert to binary and pad to fixed length
            binary_val = format(normalized, '0' + str(max_length) + 'b')
            return binary_val

        binary_string = ''
        for trait, value in traits.items():
            binary_string += to_binary(value, single_trait_length)
        return binary_string

    def decode_genetics(self, binary_string, traits, single_trait_length=13):
        # Assuming equal distribution of length for each trait
        trait_values = {}
    
        def from_binary(binary, max_length):
            # Convert from binary to decimal
            decimal = int(binary, 2)

            # Normalize value back to original range
            # Adjust back for two decimal places
            normalized = decimal / (2**max_length - 1) * 10000  # Normalize to 10000

            # Convert back to the format with two decimal places
            return normalized / 100  # e.g., 9999 becomes 99.99
        
        for i, trait in enumerate(traits):
            start = i * single_trait_length
            end = start + single_trait_length
            trait_binary = binary_string[start:end]
            trait_values[trait] = from_binary(trait_binary, single_trait_length)

        return trait_values


    def mutate(self, encoded_genetics, length=24):
        # Convert the binary string to a list for mutation
        binary_list = list(encoded_genetics)

        # Calculate the mutation chance for each bit
        for i in range(length):
            if random.random() < MUTATION_RATE:
                # Flip the bit
                binary_list[i] = '1' if binary_list[i] == '0' else '0'

        # Convert back to a binary string
        return ''.join(binary_list)

    def calculate_fitness(self, environmental_factors):
        # Calculate fitness based on environmental factors and genetic traits
        pass  # Implement fitness calculation logic

    def reproduce(self, replace=False):
        offspring = []
        offspring_number = self.genetic_base_line["Offspring"]
        if replace:
            offspring_number = 1
        reproduction_rates = []
        for idx, individual in enumerate(self.individuals):
            if individual[1] <= 0:
                continue # Skip dead individuals
            decoded_genetics = self.decode_genetics(individual[0], self.genetic_base_line)
            reproduction_rate = decoded_genetics["Reproductive Rate"]
            reproduction_rate = reproduction_rate / 100.0
            health_factor = individual[1] / 100.0
            reproduction_probability = reproduction_rate * health_factor * REPRODUCTION_MODIFIER
            reproduction_rates.append(reproduction_probability)
            if random.random() < reproduction_probability:
                for _ in range(int(offspring_number)):
                    if self.reproduction_type == "Asexual":
                        offspring.append(individual)  # Clone the individual
                    elif self.reproduction_type == "Sexual":
                        partner = self.select_mate()  # Select a mate for sexual reproduction
                        new_genetics = self.genetic_crossover(individual[0], partner[0])
                        decoded_genetics = self.decode_genetics(new_genetics, self.genetic_base_line)
                        offspring.append([new_genetics, 100, decoded_genetics])  # New offspring with full health
                if replace:
                    self.individuals[idx] = offspring[0]

        # Append offspring to the population
        if not replace:
            for new_individual in offspring:
                self.individuals.append(new_individual)

        self.population = len(self.individuals)
        total  = sum(reproduction_rates) / len(reproduction_rates)
        # logger.info("reproduction rate {}%".format(total))

    def select_mate(self):
        # Select a mate randomly for sexual reproduction
        random_index = np.random.randint(0, len(self.individuals))
        return self.individuals[random_index]

    def genetic_crossover(self, genetics1, genetics2):
        # Implement logic for genetic crossover in sexual reproduction
        crossover_point = random.randint(1, len(genetics1) - 1)
        return genetics1[:crossover_point] + genetics2[crossover_point:]

    def adapt_to_environment(self, environment):
        # Adapt species traits based on the given environment
        pass  # Implement environmental adaptation logic

    # For mainline consumers and producers
    def identify_food(self, lifeforms):
        # Identify food sources based on the given environment
        possible_prey = []
        for prey in lifeforms:
            if prey.population <= 0: # dead species
                continue
            # Primary Consumers (Herbivores): Feed directly on producers (e.g., deer, grasshoppers).
            if prey.role == "Producers" and self.role in ["Primary Consumers", "Omnivores"]:
                possible_prey.append(prey)
            if prey.role in ["Primary Consumers", "Omnivores"] and self.role in ["Secondary Consumers", "Omnivores"]:
                possible_prey.append(prey)
            if prey.role in ["Secondary Consumers", "Omnivores"] and self.role in ["Tertiary Consumers", "Omnivores"]:
                possible_prey.append(prey)

        return possible_prey
    
    def roll_for_prey_location(self, predator, possible_prey, total_population):
        prey_possible = []
        for prey in possible_prey:
            if prey.population <= 0 or len(prey.individuals) <= 0 or prey == predator:
                continue
            prey_possible.append(prey)

        # Grab a random prey, implement location logic later
        return np.random.choice(prey_possible)
    
    def autotropic_growth(self, individual, environment):
        # Extracting individual's attributes
        resource_utilization = individual[2]['Resource Utilization'] / 100.0
        mass = individual[2]['Mass']
        photosynthetic_ability = individual[2]['Photosynthetic Ability'] / 100.0
        nutritional_requirements = individual[2]['Nutritional Requirements'] / 100.0
        current_health = individual[1]

        # Calculate realistic resource consumption
        water_consumption = min(resource_utilization * mass * PLANT_GROWTH_FACTOR, environment['Water'] * PLANT_GROWTH_FACTOR)
        sunlight_consumption = min(photosynthetic_ability * mass * PLANT_GROWTH_FACTOR, environment['Sunlight'] * PLANT_GROWTH_FACTOR)
        nutrient_consumption = min(resource_utilization * mass * PLANT_GROWTH_FACTOR, environment['Nutrients'] * PLANT_GROWTH_FACTOR)

        # Reduce available resources in the environment
        environment['Water'] -= water_consumption
        environment['Sunlight'] -= sunlight_consumption
        environment['Nutrients'] -= nutrient_consumption

        # Update individual's health based on resource consumption and nutritional requirements
        growth = water_consumption + sunlight_consumption + nutrient_consumption
        health_increase = min(growth, 100 - current_health)
        health_decrease_due_to_nutrition = nutritional_requirements * mass
        # logger.info("health_increase {}".format(health_increase - health_decrease_due_to_nutrition))
        individual[1] = max(0, current_health + health_increase - health_decrease_due_to_nutrition)  # Ensure health doesn't go below 0
        # logger.info("water left {}".format(environment['Water']))
        # logger.info("current_health + health_increase - health_decrease_due_to_nutrition = health")
        # logger.info("{} + {} - {} = {}".format(current_health, health_increase, health_decrease_due_to_nutrition, individual[1]))

        return environment

    def roll_for_consumption(self, predator, food):
        # Factors influencing consumption success
        predation_success_factors = {
            "Strength": 0.3,  # Strength's influence on the success rate
            "Speed": 0.2,     # Speed's influence
            "Stealth": 0.2,   # Stealth's influence
            "Predation Instincts": 0.3,  # Predatory instincts' influence
            "Toxin Production": 0.3,  # Toxin production's influence
            "Toxin Resistance": 0.3  # Toxin resistance's influence
        }

        food_defense_factors = {
            "Toxin Production": 0.3,   # Influence of toxin production
            "Toxin Resistance": 0.3,   # Influence of toxin resistance
            "Speed": 0.3,              # Influence of speed (for evasion)
            "Strength": 0.2,           # Influence of strength (in self-defense)
            "Dexterity": 0.2,          # Influence of dexterity (in self-defense)
            "Intelligence": 0.3        # Influence of intelligence (in self-defense)
        }

        # Calculate predator's success potential based on its traits
        predation_potential = sum([predator[2][trait] * weight for trait, weight in predation_success_factors.items()])

        # Adjust for the predator's toxin resistance
        predation_potential -= predator[2]["Toxin Resistance"] * predation_success_factors["Toxin Resistance"]

        # Calculate food's defense potential based on its traits
        food_defense = sum([food[2][trait] * weight for trait, weight in food_defense_factors.items()])
        # Adjust for the food's toxin resistance
        food_defense -= food[2]["Toxin Resistance"] * food_defense_factors["Toxin Resistance"]

        # Determine the overall success rate
        success_rate = predation_potential / (predation_potential + food_defense)

        # Roll for consumption success
        return random.random() < success_rate
    
    def get_weak_individuals(self):
        # Check if there are no individuals
        if len(self.individuals) == 0:
            return None, None

        # Extract health values
        health_values = np.array([individual[1] for individual in self.individuals], dtype=float)

        # Replace NaN values with a large number to effectively make their probability zero
        health_values = np.nan_to_num(health_values, nan=9999999)

        # Invert health values to bias towards lower health
        inverted_health = 1 / health_values

        # Normalize the inverted health values to get probabilities
        probabilities = inverted_health / np.sum(inverted_health)
        probabilities = np.nan_to_num(probabilities, nan=0)
        probabilities = np.maximum(probabilities, 0)

        total = sum(probabilities)
        if total == 0:
            return None, None

        normalized_probabilities = [p / total for p in probabilities]

        # Select an index based on these probabilities
        try:
            selected_index = np.random.choice(len(self.individuals), p=normalized_probabilities)
        except Exception as e:
            logger.info(normalized_probabilities)
            logger.info(health_values)
            raise e
        selected_individual = self.individuals[selected_index]

        return selected_individual, selected_index

    def consume(self, predator, prey, prey_ind):
        # Handle consumption of prey
        health_percentage = (prey_ind[2]['Mass']/100.0 * HEALTH_CONSUMPTION_FACTOR)
        consumed = prey_ind[1] * health_percentage
        # more efficient predators consume more
        # logger.info("Mass {}".format(prey_ind[2]['Mass']/100.0))
        # logger.info("gained {} health % {}".format(consumed / (predator[2]['Resource Utilization']/100.0), health_percentage))
        predator[1] += min(MAX_HEALTH, consumed * (predator[2]['Resource Utilization']/100.0))
        # prey.population -= 1y

    def consume_decomposing_matter(self):
        # Handle consumption of dead organisms -- calculate how much dead mass the scavenger should consume
        pass

    def pollinate(self):
        # Handle pollination of plants -- pollinators should increase health of plants
        pass

    def parasitic_interaction(self):
        # Handle parasitic interaction with host
        pass

class EvolutionarySimulation:
    def __init__(self, planet_type, biome_type, uuid="default"):
        # Roll final states
        self.final_evolutionary_stage = self.roll_evolutionary_stage()
        self.current_milestone = self.roll_technological_milestone(self.final_evolutionary_stage),

        # Create the ecology model
        self.ecology = SpeciesGenerator(planet_type, uuid)
        self.life = Lifeform()
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

                lifeform.genus = self.get_genus(lifeform.species_data["Biological Type"], self.evolutionary_stage)
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
            new_species.genus = self.get_genus(new_species.species_data["Biological Type"], self.evolutionary_stage)
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
    
    def get_genus(self, biological_type, evolutionary_stage):
        if biological_type not in self.lifeform_genus_data:
            return "Exotic"
        probabilities = list(self.lifeform_genus_data[biological_type][evolutionary_stage].values())
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]
        names = list(self.lifeform_genus_data[biological_type][evolutionary_stage].keys())
        return np.random.choice(names, p=probabilities)

    evolutionary_probability = {
        'Single-celled organisms': 0.95,
        'Multi-celled organisms': 0.80,
        'Complex lifeforms': 0.75,
        'Primitive civilization': 0.5, # early sentience evolves from complex lifeforms
        'Advanced Civilization - Early Societies': 0.45,
        'Advanced Civilization - Classical Era': 0.45,
        'Advanced Civilization - Medieval Era': 0.4,
        'Advanced Civilization - Renaissance': 0.35,
        'Advanced Civilization - Industrial Era': 0.35,
        'Advanced Civilization - Atomic Era': 0.3,
        'Advanced Civilization - Information Era': 0.25,
        'Advanced Civilization - Digital Age': 0.2,
        'Early Spacefaring Civilization': 0.2,
        'Advanced Spacefaring Civilization': 0.15,
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

    flora_genus = {
        "Single-celled organisms": {
                "Chlorella": 1.0,
                "Volvox": 1.0,
                "Diatoms": 1.0,
                "Cyanobacteria": 1.0,
                "Spirulina": 1.0,
        },
        "Multi-celled organisms": {
            "Mosses": 1.0,
            "Liverworts": 1.0,
            "Hornworts": 1.0,
            "Ferns": 1.0,
            "Horsetails": 1.0,
            "Bryophytes" : 1.0,
            "Conifers": 1.0,
            "Cycads": 1.0,
            "Gymnosperms": 1.0,
        },
        "Complex lifeforms": {
            "Monocots (e.g., Grasses, Orchids)": 1.0,
            "Dicots (e.g., Roses, Sunflowers)": 1.0,
            "Woody Plants (Trees, Shrubs)": 1.0,
            "Herbaceous Plants (Non-woody Plants)": 1.0,
        }
    }

    # More speciiic life form concepts -- to supply LLM prompts
    lifeform_genus_data = {
        "Terrestrial": {
            "Single-celled organisms": {
                "Bacteria": 1.0, 
                "Archaea": 1.0,
                "Protozoa": 1.0,
                "Unicellular Fungi (e.g., Yeasts)": 1.0,
                "Protists (e.g., Amoebas, Slime Molds)": 1.0,
                "Choanoflagellates": 1.0,
                "Ciliates (such as Paramecium)": 1.0,
                "Flagellates (e.g., Euglena)": 1.0,
            },
            "Multi-celled organisms": {
                "Fungi": 1.0,
                "Molds": 1.0,
                "Mildews": 1.0,
                "Yeast": 1.0,
                "Simple Annelids": 1.0,  
            },
            "Complex lifeforms": {
                "Mammals": 1.0,
                "Birds": 1.0,
                "Reptiles": 1.0,
                "Amphibians": 1.0,
                "Fish": 1.0,
                "Coleoptera (Beetles)": 1.0,
                "Lepidoptera (Butterflies and Moths)": 1.0,
                "Hymenoptera (Bees, Wasps, Ants)": 1.0,
                "Diptera (Flies)": 1.0,
                "Hemiptera (True Bugs)": 1.0,
                "Odonata (Dragonflies)": 1.0,
                "Orthoptera (Grasshoppers)": 1.0,
                "Araneae (Spiders)": 1.0,
                "Gastropoda (Snails)": 1.0,
                "Isoptera (Termites)": 1.0,
                "Lagomorpha (Rabbits)": 1.0,
                "Mantodea (Praying Mantises)": 1.0,
                "Blattodea (Cockroaches)": 1.0,
                "Myriapods": 1.0,
                "Arachnids": 1.0,
                "Arachnids": 1.0,
                "Felines": 1.0,
                "Canines": 1.0,
                "Primates": 1.0,
                "Rodents": 1.0,
                "Bovines": 1.0,
                "Equines": 1.0,
                "Porcines": 1.0,
                "Avians": 1.0,
                "Annelids": 1.0,
                "Mollusks": 1.0,
            }
        },
        "Aquatic": {
            "Single-celled organisms": {
                "Phytoplankton (e.g., Diatoms, Dinoflagellates)": 1.0,
                "Green Algae (e.g., Chlamydomonas)": 1.0,
                "Foraminifera": 1.0,
            },
            "Multi-celled organisms": {
                "Sponges (Porifera)": 1.0,
                "Coenocytic Organisms": 1.0,
                "Cnidarians": 1.0,
                "Flatworms": 1.0,
                "Roundworms": 1.0,
                "Mollusks": 1.0,
                "Annelids": 1.0,
                "Arthropods": 1.0,
                "Echinoderms": 1.0,
                "Chordates": 1.0,
            },
            "Complex lifeforms": {
                "Corals": 1.0,
                "Sponges": 1.0,
                "Algae": 1.0,
                "Anemones": 1.0,
                "Polychaetes": 1.0,
                "Parrotfish": 1.0,
                "Butterflyfish": 1.0,
                "Octopuses": 1.0,
                "Urchins": 1.0,
                "Turtles": 1.0,
                "Sharks": 1.0,
                "Groupers": 1.0,
                "Eels": 1.0,
                "Barracudas": 1.0,
                "Lionfish": 1.0,
            }
        },
        "Flora": flora_genus,
        "Cold-Tolerant Flora": flora_genus,
    }
