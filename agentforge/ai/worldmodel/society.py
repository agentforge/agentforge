import random, math, humanize, pprint, uuid
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
from agentforge.ai.worldmodel.action import ActionHistoryManager
from agentforge.ai.worldmodel.reputation import ReputationManager
from agentforge.ai.worldmodel.war import War
from agentforge.ai.worldmodel.government import determine_governance_type
from noise import pnoise1

# TODO: make dependent on tech level, cultural framework, and environmental factors
BASE_POP_RESOURCE_REQUIREMENT = 10
MIN_POP_REQUIREMENTS = 5
RESOURCE_GATHERING_MULTIPLIER = 1
FOOD_RESOURCE_GATHERING_MULTIPLIER = 75
BASE_HOUSE_COST = 100
BASE_CIVIC_BUILDING_COST = 30
HOUSING_LOSS_RATE = 0.001
ARTIFACT_LOSS_RATE = 0.01
FOOD_LOSS_RATE = 0.05
BASE_RESEARCH_RATE = 0.00000005
WORKERS_PER_HOUSE = 5
STARVATION_RATE = 0.005
BASE_ARTIFACTS_PER_ARTISAN = 2.0

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
    def __init__(self, initial_population, species: Species, id=None):
        if not id:
            self.uuid = str(uuid.uuid4())
        else:
            self.uuid = id
        # Identification
        self.species = species
        self.values = ValueFramework(species.species_data["Life Form Attributes"])
        self.action_history = ActionHistoryManager()
        self.sociopolitical = SocioPoliticalFramework()
        self.sociopolitical.setup_values(self.values)
        self.technology = TechnologicalFramework()
        self.economy = EconomicFramework()
        self.culture = CulturalFramework()
        self.reputation = ReputationManager()
        self.war_manager = War()
        # Store reputation with other societies

        # Societal Characteristics
        self.corruption = 0
        self.happiness = 0
        self.disease = 0
        self.missing_meals = 0
        self.starvation_event = {}
        self.civ_info = {}

        # Social Constraints and demographics
        self.population = initial_population
        self.era = 'Prehistoric'
        self.collapse = None
        self.year = 0

    def initialize(self, initial_population):
        self.demographics = self.generate_demographic_distribution(initial_population)
        self.government = determine_governance_type(self.sociopolitical.dimension_values, 'Prehistoric') # Start at hunter-gatherer level
        self.designator = SocietyNamingSystem()
        self.name = self.designator.generate_name()
        # Resource/Economics stand-in
        self.resources = {
            "food_supply": Resource("Food", 1000, req_per_pop=self.food_per_pop(), gather_per_pop=self.food_gathered_per_pop(), tradeable=True, consumable=True),
            "housing": Resource("Housing", 4, req_per_pop=0.25, gather_per_pop=1, consumable=True),
            "artifacts": Resource("Artifacts", 12, req_per_pop=1, gather_per_pop=1, tradeable=True, consumable=True),
            "resource_pool": Resource("Resources", 200, req_per_pop=1, gather_per_pop=1, tradeable=True)
        }

    def serialize(self):
        # Convert the object's state to a serializable dictionary
        return {
            "id": self.uuid,
            "species": self.species.uuid,
            "values": self.values.serialize(),
            "sociopolitical": self.sociopolitical.serialize(),
            "technology": self.technology.serialize(),
            "economy": self.economy.serialize(),
            "culture": self.culture.serialize(),
            "reputation": self.reputation.serialize(),
            "war_manager": self.war_manager.serialize(),
            "government": self.government,
            "era": self.era,
            "name": self.name,
            "collapse": self.collapse,
            "year": self.year,
            "resources": {k: v.serialize() for k, v in self.resources.items()},
            "corruption": self.corruption,
            "happiness": self.happiness,
            "disease": self.disease,
            "missing_meals": self.missing_meals,
            "starvation_event": self.starvation_event,
            "population": self.population,
            "demographics": self.demographics,
            "civ_info": self.civ_info
        }

    def save(self, db, collection):
        species_dict = self.serialize()
        db.set(collection, self.uuid, species_dict)

    @classmethod
    def load(cls, db, collection, uuid, society_dict=None):
        if society_dict is None:
            society_dict = db.get(collection, uuid)
            if society_dict is None:
                return None

        # Deserialize the Species object
        species = Species.load(db, "species", society_dict["species"], load_individuals=False)

        # Initialize the SociologicalGroup object with basic attributes
        obj = cls(society_dict["population"], species, id=society_dict["id"])

        # Deserialize and set complex attributes
        obj.values = ValueFramework.deserialize(society_dict["values"])
        obj.action_history = ActionHistoryManager()
        obj.sociopolitical = SocioPoliticalFramework.deserialize(society_dict["sociopolitical"])
        obj.sociopolitical.setup_values(obj.values)
        obj.technology = TechnologicalFramework.deserialize(society_dict["technology"])
        obj.economy = EconomicFramework.deserialize(society_dict["economy"])
        obj.culture = CulturalFramework.deserialize(society_dict["culture"])
        obj.reputation = ReputationManager.deserialize(society_dict["reputation"])
        obj.war_manager = War.deserialize(society_dict["war_manager"])

        # Deserialize resources
        obj.resources = {k: Resource.deserialize(v) for k, v in society_dict["resources"].items()}

        # Set simple attributes
        obj.government = society_dict["government"]
        obj.era = society_dict["era"]
        obj.name = society_dict["name"]
        obj.collapse = society_dict["collapse"]
        obj.year = society_dict["year"]
        obj.corruption = society_dict["corruption"]
        obj.happiness = society_dict["happiness"]
        obj.disease = society_dict["disease"]
        obj.missing_meals = society_dict["missing_meals"]
        obj.starvation_event = society_dict["starvation_event"]
        obj.population = society_dict["population"]
        obj.demographics = society_dict["demographics"]
        obj.civ_info = society_dict["civ_info"]

        return obj

    def __str__(self):
        resource_happiness = [f"{i.name}: {i.inventory(self.population)['happiness']}" for i in self.resources.values() if i.consumable]
        resource_str = "                \n                ".join(resource_happiness)
        return f"""{self.name + " " + self.government}:
            Population: {humanize.intword(self.population)}
            Era: {self.era}
            Happiness Total: {self.happiness}
                {resource_str}
            {humanize.intword(self.resources['food_supply'])}
            Food Per Pop: {self.food_per_pop()}
            {humanize.intword(self.resources['housing'])}
            {humanize.intword(self.resources['artifacts'])}
            {humanize.intword(self.resources['resource_pool'])}
            Last War Actions: {self.action_history.get_window(6, 5)}
            Last Trade Actions: {self.action_history.get_window(4, 5)}
            Last Research Actions: {self.action_history.get_window(8, 5)}
            Starvation Event: {self.starvation_event}
            Reputation: {self.reputation.list_all_reputations()}
            Collapse: {self.collapse}
            Values: {self.values.values}
            Ecological Role: {self.species.role}
            Technology: {self.technology.state_values}
            Sociopolitical: {pprint.pformat({k: (round(v, 2) if isinstance(v, float) else v) for k, v in self.sociopolitical.dimension_values.items()})}
            Demographics: {self.demographics}
            """

    def full_name(self):
        return f"{self.name} {self.government}"

    def run_epoch(self, action, civs, current_year, current_season, environment):
        year_change = self.year != current_year
        self.year = current_year
        self.season = current_season
        self.last_effect = {}
        
        self.demographics = self.generate_demographic_distribution(self.population)
        self.actions[action](self, civs=civs, year=current_year, season=current_season, environment=environment)
        self.adjust_supplies()
        # Run the prescribed action
        if year_change:
            self.adjust_population() # birth/death
        self.migration()
        self.reset_to_zero()
        # print(self.housing)
        self.mutate_society(action)
        self.evolve_society()
        self.war_manager.tick()
        self.reputation.tick()
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
        return total_requirement
    
    # Gather resources, hunter-gatherer absolute min = 0.2
    def food_gathered_per_pop(self):
        tech_level = max(self.technology.get_state_value("Agriculture and Pastoralism"), 0.1) * BASE_POP_RESOURCE_REQUIREMENT
        return tech_level * FOOD_RESOURCE_GATHERING_MULTIPLIER
    
    def housing_per_pop(self):
        return 4 # Rough estimate for now, adjust based on cultural framework and tech

    ### RESOURCE ACTIONS FOR THE RL AGENT ###

    # Gathering food, manually or through hunting/farming -- plants/animals
    def gather_food(self, **kwargs):
        food_gathered_per_pop = self.food_gathered_per_pop()
        # Technology dictates how much of the environment we can capture
        # food_supply_capturable = kwargs['environment']['food_supply'] * max(self.technology.get_state_value("Agriculture and Pastoralism"), 0.1)
        food_gathered = self.demographics['workers'] * food_gathered_per_pop
        self.resources['food_supply'] += food_gathered
        kwargs['environment']['food_supply'] -= food_gathered
        # print(f"FOOD SUPPLY NOW AT: {kwargs['environment']['food_supply']} and {food_gathered} gathered ({food_gathered_per_pop} per pop). by {self.demographics['workers']} workers.")
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
        # Determine the need for new cultural artifacts and technology
        self.resources['artifacts'] += math.ceil(self.demographics['artisans']* BASE_ARTIFACTS_PER_ARTISAN)

    def research(self, **kwargs):
        # Pick a random technology to research
        tech = random.choice([self.technology, self.sociopolitical, self.economy, self.culture])
        research_rate = BASE_RESEARCH_RATE * self.species.get_trait("Intelligence") * self.demographics['scholars'] * self.sociopolitical.get_dimension_value("Technological Integration") * self.sociopolitical.get_dimension_value("Innovation and Research")
        name = tech.research(research_rate)
        self.last_effect = {
            "type": "research",
            "year": self.year,
            "season": kwargs["season"],
            "target": name,
            "progress": research_rate
        }

    ### DIPLOMATIC FUNCTIONS ###
    def ally(self, **kwargs):
        for civ in kwargs['civs']:
            if civ == self:
                continue
            alliance_potential = self.sociopolitical.calculate_alliance_factor(civ.sociopolitical)
            similarity = self.sociopolitical.calculate_similarity(civ.sociopolitical)
            # logger.info(f"alliance_potential: {alliance_potential} and similarity: {similarity}")
            # self.reputation.update_reputation(civ.name, "ally", 0.1)

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
            self.trade_with(best_trade_partner, season=kwargs["season"])

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
            if not resource.tradeable:
                continue
            report = resource.inventory(society.population)
            if report["surplus"] > 0:
                surplus_resources.append(key)
            elif report["deficit"] > 0:
                needed_resources.append(key)
        return surplus_resources, needed_resources

    def trade_with(self, society, **kwargs):
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
        # print(f"Exchange rates: {exchange_rate_good1_to_good2} and {exchange_rate_good2_to_good1}")
        # Trade the resources
        # We want to cover our deficit
        needs = abs(society.resources[matching_our_needs[0]].inventory(society.population)["deficit"])
        wants = self.resources[matching_our_surplus[0]].inventory(self.population)["surplus"]
        cost = round(exchange_rate_good2_to_good1 * needs,2)
        # If the cost is more expensive than they can afford, we adjust the cost and needs
        if cost > wants:
            cost = round(wants,2)
            needs = round(cost / exchange_rate_good2_to_good1, 2)
        # print(f"Trading {needs} {matching_our_needs[0]} for {cost} {matching_our_surplus[0]} with {wants} available.")
        self.resources[matching_our_needs[0]] += needs
        society.resources[matching_our_needs[0]] -= needs
        self.resources[matching_our_surplus[0]] -= cost
        society.resources[matching_our_surplus[0]] += cost
        society.reputation.update_reputation(self.name, "trade", 0.1)
        self.reputation.update_reputation(society.name, "trade", 0.1)
        self.last_effect = {
            "type": "trade",
            "year": self.year,
            "season": kwargs["season"],
            "target": society.name,
            "resources": {matching_our_surplus[0]: cost, matching_our_needs[0]: needs}
        }

    def accept_trade(self, society, our_surplus, their_needs):
        # Determine if we accept the trade based on the economic framework and technological proficiency
        # TODO: Make this specific to our relations with this society and current needs
        return True

    ### WAR ACTIONS ###
    def war(self, **kwargs):
        rand = np.random.rand() - self.war_manager.get_weariness()
        ethics = self.sociopolitical.get_state_value("Ethics")
        if rand < self.sociopolitical.get_dimension_value("Militaristic") or rand < ethics:
            return # No war today, weary troops or pacifism
        # print(f"rand: {rand} and ethics: {ethics} and weariness: {self.war_manager.get_weariness()}")
        possible_war_targets = []
        possible_war_probabilities = []
        for civ in kwargs['civs']:
            if civ != self and civ.population > 0:
                probability = self.war_manager.calculate_war_probabilities(self, civ)
                if probability <= 0 or math.isnan(probability):
                    continue
                possible_war_targets.append(civ)
                possible_war_probabilities.append(self.war_manager.calculate_war_probabilities(self, civ))
        if len(possible_war_targets) == 0:
            return
        # print(possible_war_probabilities)
        # print(self.war_manager.get_weariness())
        normalized_war_probabilities = np.array(possible_war_probabilities) / np.sum(possible_war_probabilities)
        target = np.random.choice(possible_war_targets, p=normalized_war_probabilities)
        resolution = self.resolve_conflict(target)
        # Now let's calculate the impact, weariness, and spoils of war
        spoils, victor = self.war_spoils(resolution, target)
        self.last_effect = {
            "type": "war",
            "year": kwargs['year'],
            "target": target.name,
            "resolution": resolution,
            "season": kwargs["season"],
            "spoils": spoils,
            "victor": victor.name if victor else None
        }
        # print(self.last_effect)
        impact = self.war_manager.calculate_war_impact(victor, resolution)
        # print(f"War impact: {impact} and resolution: {resolution}")
        self.war_manager.update_weariness(impact, self.sociopolitical.dimension_values, self.wealth())
        target.war_manager.update_weariness(impact, target.sociopolitical.dimension_values, target.wealth())
        target.reputation.update_reputation(self.name, "war", -0.2)

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
            return {"population": 0, "resources": 0, "artifacts": 0, "food": 0}, None
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
        noise_factor = pnoise1(self.year + seed, octaves=1, persistence=0.5, lacunarity=2.0, repeat=1024, base=0)
        
        # Adjust the base factor with Perlin noise
        pop_diff_factor = base_factor * (1 + noise_factor)  # Noise can increase or decrease the impact
        
        # Calculate the population difference
        pop = loser.demographics['military'] + (loser.demographics['workers'] / 10)
        pop_diff = math.floor(pop * pop_diff_factor)
        # print(f"pop_diff: {pop_diff} and pop_diff_factor: {pop_diff_factor} and noise_factor: {noise_factor}")
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
        
        return report, victor

    def rest(self, **kwargs):
        # Determine the type of rest and cultural activities based on sociopolitical framework and cultural values

        # Engage in cultural activities and rest, update happiness and health metrics
        pass

    def work(self, **kwargs):
        # Allow the workers to do independent labor, acquire resources, etc.
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
        8: research,
        # 9: work
    }

    def fitness(self, action, societies, year, season):
        if self.population <= 0:
            return -1
        # happiness is based on having adequate food, housing, and cultural artifacts
        happiness = [i.inventory(self.population)["happiness"] for i in self.resources.values() if i.consumable]
        happiness_boost = 0.0

        # calculate the war weariness/happiness
        if action == 6 and "resolution" in self.last_effect:
            proportion = self.demographics['military'] / self.population
            if self.last_effect["resolution"] > 0.5:
                happiness_boost += 0.8 * self.sociopolitical.get_dimension_value("Militaristic") * proportion
            else:
                happiness_boost -= 1.2 * self.sociopolitical.get_dimension_value("Militaristic") * proportion

        # calculate trade action happiness boost
        if action == 4 and "year" in self.last_effect:
            proportion = self.demographics['merchants'] / self.population
            happiness_boost += 0.5 * self.economy.get_dimension_value("Economic Equality") * proportion

        # calculate research action happiness boost
        if action == 8 and "year" in self.last_effect:
            proportion = self.demographics['scholars'] / self.population
            happiness_boost += 0.2 * self.sociopolitical.get_dimension_value("Innovation and Research") * proportion

        new_happiness = (sum(happiness) / len(happiness)) + happiness_boost

        # Return delta of happiness as reward
        happiness_change = max(0, new_happiness - self.happiness)
        self.happiness = new_happiness
        return happiness_change

        # happiness is boosted by rest+cultural activities
        # festival_importance = self.culture.get_dimension_value("Ritual Importance")

    def adjust_supplies(self):
        # Housing and artifacts degrade over time
        self.resources['housing'] -= HOUSING_LOSS_RATE
        self.resources['artifacts'] -= self.resources['artifacts'].value * ARTIFACT_LOSS_RATE

        # Food is consumed
        self.resources['food_supply'] -= self.population * self.food_per_pop()
        self.resources['food_supply'] -= self.resources['food_supply'].value * FOOD_LOSS_RATE

        if self.resources['food_supply'].value <= 0:
            self.missing_meals += abs(self.resources['food_supply'].value) / self.food_per_pop()
            self.resources['food_supply'].value = 0

    # Societal drift over time base on actions
    def mutate_society(self, action):
        if action == 0 or action == 1: # gather food, resource gathering
            # self.economy.mutate("Resource Acquisition Methods", 0.01)
            pass
        elif action == 2: # Build Housing/Infrastructure
            self.sociopolitical.mutate("Social Welfare", 0.01)
        elif action == 3: # Create
            self.sociopolitical.mutate("Social Mobility", 0.01)
            self.culture.mutate("Art & Aesthetics", 0.01)
        elif action == 4: # Trade
            self.sociopolitical.mutate("Isolationism", -0.01)
            self.economy.mutate("Economic Autonomy", -0.01)
            self.economy.mutate("Economic Integration", 0.03)
        elif action == 5: # Ally
            self.sociopolitical.mutate("Nationalism", -0.01)
            self.sociopolitical.mutate("Diplomatic", 0.01)
        elif action == 6: # War
            self.sociopolitical.mutate("Nationalism", 0.01)
            self.sociopolitical.mutate("Diplomatic", -0.01)
        elif action == 7: # Rest
            self.culture.mutate("Ritual Importance", 0.01)
        elif action == 8: # Research
            self.sociopolitical.mutate("Innovation and Research", 0.01)
        
        # Randomly mutate a value
        if np.random.rand() < 0.1:
            random_value = random.choice([self.sociopolitical, self.economy, self.culture])
            random_value.mutate(random.choice(list(random_value.dimension_values.keys())), np.random.uniform(-0.01, 0.01))

    def war_power(self):
        # Simplified war power calculation based on population and technological proficiency
        proficiency = [self.technology.get_state_value("Warfare"),
            self.sociopolitical.get_dimension_value("Militaristic"),
            self.sociopolitical.get_dimension_value("Nationalism"),
            self.sociopolitical.get_dimension_value("Egalitarianism"),
            self.sociopolitical.get_dimension_value("Participatory Governance")]
        return self.demographics['military'] * (sum(proficiency) / len(proficiency))

    # Determine if we need a government change, roll minor chance of revolution
    def evolve_society(self):
        # Get the current era based on overall progress
        era = self.get_era()
        if era != self.era:
            self.era = era
            self.government = determine_governance_type(self.sociopolitical.dimension_values, era)

    def get_era(self):
        eras = {
            (0, 0.11, "Prehistoric"),
            (0.11, 0.22, "Ancient"),
            (0.22, 0.33, "Classical"),
            (0.33, 0.44, "Medieval"),
            (0.44, 0.55, "Renaissance"),
            (0.55, 0.67, "Industrial"),
            (0.67, 0.78, "Modern"),
            (0.78, 0.89, "Post-Modern"),
            (0.89, 1.0, "Future")
        }
        progress = [tech.get_progress() for tech in [self.technology, self.sociopolitical, self.economy, self.culture]]
        progress = sum(progress) / len(progress)
        for era in eras:
            if era[0] <= progress <= era[1]:
                return era[2]

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
        worker_management_scale = self.sociopolitical.worker_control_focus()
        demographics['unemployed'] = demographics['workers'] * 0.05 * (1 - worker_management_scale)
        
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

    def adjust_population(self):
        # Birth/death rates decline over time as healthcare, education, and economic opportunities improve
        progress_total = self.sociopolitical.get_state_value("Healthcare") + self.sociopolitical.get_state_value("Education") + self.sociopolitical.get_dimension_value("Gender Equality")
        progress_proportional = progress_total / 3

        # Parameters for the inverted Gaussian curve
        mu = 0.68  # Adjusted for a specific period in the timeline, around 1700 in a 2500-year timeline
        sigma = 0.20  # Spread of the dip

        # Implementing the adjustments to ensure death rate never exceeds birth rate
        # Applying the inverted Gaussian to decrease the death rate temporarily
        birth_rate_adjustment = gaussian(progress_proportional, mu, sigma) * 0.01  # Smaller magnitude of adjustment
        # Birth rate formula, ensuring it's always higher than the death rate
        death_rate = (1 / (1 + np.exp(-(progress_proportional * 2500 - 1000) / 200))) + 0.05  # Base birth rate
        # Death rate formula adjusted to be always lower than the birth rate
        birth_rate = death_rate + birth_rate_adjustment - 0.1  # Ensures death rate is lower with a buffer
        
        # Invert
        birth_rate = min(1, (1-birth_rate))  # Ensure birth rate never exceeds 1
        death_rate = (1-death_rate)
        # print(f"Birth Rate: {birth_rate} Death Rate: {death_rate}")

        # Adjust down 
        birth_rate *= .015
        death_rate *= .013

        # Adjust for happiness
        # print(f"{birth_rate} *= max({self.happiness} + 0.1, 1.0) == {max(self.happiness + 0.1, 1.0)}")
        birth_rate *= max(self.happiness + 0.1, 1.0)

        if self.missing_meals > 0:
            missing_rate = min(1, self.missing_meals / self.population)
            death_rate = missing_rate * STARVATION_RATE
            self.starvation_event = {
                "year": self.year,
                "season": self.season,
                "missing_meals": self.missing_meals,
                "missing_rate": missing_rate,
                "death_rate": death_rate,
                "dead": math.ceil(self.population * death_rate),
                "food_supply": self.resources['food_supply'].value,
            }
            self.population -= math.ceil(self.population * death_rate)
            self.missing_meals = 0

        # Fertile population
        fertile_pop = self.population - (self.demographics['children'] + self.demographics['elderly'])
        new_pop = max(round(fertile_pop * (birth_rate - death_rate), 0), 1)
        # print(f"new_pop: {new_pop} and {fertile_pop} * ({birth_rate - death_rate})")
        self.population += new_pop
        # print(f"self.population: {humanize.intword(self.population)}")

    def migration(self):
        # Migration is based on the sociopolitical framework, environmental factors, and happiness
        pass
