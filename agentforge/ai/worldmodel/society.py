import random, math, humanize
import numpy as np
from agentforge.utils import logger
from agentforge.ai.worldmodel.species import Species
from agentforge.ai.worldmodel.sociopolitical import SocioPoliticalFramework
from agentforge.ai.worldmodel.technology import TechnologicalFramework
from agentforge.ai.worldmodel.culture import CulturalFramework
from agentforge.ai.worldmodel.economics import EconomicFramework
from agentforge.ai.worldmodel.values import ValueFramework
from agentforge.ai.worldmodel.designation import SocietyNamingSystem
from agentforge.ai.worldmodel.resource import Resource
from agentforge.ai.worldmodel.government import determine_governance_type
from noise import pnoise1

# TODO: make dependent on tech level, cultural framework, and environmental factors
BASE_POP_RESOURCE_REQUIREMENT = 10
MIN_POP_REQUIREMENTS = 5
RESOURCE_GATHERING_MULTIPLIER = 1
FOOD_RESOURCE_GATHERING_MULTIPLIER = 5
BASE_HOUSE_COST = 100
BASE_CIVIC_BUILDING_COST = 30
HOUSING_LOSS_RATE = 0.001
ARTIFACT_LOSS_RATE = 0.25
FOOD_LOSS_RATE = 0.05
BASE_RESEARCH_RATE = 0.001
WORKERS_PER_HOUSE = 5
STARVATION_RATE = 1.1

def gaussian(x, mu, sigma):
    """Generate a Gaussian curve for a given x, mean (mu), and standard deviation (sigma)."""
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sigma, 2.)))

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
        self.designator = SocietyNamingSystem()
        self.sociopolitical = SocioPoliticalFramework()
        self.technology = TechnologicalFramework()
        self.economy = EconomicFramework()
        self.culture = CulturalFramework()
        self.values = ValueFramework(species.species_data["Life Form Attributes"])
        self.government = determine_governance_type(self.sociopolitical.dimension_values)
        self.name = self.designator.generate_name(self.government)
        self.current_year = 0

        # Resource/Economics stand-in
        self.resources = {
            "food_supply": Resource("Food", 1000, req_per_pop=self.food_per_pop(), gather_per_pop=self.food_gathered_per_pop(), tradeable=True, consumable=True),
            "housing": Resource("Housing", 4, req_per_pop=0.25, gather_per_pop=1, consumable=True),
            "artifacts": Resource("Artifacts", 12, req_per_pop=1, gather_per_pop=1, tradeable=True, consumable=True),
            "resource_pool": Resource("Resources", 200, req_per_pop=1, gather_per_pop=1, tradeable=True)
        }
        self.forums = 0

        # Societal Characteristics
        self.corruption = 0
        self.happiness = 0
        self.disease = 0
        self.war_action = {}

        # Social Constraints and demographics
        self.population = initial_population
        self.demographics = self.generate_demographic_distribution(initial_population)

    def __str__(self):
        resource_happiness = [f"{i.name}: {i.inventory(self.population)['happiness']}" for i in self.resources.values() if i.consumable]
        resource_str = "                \n                ".join(resource_happiness)
        return f"""{self.name}:
            Population: {humanize.intword(self.population)}
            Happiness Total: {self.happiness}
                {resource_str}
            {humanize.intword(self.resources['food_supply'])}
            {humanize.intword(self.resources['housing'])}
            {humanize.intword(self.resources['artifacts'])}
            {humanize.intword(self.resources['resource_pool'])}
            Values: {self.values.values}
            Ecological Role: {self.species.role}
            Last War Action: {self.war_action}
            Technology: {self.technology.state_values}
            Sociopolitical: {self.sociopolitical.state_values}
            Demographics: {self.demographics}
            """

    def run_epoch(self, action, civs, current_year, current_season, environment):
        self.demographics = self.generate_demographic_distribution(self.population)
        self.actions[action](self, civs=civs, year=current_year, season=current_season, environment=environment)
        self.adjust_supplies()
        # Run the prescribed action
        if self.current_year != current_year:
            self.adjust_population() # birth/death
        self.migration()
        self.reset_to_zero()
        # print(self.housing)
        # self.mutate_society
        # self.evolve_society()
        self.current_year = current_year
        return environment

    # Determines order in which societies take actions
    def initiative(self):
        return (self.culture.get_dimension_value("Zealotry") + self.sociopolitical.get_dimension_value("Civic Participation") / 2.0) * np.random.rand()

    def wealth(self):
        # Wealth is based on the amount of resources and artifacts +1 to avoid division by zero
        resource_values = [i.value for i in self.resources.values() if i.tradeable]
        return sum(resource_values) + self.population + 1.0

    def observe(self):
        # First determine the amount of resources needed based on the population
        # technology level, cohesiveness of society, and environmental factors
        resources = [i.value for i in self.resources.values()]
        social_factors = [ self.corruption, self.happiness, self.disease ]
        return resources + social_factors + self.sociopolitical.values() + self.technology.values() + self.economy.values()

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
        return BASE_POP_RESOURCE_REQUIREMENT * max(0.2, resource_acquisition_efficiency) * FOOD_RESOURCE_GATHERING_MULTIPLIER
    
    def housing_per_pop(self):
        return 4 # Rough estimate for now, adjust based on cultural framework and tech

    ### RESOURCE ACTIONS FOR THE RL AGENT ###

    # Gathering food, manually or through hunting/farming -- plants/animals
    def gather_food(self, **kwargs):
        food_gathered = min(self.population * self.food_gathered_per_pop(), kwargs['environment']['food_supply'])
        self.resources['food_supply'] += food_gathered
        kwargs['environment']['food_supply'] -= food_gathered
        # print(f"FOOD SUPPLY NOW AT: {kwargs['environment']['food_supply']} and {food_gathered} gathered.")
        return kwargs['environment']
    
    # Gathering resources needed, manually or through mining --  iron/wood/stone
    def resource_gathering(self, **kwargs):
        resource_acquisition_efficiency = self.economy.get_state_value("Resource Acquisition Methods") + 0.1
        resources_gathered = min(self.population * resource_acquisition_efficiency * RESOURCE_GATHERING_MULTIPLIER, kwargs['environment']['resource_pool'])
        self.resources['resource_pool'] += resources_gathered
        kwargs['environment']['resource_pool'] -= resources_gathered
        return kwargs['environment']

    def build(self, **kwargs):
        # Determine need for new infrastructure, technology, and cultural artifacts
        cur_housing = self.resources['housing'].value
        tot_resources = self.resources['resource_pool'].value
        self.housing_needed = self.population / self.housing_per_pop()
        self.housing_to_build = max(0, self.housing_needed - cur_housing)
        # House cost increases over time based on technology
        house_cost = (self.technology.get_state_value("Engineering") + 0.001) * BASE_HOUSE_COST
        self.resources_needed = (self.housing_needed * house_cost)
        # print(f"{house_cost} <= {tot_resources} and {self.housing_needed} > {cur_housing}")
        #If we have the resources and need housing, build the building
        if house_cost <= tot_resources and self.housing_needed > cur_housing:
            houses_affordable = tot_resources / house_cost
            houses_to_build = int(self.demographics['workers'] / WORKERS_PER_HOUSE)
            # print(f"{houses_to_build} and {houses_affordable}")
            if houses_to_build > houses_affordable: # if more homes than we have resources for
                houses_to_build = houses_affordable
            # print(f"building {houses_to_build} houses for {house_cost * houses_to_build} resources.")
            self.resources['housing'] += houses_to_build
            self.resources['resource_pool'] -= house_cost * houses_to_build
            # print(f"new housing: {cur_housing} and resources: {tot_resources}")

        # TODO: Add a building system and more building types
        # self.public_works_required = self.population * self.sociopolitical.get_dimension_value("Civic Participation") * (1 - self.sociopolitical.get_dimension_value("Centralization"))
        # self.public_works_to_build = max(0, self.public_works_required - self.forums)
        # civic_building_cost = self.technology.get_state_value("Engineering") * BASE_CIVIC_BUILDING_COST
        # self.resources_needed += (self.public_works_required * civic_building_cost)

    def create(self, **kwargs):
        self.resources['artifacts'] += self.population * self.culture.get_dimension_value("Creativity")

    def research(self, **kwargs):
        # Pick a random technology to research
        tech = random.choice([self.technology, self.sociopolitical, self.economy, self.culture])
        research_rate = BASE_RESEARCH_RATE * self.species.get_trait("Intelligence") * self.demographics['scholars']
        tech.research(research_rate)

    ### DIPLOMATIC FUNCTIONS ###
    def ally(self, **kwargs):
        pass

    ### TRADING RESOURCES ###
    def trade(self, **kwargs):
        # Determine the type of trade based on economic framework and technological proficiency
        if self.demographics['merchants'] == 0:
            return
        # For each possible trade parter, determine the trade value
        best_trade_value = 0
        best_trade_partner = None
        for civ in kwargs['civs']:
            if civ == self or civ.demographics['merchants'] == 0:
                continue
            trade_value = self.calculate_trade_value(civ)
            if trade_value > best_trade_value:
                best_trade_value = trade_value
                best_trade_partner = civ
        if best_trade_partner is not None:
            self.trade_with(best_trade_partner)

    def calculate_trade_value(self, society):
        # Trade value is based on the economic framework and technological proficiency
        # TODO: Include trade ratios for artifacts
        total_value = 0.0
        for key, resource in self.resources.items():
            their_resources = society.resources[key].value
            resource_value = (resource.value + 1.0) / (their_resources + 1.0)
            total_value += resource_value
        return total_value

    def get_deficit_surplus(self, society):
        surplus_resources = []
        needed_resources = []
        for key, resource in society.resources.items():
            report = resource.inventory(society.population)
            if report["surplus"] > 0:
                surplus_resources.append(key)
            elif report["deficit"] > 0:
                needed_resources.append(key)
        return surplus_resources, needed_resources

    def trade_with(self, society):
        # TODO: Trade resources and artifacts -- first determine if we have any deficits
        our_surplus, our_needs = self.get_deficit_surplus(self)
        their_surplus, their_needs = self.get_deficit_surplus(society)
        if len(our_surplus) == 0 or len(their_needs) == 0:
            return
        # Trade the surplus resources for the needed resources
        matching_our_surplus = list(set(our_surplus) & set(their_needs))
        matching_our_needs = list(set(our_needs) & set(their_surplus))
        if len(matching_our_surplus) == 0 or len(matching_our_needs) == 0:
            return
        # Trade the surplus resources for the needed resources
        accepts = society.accept_trade(self, matching_our_surplus[0], matching_our_needs[0])
        if not accepts:
            return
        # If they accept, we trade the resources
        exchange_rate_good1_to_good2, exchange_rate_good2_to_good1 = self.resources[matching_our_surplus[0]].determine_trade_value(society.resources[matching_our_needs[0]], self.population, society.population)
        print(f"Exchange rates: {exchange_rate_good1_to_good2} and {exchange_rate_good2_to_good1}")
        # Trade the resources
        # We want to cover our deficit
        needs = abs(society.resources[matching_our_needs[0]].inventory(society.population)["deficit"])
        wants = self.resources[matching_our_surplus[0]].inventory(self.population)["surplus"]
        cost = round(exchange_rate_good2_to_good1 * needs,2)
        # If the cost is more expensive than they can afford, we adjust the cost and needs
        if cost > wants:
            cost = round(wants,2)
            needs = round(cost / exchange_rate_good2_to_good1, 2)
        print(f"Trading {needs} {matching_our_needs[0]} for {cost} {matching_our_surplus[0]} with {wants} available.")
        self.resources[matching_our_needs[0]] += needs
        society.resources[matching_our_needs[0]] -= needs
        self.resources[matching_our_surplus[0]] -= cost
        society.resources[matching_our_surplus[0]] += cost

    def accept_trade(self, society, our_surplus, their_needs):
        # Determine if we accept the trade based on the economic framework and technological proficiency
        # TODO: Make this specific to our relations with this society and current needs
        return True

    ### WAR ACTIONS ###
    def war(self, **kwargs):
        if self.sociopolitical.get_dimension_value("Militaristic") < 0.25:
            return # No war for pacifist societies
        possible_war_targets = []
        possible_war_probabilities = []
        for civ in kwargs['civs']:
            if civ != self and civ.population > 0:
                probability = self.calculate_war_probabilities(civ)
                if probability <= 0 or math.isnan(probability):
                    continue
                possible_war_targets.append(civ)
                possible_war_probabilities.append(self.calculate_war_probabilities(civ))
        if len(possible_war_targets) == 0:
            return
        normalized_war_probabilities = np.array(possible_war_probabilities) / np.sum(possible_war_probabilities)
        target = np.random.choice(possible_war_targets, p=normalized_war_probabilities)
        resolution = self.resolve_conflict(target)
        spoils = self.war_spoils(resolution, target)
        self.war_action = {
            "year": kwargs['year'],
            "target": target.name,
            "resolution": resolution,
            "season": kwargs["season"],
            "spoils": spoils,
        }

    def resolve_conflict(self, other_society):
        total_war_power = self.war_power() + other_society.war_power()
        if total_war_power == 0:
            return 0.5  # If both have zero war power, consider it a draw

        conflict_score = self.war_power() / total_war_power

        if abs(conflict_score - 0.5) < 0.05:
            return 0.5
        elif conflict_score > 0.5:
            return 0.5 + (conflict_score - 0.5) * 2
        else:
            return conflict_score * 2

    def war_spoils(self, resolution, other):
        report = {}
        # Get the victor
        if resolution == 0.5:
            return {"population": 0, "resources": 0, "artifacts": 0, "food": 0}
        if resolution > 0.5: # conquer
            victor = self
            loser = other
        else:
            victor = other
            loser = self

        # Base population change factor
        base_factor = 0.25 * (victor.technology.get_state_value("Warfare") + 0.1)
        
        # Adding Perlin noise based on the current time
        # The seed can be any fixed value; here we use a random value for variability
        seed = random.randint(0, 10000)
        noise_factor = pnoise1(self.current_year + seed, octaves=1, persistence=0.5, lacunarity=2.0, repeat=1024, base=0)
        
        # Adjust the base factor with Perlin noise
        pop_diff_factor = base_factor * (1 + noise_factor)  # Noise can increase or decrease the impact
        
        # Calculate the population difference
        pop = loser.demographics['military'] + (loser.demographics['workers'] / 3)
        pop_diff = math.ceil(pop * pop_diff_factor)
        loser.population -= pop_diff
        
        integrate_pops = victor.culture.get_dimension_value("Cultural Homogeneity") < 0.75 or victor.sociopolitical.get_dimension_value("Rights") < 0.25
        if integrate_pops:  # Integrate new pops or eliminate them
            victor.population += pop_diff

        report["population"] = pop_diff

        # Calculate the spoils
        for resource in ['resource_pool', 'food_supply', 'artifacts']:
            resource_diff = math.ceil(loser.resources[resource].value * 0.25 * ((victor.technology.get_state_value("Warfare")) + 0.1))
            loser.resources[resource] -= resource_diff
            victor.resources[resource] += resource_diff
            report[resource] = resource_diff
        
        return report

    def rest(self, **kwargs):
        # Determine the type of rest and cultural activities based on sociopolitical framework and cultural values

        # Engage in cultural activities and rest, update happiness and health metrics
        pass

    actions = {
        0: gather_food,
        1: resource_gathering,
        2: build,
        3: create,
        4: trade,
        5: ally,
        6: war,
        7: rest,
        8: research
    }

    def fitness(self, action, societies, year, season):
        # happiness is based on having adequate food, housing, and cultural artifacts
        happiness = [i.inventory(self.population)["happiness"] for i in self.resources.values() if i.consumable]
        war_happiness = 0.0

        # is the action a war? if so, calculate the war weariness/happiness
        if "resolution" in self.war_action and self.war_action["year"] == year and self.war_action["season"] == season:
            if self.war_action["resolution"] > 0.5:
                war_happiness = 0.1 * self.sociopolitical.get_dimension_value("Militaristic")
            else:
                war_happiness = -0.3 * (1-self.sociopolitical.get_dimension_value("Militaristic"))

        new_happiness = (sum(happiness) / len(happiness)) + war_happiness

        # Return delta of happiness as reward
        happiness_change = new_happiness - self.happiness
        self.happiness = new_happiness
        return happiness_change

        # happiness is boosted by rest+cultural activities
        # festival_importance = self.culture.get_dimension_value("Ritual Importance")

    def adjust_supplies(self):
         # Food is consumed
        self.resources['food_supply'] -= self.population * self.food_per_pop()
        self.resources['food_supply'] -= self.resources['food_supply'].value * FOOD_LOSS_RATE

        # Housing and artifacts degrade over time
        self.resources['housing'] -= HOUSING_LOSS_RATE
        self.resources['artifacts'] -= self.resources['artifacts'].value * ARTIFACT_LOSS_RATE

    def mutate_society(self):
        pass

    def evolve_society(self):
        pass

    # Determines the demographic makeup of the society

    def generate_demographic_distribution(self, population):
        """
        Generate a demographic distribution based on input metrics and total population.
        
        Args:
        - class_stratification (float): Determines the presence and number of nobility (0 to 1).
        - militaristic (float): Influence on the military population (0 to 1).
        - science_focus (float): Influence on the scholar population (0 to 1).
        - creativity (float): Influence on artisans and merchants (0 to 1).
        - development_scale (float): Overall development of the civilization (0.001 to 1).
        - population (int): Total population of the civilization.
        
        Returns:
        - dict: A dictionary with demographics as keys and absolute population numbers as values.
        """
        class_stratification = self.sociopolitical.feudalism_focus()
        militaristic = self.sociopolitical.military_focus()
        science_focus = self.sociopolitical.technological_focus()
        creativity = self.culture.get_dimension_value("Creativity") * self.sociopolitical.worker_control_focus()
        development_scale=0.1
        
        demographics = {
            'children': 0,
            'workers': 0,
            'elderly': 0,
            'unemployed': 0,
            'military': 0,
            'scholars': 0,
            'artisans': 0,
            'merchants': 0,
            'nobility': 0
        }
        
        # Base proportions in an early-stage civilization
        base_children = 0.4
        base_workers = 0.5
        base_elderly = 0.05

        # Adjust base proportions based on development scale (linear scaling)
        demographics['children'] = base_children - development_scale * 0.15
        demographics['workers'] = base_workers - development_scale * 0.1
        demographics['elderly'] = base_elderly + development_scale * 0.2
        
        # Calculate unemployed based on worker population
        demographics['unemployed'] = demographics['workers'] * 0.05
        
        # Adjustments based on militaristic, science focus, and creativity
        demographics['military'] = militaristic * 0.15
        demographics['scholars'] = science_focus * 0.1
        demographics['artisans'] = creativity * 0.1
        demographics['merchants'] = creativity * 0.08
        
        # Nobility based on class stratification
        demographics['nobility'] = class_stratification * 0.02
        
        # Convert percentages to absolute numbers based on the population
        for key in demographics:
            demographics[key] = round(demographics[key] * population)
        
        # Adjust to ensure the sum equals the total population
        total_demographics_sum = sum(demographics.values())
        difference = population - total_demographics_sum
        # Add or subtract the difference to/from the largest demographic group
        if difference != 0:
            largest_group = max(demographics, key=demographics.get)
            demographics[largest_group] += difference
        
        return demographics

    # Ensure no negative values
    def reset_to_zero(self):
        for key in self.resources:
            if self.resources[key].value < 0:
                self.resources[key].value = 0

    # # Given a species create a sociological group
    # def create(self, evolutionary_stage):
    #     # Determining sociopolitical structure based on species characteristics
    #     self.social_stratification = self.determine_social_systems_and_values(self.species.genetic_base_line())
    #     self.governance_system = self.adjust_governance_scores(self.social_stratification)

    def adjust_population(self):
        # Birth/death rates decline over time as healthcare, education, and economic opportunities improve
        progress_total = self.sociopolitical.get_state_value("Healthcare") + self.sociopolitical.get_state_value("Education") + self.sociopolitical.get_dimension_value("Gender Equality")
        progress_proportional = progress_total / 3

        # Parameters for the inverted Gaussian curve
        mu = 0.68  # Adjusted for a specific period in the timeline, around 1700 in a 2500-year timeline
        sigma = 0.01  # Spread of the dip

        # Implementing the adjustments to ensure death rate never exceeds birth rate
        # Applying the inverted Gaussian to decrease the death rate temporarily
        birth_rate_adjustment = gaussian(progress_proportional, mu, sigma) * 0.1  # Smaller magnitude of adjustment
        # Birth rate formula, ensuring it's always higher than the death rate
        death_rate = (1 / (1 + np.exp(-(progress_proportional * 2500 - 1000) / 200))) + 0.05  # Base birth rate
        # Death rate formula adjusted to be always lower than the birth rate
        birth_rate = death_rate + birth_rate_adjustment - 0.1  # Ensures death rate is lower with a buffer
        
        # Invert
        birth_rate = min(1, (1-birth_rate))  # Ensure birth rate never exceeds 1
        death_rate = (1-death_rate)
        # print(f"Birth Rate: {birth_rate} Death Rate: {death_rate}")

        if self.resources['food_supply'].value <= 0:
            missing_meals = abs(self.resources['food_supply'].value) / self.food_per_pop()
            missing_rate = min(1, missing_meals / self.population)
            death_rate *= missing_rate * STARVATION_RATE

        # Adjust down 
        birth_rate *= .025
        death_rate *= .023

        # Fertile population
        fertile_pop = self.population - (self.demographics['children'] + self.demographics['elderly'])
        new_pop = round(fertile_pop * (birth_rate - death_rate), 0)
        # print(f"new_pop: {new_pop}")
        self.population += new_pop
        # print(f"self.population: {humanize.intword(self.population)}")

    def migration(self):
        # Migration is based on the sociopolitical framework, environmental factors, and happiness
        pass

    def calculate_war_probabilities(self, society):
        # Less militaristic societies only engage in wars of necessity
        if self.sociopolitical.get_dimension_value("Militaristic") < 0.25:
            return 0

        # War probability is based on the sociopolitical framework and technological proficiency
        return society.wealth() / society.population
    
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
    
    def war_power(self):
        # Simplified war power calculation based on population and technological proficiency
        proficiency = [self.technology.get_state_value("Warfare"),
            self.sociopolitical.get_dimension_value("Militaristic"),
            self.sociopolitical.get_dimension_value("Nationalism"),
            self.sociopolitical.get_dimension_value("Egalitarianism"),
            self.sociopolitical.get_dimension_value("Participatory Governance")]
        return self.demographics['military'] * (sum(proficiency) / len(proficiency))
    
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