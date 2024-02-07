import random
import numpy as np
from agentforge.utils import logger
from agentforge.ai.worldmodel.species import Species
from agentforge.ai.worldmodel.sociopolitical import SocioPoliticalFramework
from agentforge.ai.worldmodel.technology import TechnologicalFramework
from agentforge.ai.worldmodel.culture import CulturalFramework
from agentforge.ai.worldmodel.economics import EconomicFramework
from agentforge.ai.worldmodel.values import ValueFramework


# TODO: make dependent on tech level, cultural framework, and environmental factors
BASE_POP_RESOURCE_REQUIREMENT = 100
MIN_POP_REQUIREMENTS = 5
RESOURCE_GATHERING_MULTIPLIER = 4
BASE_HOUSE_COST = 10
BASE_CIVIC_BUILDING_COST = 30
HOUSING_LOSS_RATE = 0.1
ARTIFACT_LOSS_RATE = 0.25
FOOD_LOSS_RATE = 0.05

def linear_interpolate(X1, X2, t):
    """
    Linearly interpolates between X1 and X2 as t goes from 0 to 1.

    Parameters:
    - X1: The starting value at t=0.
    - X2: The ending value at t=1.
    - t: The interpolation parameter, ranging from 0 to 1.

    Returns:
    - The interpolated value between X1 and X2 based on t.
    """
    return X1 + (X2 - X1) * t

class SociologicalGroup:
    def __init__(self, initial_population, species: Species):
        # Identification
        self.species = species
        self.sociopolitical = SocioPoliticalFramework()
        self.technology = TechnologicalFramework()
        self.economy = EconomicFramework()
        self.culture = CulturalFramework()
        self.values = ValueFramework(species.species_data["Life Form Attributes"])

        # Resource/Economics stand-in
        self.resource_pool = 0
        self.building_queue = []

        # Societal Characteristics
        self.corruption = 0
        self.happiness = 0
        self.disease = 0
        self.housing = 0
        self.forums = 0
        self.artifacts = 0
        self.food_supply = 0
        self.resource_pool = 0

        # Social Constraints
        self.population = initial_population
        self.observe_food()

    def __str__(self):
        return f"""Society X:
            Population: {self.population}
            Happiness Total: {self.happiness}
                Food: {min(1.0, self.food_supply / (self.food_per_pop() * self.population))}
                Housing: {min(1.0, (self.housing_per_pop() * self.housing / self.population))}
                Culture: {min(1.0, self.artifacts / self.population)}
            Food Supply: {self.food_supply}
            Housing: {self.housing}
            Artifacts: {self.artifacts}
            Resources: {self.resource_pool}
            """

    def run_epoch(self, action):
        # Run the prescribed action
        self.actions[action](self)
        self.adjust_supplies()
        self.adjust_population()
        # self.mutate_society
        # self.evolve_society()
    
    ### OBSERVATIONS ###
    def observe_food(self):
        self.food_required = self.population * self.food_per_pop()
        self.food_surplus = self.food_supply - self.food_required

    def observe(self):
        # First determine the amount of resources needed based on the population
        # technology level, cohesiveness of society, and environmental factors
        self.observe_food()
        return [
            self.corruption, 
            self.happiness,
            self.disease,
            self.housing, 
            self.forums,
            self.artifacts,
            self.food_surplus
        ] + self.sociopolitical.values() + self.technology.values() + self.economy.values()

    # Return the amount of resources needed per population member
    def food_per_pop(self):
        biological_needs = self.species.get_trait("Nutritional Requirements")
        resource_utilization = self.species.get_trait("Resource Utilization")
        total_requirement = BASE_POP_RESOURCE_REQUIREMENT * biological_needs * resource_utilization
        # Value based buffs
        if self.values.has("Resource Efficiency"):
            total_requirement *= 0.8
        if self.values.has("Food Cultivation'"):
            total_requirement *= 0.8
        return max(MIN_POP_REQUIREMENTS, total_requirement)
    
    # Gather resources, hunter-gatherer absolute min = 0.2
    def food_gathered_per_pop(self):
        resource_acquisition_efficiency = self.economy.get_state_value("Resource Acquisition Methods")
        return BASE_POP_RESOURCE_REQUIREMENT * max(0.2, resource_acquisition_efficiency) * RESOURCE_GATHERING_MULTIPLIER
    
    def housing_per_pop(self):
        return 4 # Rough estimate for now, adjust based on cultural framework and tech

    ### ACTIONS FOR THE RL AGENT ###
    def gather_food(self):
        self.food_supply += self.population * self.food_gathered_per_pop()
    
    # Gathering resources needed, manually or through mining
    def resource_gathering(self):
        resource_acquisition_efficiency = self.economy.get_state_value("Resource Acquisition Methods")
        resources_gathered = self.population * resource_acquisition_efficiency * RESOURCE_GATHERING_MULTIPLIER
        self.resource_pool += resources_gathered

    def build(self):
        # Determine need for new infrastructure, technology, and cultural artifacts
        self.housing_needed = self.population * self.housing_per_pop()
        self.housing_to_build = max(0, self.housing_needed - self.housing)
        house_cost = self.technology.get_state_value("Engineering") * BASE_HOUSE_COST
        self.resources_needed = (self.housing_needed * house_cost)
        
        #If we have the resources and need housing, build the building
        if self.resources_needed <= self.resource_pool and self.housing_needed > self.housing:
            self.housing += self.housing_to_build
            self.resource_pool -= self.resources_needed

        # self.public_works_required = self.population * self.sociopolitical.get_dimension_value("Civic Participation") * (1 - self.sociopolitical.get_dimension_value("Centralization"))
        # self.public_works_to_build = max(0, self.public_works_required - self.forums)
        # civic_building_cost = self.technology.get_state_value("Engineering") * BASE_CIVIC_BUILDING_COST
        # self.resources_needed += (self.public_works_required * civic_building_cost)

    def create(self):
        self.artifacts += self.population * self.culture.get_dimension_value("Creativity")

    def interact(self):
        # Determine the type of interaction based on governance system and external relations

        # Plan for interactions with other societies, including trade, conflict, and alliances, decide what action to take

        # Take action and determine the outcome of the interaction
        pass

    def rest(self):
        # Determine the type of rest and cultural activities based on sociopolitical framework and cultural values

        # Engage in cultural activities and rest, update happiness and health metrics
        pass

    actions = {
        0: gather_food,
        1: resource_gathering,
        2: build,
        3: create,
        4: interact,
        5: rest
    }

    def fitness(self):
        return self.population_happiness()
        # Score civilization based on health, happiness, technological proficiency, and environmental impact
    
    ### POP LEVEL FUNCTIONALITY
    def population_happiness(self):
        # happiness is based on having adequate food, housing, and cultural artifacts
        food_happiness = min(1.0, self.food_supply / (self.food_per_pop() * self.population))
        housing_happiness = min(1.0, self.housing_per_pop() * self.housing / self.population)
        artifact_happiness = min(1.0, self.artifacts / self.population)

        new_happiness = (food_happiness + housing_happiness + artifact_happiness) / 3

        # Return delta of happiness as reward
        happiness_change = new_happiness - self.happiness
        self.happiness = new_happiness

        return max(0, happiness_change)

        # happiness is boosted by rest+cultural activities
        # festival_importance = self.culture.get_dimension_value("Ritual Importance")

    def adjust_supplies(self):
         # Food is consumed
        self.food_supply -= self.population * self.food_per_pop()
        self.food_supply -= self.food_supply * FOOD_LOSS_RATE
        self.food_supply = max(0, self.food_supply)

        # Housing and artifacts degrade over time
        self.housing -= self.housing * HOUSING_LOSS_RATE
        self.artifacts -= self.artifacts * ARTIFACT_LOSS_RATE
        self.housing = max(0, self.housing)
        self.artifacts = max(0, self.artifacts)

    def mutate_society(self):
        pass

    def evolve_society(self):
        pass

    # # Given a species create a sociological group
    # def create(self, evolutionary_stage):
    #     # Determining sociopolitical structure based on species characteristics
    #     self.social_stratification = self.determine_social_systems_and_values(self.species.genetic_base_line())
    #     self.governance_system = self.adjust_governance_scores(self.social_stratification)

    def adjust_population(self):
        # Birth/death rates decline over time as healthcare, education, and economic opportunities improve
        progress_total = self.sociopolitical.get_state_value("Healthcare") + self.sociopolitical.get_state_value("Education") + self.sociopolitical.get_dimension_value("Gender Equality")

        birth_rate = linear_interpolate(0.04, 0.008, progress_total / 3)
        death_rate = linear_interpolate(0.03, 0.003, progress_total / 3)

        if self.food_supply <= 0:
            death_rate *= 2.5

        self.population += int(self.population * (birth_rate - death_rate))
    
    def simulate_technological_progress(self):
        stage_innovation_rate = {
            'Foundation of Civilization - Communicative Emergence': 0.01,
            'Foundation of Civilization - Gatherer Nexus': 0.01,
            'Foundation of Civilization - Tribal Societies': 0.02,
            'Consolidation of Civilization -  Polity Synthesis': 0.03,
            'Consolidation of Civilization - Sophisticated Governance': 0.04,
            'Enlightenment of Civilization - Scientific Discovery': 0.05,
            'Industrialization of Civilization - Industrial Era': 0.06,
            'Industrialization of Civilization - Atomic Era': 0.07,
            'Information Civilization - Digital Era': 0.08,
            'Spacefaring Civilization - Homebound': 0.09,
            'Spacefaring Civilization - Multiplanetary': 0.1,
            'Interstellar Civilization': 0.11
        }

        self.technological_proficiency += stage_innovation_rate.get(self.evolutionary_stage, 0.01)
    
    def simulate_societal_interactions(self, societies):
        # Interaction effects for each governance system
        governance_interaction_effects = {
            'Democracy': 0.05,
            'Oligarchy': 0.04,
            'Monarchy': 0.04,
            'Dictatorship': 0.03,
            'Anarchy': 0.02,
            'Republic': 0.05,
            'Theocracy': 0.03,
            'Technocracy': 0.05,
            'Meritocracy': 0.05,
            'Feudal System': 0.02,
            'Empire': 0.02,
            'Federation': 0.06,
            'Confederation': 0.04,
            'Corporate State': 0.03,
            'Tribalism': 0.01,
            'Matriarchy': 0.02,
            'Patriarchy': 0.02,
            'Cyberocracy': 0.04,
            'Eco-Governance': 0.05,
            'Direct Democracy': 0.05,
            'Plutocracy': 0.02,
            'Syndicalism': 0.03
        }

        for society in societies:
            if society != self:
                # Determine interaction type based on governance and relation type
                interaction_type = self.determine_interaction_type(society)
                effect_modifier = governance_interaction_effects.get(self.governance_system, 0.03)
                
                if interaction_type == 'Cooperative':
                    # Technological and cultural exchanges
                    exchange_rate = 0.01 * effect_modifier
                    self.technological_proficiency += exchange_rate * society.technological_proficiency
                    society.technological_proficiency += exchange_rate * self.technological_proficiency
                elif interaction_type == 'Competitive' or interaction_type == 'Hostile':
                    # Determine outcome of competition or conflict
                    outcome = self.resolve_conflict(society)
                    if outcome == 'win':
                        self.technological_proficiency += 0.02 * society.technological_proficiency
                    elif outcome == 'lose':
                        society.technological_proficiency += 0.02 * self.technological_proficiency
                elif interaction_type == 'Alliance-Based':
                    # Benefits from alliances
                    alliance_effect = 0.02 * effect_modifier
                    self.technological_proficiency += alliance_effect * society.technological_proficiency
                    society.technological_proficiency += alliance_effect * self.technological_proficiency
                # Add more interactions as necessary

    def determine_interaction_type(self, other_society):
        # Simplified logic to determine interaction type based on external relations
        if self.external_relations == 'Open' and other_society.external_relations == 'Open':
            return 'Cooperative'
        elif self.external_relations == 'Aggressive' or other_society.external_relations == 'Aggressive':
            return 'Competitive'
        elif self.external_relations == 'Isolationist' or other_society.external_relations == 'Isolationist':
            return 'Isolationist'
        # Add more logic for other types
        return 'Neutral'

    def resolve_conflict(self, other_society):
        # Simplified conflict resolution logic, can be expanded with detailed mechanisms
        self_power = self.population * self.technological_proficiency
        other_power = other_society.population * other_society.technological_proficiency
        
        if self_power > other_power:
            return 'win'
        else:
            return 'lose'

    def simulate_environmental_impacts(self, environment):
        stage_environmental_impact_factor = {
            'Primitive Civilization - Hunter Gatherers': 0.8,  # Minimal impact due to low population density and sustainable practices
            'Primitive Civilization - Tribal Societies': 0.85,  # Slightly higher impact due to more permanent settlements
            'Classical Civilization - City States and Empires': 0.9,  # Growing impact from agriculture and urbanization
            'Feudal Civilization - Medieval Era': 0.92,  # Similar to classical but with some advancements in land use
            'Feudal Civilization - Renaissance': 0.94,  # Beginning of more significant environmental modifications
            'Industrial Civilization - Industrial Era': 1.2,  # Major environmental impact due to industrialization
            'Industrial Civilization - Atomic Era': 1.1,  # High impact but begins to include some environmental awareness
            'Information Civilization - Digital Era': 1.0,  # Reduction in some types of pollution but still significant consumption and waste
            'Spacefaring Civilization - Homebound': 0.8,  # Advanced technologies allow for more sustainable interaction with the environment
            'Spacefaring Civilization - Multiplanetary': 0.6,  # Ability to harness resources from multiple planets reduces strain on any single environment
            'Interstellar Civilization': 0.4  # Advanced technologies and societal structures minimize environmental impact
        }

        impact_factor = stage_environmental_impact_factor.get(self.evolutionary_stage, 1)
        self.environmental_impact = self.population * self.resource_utilization * impact_factor
    
    def simulate_health_metrics(self):
        stage_healthcare_improvement = {
            'Primitive Civilization - Hunter Gatherers': 0.5,
            'Primitive Civilization - Tribal Societies': 1.0,
            'Classical Civilization - City States and Empires': 2.0,
            'Feudal Civilization - Medieval Era': 2.5,
            'Feudal Civilization - Renaissance': 3.0,
            'Industrial Civilization - Industrial Era': 5.0,
            'Industrial Civilization - Atomic Era': 7.0,
            'Information Civilization - Digital Era': 10.0,
            'Spacefaring Civilization - Homebound': 12.0,
            'Spacefaring Civilization - Multiplanetary': 15.0,
            'Interstellar Civilization': 20.0
        }

        improvement = stage_healthcare_improvement.get(self.evolutionary_stage, 0)
        self.life_expectancy += improvement

    def calculate_detailed_fitness(self):
        health_score = self.life_expectancy / 100
        environmental_sustainability = 1 - self.environmental_impact
        fitness = self.population * health_score * environmental_sustainability * self.technological_proficiency
        return fitness

    def determine_current_stage(self):
        # Placeholder function for determining the society's current evolutionary stage
        # This could be based on technological proficiency, population size, etc.
        return 'Primitive Civilization - Hunter Gatherers'


    def adjust_governance_scores(self, social_group):
        social_systems = social_group['social_systems']
        sociological_values = social_group['sociological_values']

        # Initialize governance scores with base probabilities
        adjusted_scores = {system: score for system, score in self.governance_systems.items()}
        
        # Adjust scores based on social systems
        for social_system, weight in social_systems.items():
            if social_system in self.social_to_governance_mapping:
                for governance_system in self.social_to_governance_mapping[social_system]:
                    if governance_system in adjusted_scores:
                        adjusted_scores[governance_system] += weight  # Adjusting score directly by weight
        
        # Further adjust scores based on sociological values
        for value in sociological_values:
            if value in self.sociological_values_to_governance_adjustments:
                adjustments = self.sociological_values_to_governance_adjustments[value]
                for governance_system, adjustment_details in adjustments.items():
                    adjustment = adjustment_details['adjustment']
                    operator = adjustment_details['operator']
                    
                    if governance_system in adjusted_scores:
                        if operator == '+':
                            adjusted_scores[governance_system] += adjustment
                        elif operator == '-':
                            adjusted_scores[governance_system] = max(0, adjusted_scores[governance_system] - adjustment)
                        elif operator == '*':
                            adjusted_scores[governance_system] *= adjustment
        
        # Normalize scores
        total_score = sum(adjusted_scores.values())
        normalized_scores = {system: score / total_score for system, score in adjusted_scores.items()}
        
        # Convert scores to probabilities
        systems, probabilities = zip(*normalized_scores.items())
        
        # Select one governance system based on adjusted and normalized probabilities
        selected_system = np.random.choice(systems, p=probabilities)
        
        return selected_system

    social_systems = {
        'Egalitarian': 0.1,
        'Class-Based': 0.2,
        'Caste-Based': 0.1,
        'Meritocratic': 0.15,
        'Plutocratic': 0.05,
        'Technocratic': 0.1,
        'Feudal': 0.2,
        'Tribal': 0.1
    }

    # Mapping from social systems to governance systems
    social_to_governance_mapping = {
        'Egalitarian': ['Democracy', 'Republic', 'Direct Democracy'],
        'Class-Based': ['Oligarchy', 'Plutocracy'],
        'Caste-Based': ['Monarchy', 'Theocracy'],
        'Meritocratic': ['Meritocracy', 'Technocracy'],
        'Plutocratic': ['Plutocracy', 'Corporate State'],
        'Technocratic': ['Technocracy', 'Cyberocracy'],
        'Feudal': ['Feudal System', 'Monarchy'],
        'Tribal': ['Tribalism', 'Anarchy']
    }
    
    relation_types = {
        'Isolationist': 0.15,
        'Cooperative': 0.25,
        'Competitive': 0.2,
        'Hostile': 0.1,
        'Alliance-Based': 0.15,
        'Dominant-Submissive': 0.15
    }

    conflict_resolution_mechanisms = {
        'Diplomacy': 0.2,
        'Legal System': 0.25,
        'Trial by Combat': 0.05,
        'Mediation': 0.2,
        'Warfare': 0.1,
        'Economic Sanctions': 0.1,
        'Social Ostracism': 0.1
    }
    
    governance_systems = {
        'Democracy': 0.15,
        'Oligarchy': 0.1,
        'Monarchy': 0.1,
        'Dictatorship': 0.1,
        'Anarchy': 0.05,
        'Republic': 0.15,
        'Theocracy': 0.1,
        'Technocracy': 0.1,
        'Meritocracy': 0.15,
        # Adding more governance systems including sci-fi concepts
        'Feudal System': 0.05, # Includes systems like the Klingon Houses
        'Empire': 0.05,
        'Federation': 0.07, # Advanced spacefaring civilizations
        'Confederation': 0.05,
        'Corporate State': 0.05, # Governance by corporate entities
        'Tribalism': 0.03, # Primitive civilizations
        'Matriarchy': 0.02,
        'Patriarchy': 0.02,
        'Cyberocracy': 0.03, # Governance through computerized/algorithmic means
        'Eco-Governance': 0.02, # Governance prioritizing ecological balance
        'Direct Democracy': 0.03, # Full participation in decision making
        'Plutocracy': 0.02, # Governance by the wealthy
        'Syndicalism': 0.02 # Governance by workers' syndicates or unions
    }