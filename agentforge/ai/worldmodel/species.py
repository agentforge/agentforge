import random
import numpy as np
from agentforge.utils import logger
import uuid as uuid

MIN_DEATH_RATE = 0.01  # 5% minimal death rate
REPRODUCTION_MODIFIER = 0.1  # 1.0 is default
MAX_HEALTH = 100.0
HEALTH_CONSUMPTION_FACTOR = 0.1
MUTATION_RATE = 0.05
PLANT_GROWTH_FACTOR = 0.30
class Species:
    def __init__(self, species_data, evolutionary_stage):
        self.species_data = species_data
        self.reproduction_type = self.determine_reproduction(evolutionary_stage)
        self.individuals = []  # List to store individual lifeforms
        self.population = 0
        self.evolutionary_stage = evolutionary_stage
        self.uuid = str(uuid.uuid4())
        self.role = ""
        self.behavioral_role = ""
        self.genus = ""

    def genetic_base_line(self):
        return self.species_data["Genetic Profile"]
    
    def get_trait(self, trait):
        return round(self.genetic_base_line()[trait] / 100.0, 2)

    def save(self, db, collection: str):
        """Save the species instance to MongoDB."""
        species_dict = {
            "species_data": self.species_data,
            "reproduction_type": self.reproduction_type,
            "population": self.population,
            "individuals": self.individuals,
            "evolutionary_stage": self.evolutionary_stage,
            "role": self.role,
            "behavioral_role": self.behavioral_role,
            "genus": self.genus
        }
        db.set(collection, self.uuid, species_dict)

    @classmethod
    def load(cls, db, collection: str, key: str):
        """Load a species instance from MongoDB."""
        species = db.get(collection, key)
        if species:
            species_data = species["species_data"]
            # Create a new Species instance with the loaded data
            species_instance = cls(species_data, species["evolutionary_stage"])
            for key, value in species.items():
                setattr(species_instance, key, value)
            return species_instance
        else:
            return None

    def generate_population(self, health=100):
        encoded_genetics =  self.encode_genetics(self.genetic_base_line())
        logger.info("Generating {}".format(self.population))
        for x in range(self.population):
            encoded_genetics = self.mutate(encoded_genetics)
            # Create initial individuals
            self.individuals.append([
                encoded_genetics,
                health,
                self.genetic_base_line()
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
        offspring_number = self.genetic_base_line()["Offspring"]
        if replace:
            offspring_number = 1
        reproduction_rates = []
        for idx, individual in enumerate(self.individuals):
            if individual[1] <= 0:
                continue # Skip dead individuals
            decoded_genetics = self.decode_genetics(individual[0], self.genetic_base_line())
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
                        decoded_genetics = self.decode_genetics(new_genetics, self.genetic_base_line())
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

