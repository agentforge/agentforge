import random
from agentforge.ai.worldmodel.lifeform import Lifeform
from agentforge.ai.worldmodel.generator import SpeciesGenerator
import numpy as np

""" Evolution baby! A Genetic Algorithm for simulating evolution of lifeforms on a planet

bio_info = {
    "Biological": biological_type,
    "Biological Characteristics": self.lifeform.biologic_concepts[biological_type].metadata,
    "Life Form Attributes": life_form_characteristic_list,
    "Evolutionary Stage": final_evolutionary_stage,
    "Technological Milestone": self.lifeform.roll_technological_milestone(final_evolutionary_stage),
    "Genetic Profile": self.lifeform.sample_genetic_profile(biological_type),
    "system_uuid": star_id,
}

"""

HEALTH_CONSUMPTION_FACTOR = 0.1

class Species:
    def __init__(self, species_data, health=100):
        self.genetics = species_data["Genetic Profile"]
        self.encoded_genetics = self.encode_genetics(self.genetics)
        self.health = health
        self.population = species_data["Population"]
        species_data['Ecological Role'] = self.choose_role(self.evolutionary_stage_idx, self.consumption_roles)
        species_data['Behavioral Role'] = self.choose_role(self.evolutionary_stage_idx, self.behavioral_roles)
        self.determine_reproduction(self.evolutionary_stage_idx)
        self.species_data = species_data

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
        ["Producers", 1.0, 1.0, 1.0],
        ["Primary Consumers", 0.2, 1.0, 1.0],
        ["Secondary Consumers", 0.1, 0.8, 1.0],
        ["Tertiary Consumers", 0.0, 0.5, 1.0],
        ["Omnivores", 0.0, 0.6, 1.0],
        ["Scavengers", 0.1, 0.7, 1.0],
        ["Decomposers", 0.8, 1.0, 1.0],
        ["Detritivores", 0.0, 0.7, 1.0],
        ["Pollinators", 0.0, 0.4, 0.9],
        ["Parasites", 0.3, 0.9, 1.0],
        ["Parasitoids", 0.0, 0.3, 0.8],
    ]

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
        self.reproduction_type = reproduction_type

    # Ecological Role for Unicellular, Multicellular, Complex Life
    def choose_role(self, evolutionary_stage, role_source):
        roles = [role[0] for role in role_source]
        probabilities = [role[evolutionary_stage + 1] for role in role_source]

        # Normalize probabilities to sum to 1
        total = sum(probabilities)
        normalized_probabilities = [p / total for p in probabilities]

        return np.random.choice(roles, p=normalized_probabilities)
    
    def encode_genetics(traits, length=24):
        # Assuming equal distribution of length for each trait
        single_trait_length = length // len(traits)
        
        # Function to convert a value to a fixed-length binary string
        def to_binary(value, max_length):
            # Normalize value to fit in the binary range
            normalized = int(value / 100 * (2**max_length - 1))
            # Convert to binary and pad to fixed length
            return format(normalized, '0' + str(max_length) + 'b')

        binary_string = ''
        for trait, value in traits.items():
            binary_string += to_binary(value, single_trait_length)

        return binary_string

    def decode_genetics(self, binary_string, traits, length=24):
        # Assuming equal distribution of length for each trait
        single_trait_length = length // len(traits)
        trait_values = {}

        # Function to convert a binary string to its original value
        def from_binary(binary, max_length):
            # Convert from binary to decimal
            decimal = int(binary, 2)
            # Normalize value back to original range
            return decimal / (2**max_length - 1) * 100

        for i, trait in enumerate(traits):
            start = i * single_trait_length
            end = start + single_trait_length
            trait_binary = binary_string[start:end]
            trait_values[trait] = from_binary(trait_binary, single_trait_length)

        return trait_values


    def mutate(self, binary_string, mutation_rate, length=24):
        # Convert the binary string to a list for mutation
        binary_list = list(binary_string)

        # Calculate the mutation chance for each bit
        for i in range(length):
            if random.random() < mutation_rate:
                # Flip the bit
                binary_list[i] = '1' if binary_list[i] == '0' else '0'

        # Convert back to a binary string
        return ''.join(binary_list)

    def calculate_fitness(self, environmental_factors):
        # Calculate fitness based on environmental factors and genetic traits
        pass  # Implement fitness calculation logic

    def reproduce(self, reproduction_rate):
        # Handle reproduction based on the species' reproduction rate
        offspring = []  # List of offspring species
        pass  # Implement reproduction logic
        return offspring

    def adapt_to_environment(self, environment):
        # Adapt species traits based on the given environment
        pass  # Implement environmental adaptation logic

    # For mainline consumers and producers
    def identify_food(self, role, lifeforms):
        # Identify food sources based on the given environment
        possible_prey = []
        for prey in lifeforms:
            # Primary Consumers (Herbivores): Feed directly on producers (e.g., deer, grasshoppers).
            if prey.role == "Producers" and role in ["Primary Consumers", "Omnivores"]:
                possible_prey.append(prey)
            if prey.role in ["Primary Consumers", "Omnivores"] and role in ["Secondary Consumers", "Omnivores"]:
                possible_prey.append(prey)
            if prey.role in ["Secondary Consumers", "Omnivores"] and role in ["Tertiary Consumers", "Omnivores"]:
                possible_prey.append(prey)

        return possible_prey
    
    def roll_for_prey_location(self, possible_prey, total_population):
        success_rates = []

        for prey in possible_prey:
            # Calculate success rate based on Sensory Range, Perception, Camouflage, Stealth, and population ratio
            sensory_advantage = self.genetics['Sensory Range'] + self.genetics['Perception']
            stealth_factor = prey.genetics['Camouflage'] + prey.genetics['Stealth']
            
            # Calculate prey population as a percentage of total population
            prey_population_percentage = prey.population / total_population

            # Success rate considering sensory factors and relative population
            success_rate = max(0, sensory_advantage - stealth_factor) * (1 - prey_population_percentage)

            success_rates.append((prey, success_rate))

        # Find prey with highest success rate
        chosen_prey = max(success_rates, key=lambda x: x[1])[0]

        return chosen_prey

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
        predation_potential = sum([predator[trait] * weight for trait, weight in predation_success_factors.items()])
        # Adjust for the predator's toxin resistance
        predation_potential -= predator.get("Toxin Resistance", 0) * predation_success_factors["Toxin Resistance"]

        # Calculate food's defense potential based on its traits
        food_defense = sum([food[trait] * weight for trait, weight in food_defense_factors.items()])
        # Adjust for the food's toxin resistance
        food_defense -= food.get("Toxin Resistance", 0) * food_defense_factors["Toxin Resistance"]

        # Determine the overall success rate
        success_rate = predation_potential / (predation_potential + food_defense)

        # Roll for consumption success
        return random.random() < success_rate

    def consume(self, predator, prey):
        # Handle consumption of prey
        health_percentage = (prey.genetics['Mass']/100.0 * HEALTH_CONSUMPTION_FACTOR)
        consumed = prey.health * health_percentage
        # more efficient predators consume more
        predator.health += consumed / (predator.genetics['Resource Utilization']/100.0)
        prey.health -= consumed
        prey.population -= 1

    def consume_decomposing_matter(self):
        # Handle consumption of dead organisms -- calculate how much dead mass the scavenger should consume
        pass

    def pollinate(self, pollinator):
        # Handle pollination of plants -- pollinators should increase health of plants
        pass

    def parasitic_interaction(self, parasite):
        # Handle parasitic interaction with host
        pass

    def update_health(self, health):
        self.health += health

class EvolutionarySimulation:
    def __init__(self, planet_type, biome_type):
        # Create the ecology model
        self.ecology = SpeciesGenerator(planet_type)
        self.life = Lifeform()
        self.biome_type = biome_type
        self.total_population = 0
        self.dead_mass = 0 # for scavengers and decomposers

        # Setup initial evolutionary stage
        self.evolutionary_stage_idx = 0
        self.final_evolutionary_stage_idx = 4
        self.evolutionary_stage = list(self.evolutionary_probability.keys())[self.evolutionary_stage_idx]
        
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
            'Season': 0.5
        }  # Dictionary to store environmental conditions
        self.current_epoch = 0
        self.total_epochs = 0 # point at which to evolve to next stage

        # Genetic Algorithm Parameters
        self.mutation_rate = 0.01
        self.selection_criteria = {}  # Criteria for natural selection
        self.reproduction_rate = 0.1

        # Timescales
        self.epoch_duration = 100  # Example duration in arbitrary units

    environmental_effects = [
        # Temperature Impact
        lambda self, lifeform: lifeform.update_health(-abs(self.temperature - 20) * (1 - lifeform.traits["Thermal Resistance"] / 100)),

        # Gravity Impact on strength and endurance
        lambda self, lifeform: lifeform.update_health(-abs(self.gravity - 9.81) * (1 - (lifeform.traits["Strength"] + lifeform.traits["Endurance"]) / 200)),

        # Gravity Impact on height and mass
        lambda lifeform, gravity: lifeform.update_health(
            ((9.81 - gravity) * lifeform.traits["Height"] / 100) +
            ((9.81 - gravity) * lifeform.traits["Mass"] / 100)
        ),

        # Atmosphere Thickness Impact
        lambda self, lifeform: lifeform.update_health(-abs(self.atmosphere_thickness - 1) * (1 - lifeform.traits["Oxygen Utilization Efficiency"] / 100)),

        # Water Coverage Impact
        lambda self, lifeform: lifeform.update_health(self.water_coverage * lifeform.traits["Aquatic Adaptation"] / 100),

        # Radiation Impact
        lambda self, lifeform: lifeform.update_health(-self.radiation * (1 - lifeform.traits["Radiation Resistance"] / 100)),

        # Photosynthetic Ability Impact (for flora)
        lambda self, lifeform: lifeform.update_health(self.uv_index * lifeform.traits["Photosynthetic Ability"] / 100) if lifeform.type == "Flora" else 0,

        # UV Index Impact
        lambda self, lifeform: lifeform.update_health(-self.uv_index * (1 - lifeform.traits["Regeneration"] / 100)),

        # # Weather Patterns and Seasons Impact
        # lambda lifeform, weather_pattern: lifeform.update_health(-abs(weather_pattern - 0.5) * (1 - lifeform.traits["Adaptability"] / 100)),
    ]

    def run(self):
        # Example usage
        self.create_initial_lifeforms(initial_population=50)
        self.run_simulation(total_epochs=100)
        results = self.collect_data()
        print(results)
        return results
    
    def primordial_biome_prefix(self):
        ## First we generate initial species -- primordial single-celled organisms
        if self.biome_type in ["Forest", "Desert", "Ocean", "Tundra", "Grassland", "Wetlands", "Savanna", "Taiga", "Chaparral", "Temperate Deciduous Forest", "Temperate Rainforest", "Mediterranean", "Montane (Alpine)", "Coral Reefs", "Mangroves"]:
            return np.random.choice(['Primordial', 'Alien Primordial', 'Prebiotic'])
        else:
            return 'Alien Primordial'

    def create_initial_lifeforms(self, lifeforms, initial_population):
        # Initial lifeform are generated from probability engine
        self.lifeforms = lifeforms
        prefix = self.primordial_biome_prefix()
        species = []
        for lifeform in self.lifeforms:
            real_biome = prefix + ' ' + self.biome_type
            generative_data = self.ecology.generate(real_biome, evolutionary_stage=self.evolutionary_stage, life_form_class=lifeform['Biological'])
            lifeform.update(generative_data)
            ### TODO: Better way to generate intial population
            lifeform['Population'] = initial_population
            self.total_population += initial_population
            new_species = Species(lifeform)
            species.append(new_species)

        return species

    def mutate_lifeforms(self):
        # Apply genetic mutations to lifeforms
        for lifeform in self.lifeforms:
            lifeform.mutate(self.mutation_rate)

    def environmental_interaction(self):
        for lifeform in self.lifeforms:
        # Simulate environmental interaction with lifeforms
            for effect in self.environmental_effects:
                effect(self, lifeform)

    def predation_consumption_loop(self):
        for lifeform in self.lifeforms:
            # Simulate food chain dynamics
            if lifeform.role in ["Primary Consumers", "Secondary Consumers", "Tertiary Consumers", "Omnivores"]:
                possible_prey = lifeform.identify_food(self.lifeforms)
                chosen_prey = lifeform.roll_for_prey_location(possible_prey, self.total_population)
                if chosen_prey is None: # You fail
                    continue
                success = lifeform.roll_for_consumption(lifeform, chosen_prey)
                if not success:
                    continue # You fail
                dead_mass = self.consume(lifeform, chosen_prey)

            # Scavengers and Decomposers benefit from dead organisms
            if lifeform.role in ["Scavengers", "Decomposers", "Detritivores"]:
                self.consume_decomposing_matter(lifeform)

            # Pollinators interact with plants
            if lifeform.role == "Pollinators":
                self.pollinate(lifeform)

            # Parasites and Parasitoids impact hosts
            if lifeform.role in ["Parasites", "Parasitoids"]:
                self.parasitic_interaction(lifeform)
            
    ### TODO: Implement natural events (floods, droughts, meteor impacts etc.)
    def natural_events(self):
        pass

    def natural_selection(self):
        # Apply the selection criteria to filter lifeforms
        pass  # Implement selection logic

    def reproduce_lifeforms(self):
        # Handle reproduction of lifeforms
        pass  # Implement reproduction logic

    def update_environment(self):
        # Simulate environmental changes
        pass  # Implement environmental change logic

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

    def run_simulation(self, total_epochs):
        # Run the simulation for the specified number of epochs
        self.total_epochs = total_epochs
        for _ in range(total_epochs):
            self.run_epoch()

    def collect_data(self):
        # Collect and return data from the simulation
        return {
            "lifeforms": self.lifeforms,
            "environment": self.environment,
            "current_epoch": self.current_epoch
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