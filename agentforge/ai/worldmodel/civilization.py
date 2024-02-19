from agentforge.interfaces import interface_interactor
from agentforge.ai.worldmodel.society import SociologicalGroup
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from gymnasium import spaces
import gymnasium as gym
from agentforge.ai.worldmodel.species import Species
import numpy as np
from collections import defaultdict
from agentforge.utils import logger
from agentforge.utils.timeseries import TimeSeriesPlotterManager
from agentforge.ai.worldmodel.generator import CivilizationGenerator
import json

NUM_GROUPS_AT_START = 10

class CivilizationRunner():
  def __init__(self, species_ids=[], analysis_engine=None):
    self.species_ids = species_ids
    self.analysis_engine = analysis_engine
    self.civilization_generator = CivilizationGenerator() # for llm access

  def make_env(self):
    # Get DB interface and get species
    db = interface_interactor.get_interface("db")
    species_id = self.species_ids.pop()
    species = Species.load(db, "species", species_id)

    # Set the environment and civilization
    return Civilization(species, analysis_engine=self.analysis_engine)

### Encompasses sociological groups coordinated by an RL Agent that plays
### a game of society management through self-play to determine
### the sociological history of this planet and historical events
class Civilization(gym.Env):
    metadata = {'render.modes': ['human']}
    resource_total = 1000000000

    def __init__(self, species=None, analysis_engine=None) -> None:
        super(Civilization, self).__init__()    
        self.societies = []
        self.dead_societies = []
        self.society_idx = 0
        # TODO: Alter the environemental resources based on planet environment
        self.environment = {
            "resource_pool": self.resource_total,
            "food_supply": self.resource_total,
        }
        self.year = 0
        self.seasons = 4
        self.season = 1
        self.iterator = 0
        self.wars = []
        # Metrics and introspection
        self.action_metrics = defaultdict(int)
        self.analysis_engine = analysis_engine

        self.action_space = spaces.Discrete(9)  # Define your actions here
        self.observation_space = spaces.Box(low=0, high=1, shape=(75,), dtype=np.float32)  # Define your state space here
        if species:
            self.create(species)
            self.state = self.get_state()  # Example initialization

    # Update the counters for the year and season
    def counters(self, action):
        self.action_metrics[action] += 1
        self.iterator += 1
        if self.iterator % (self.seasons * self.num_societies) == 0: # Each society gets a turn in each season
            self.year += 1
            self.season = 1
        elif self.iterator % self.num_societies == 0:
            self.season += 1

    def step(self, action):
        # First update counters
        self.counters(action)
        # Implement action logic, state transition, and reward calculation
        # Example: self.state, reward, done, info = self.transition(action)
        if len(self.societies) == 0:
            return self.state, 0, True, False, {}

        society = self.societies[self.society_idx]
        self.environment = society.run_epoch(action, self.societies, self.year, self.season, self.environment)
        if action == 6: # war
            self.wars.append(society.last_effect)
        reward = self.societies[self.society_idx].fitness(action, self.societies, self.year, self.season)

        done = False
        truncated = False
        society_name = self.societies[self.society_idx].name
        self.analysis_engine.add("population", society_name, self.year, self.societies[self.society_idx].population)
        self.analysis_engine.add("technology", society_name, self.year, self.societies[self.society_idx].technology.get_progress())

        # Log action for this society
        self.societies[self.society_idx].action_history.add(action, reward, self.year, self.season, self.societies[self.society_idx].last_effect)

        if society.population <= 5: # a society has died out
            self.societies.remove(society)
            society.collapse = (self.year, self.season)
            self.dead_societies.append(society)

        if len(self.societies) <= 1: # We have a winner
            done = True        

        # Setup for the next step
        self.society_idx += 1
        if self.society_idx >= len(self.societies):
            self.societies = sorted(self.societies, key=lambda x: x.initiative() * np.random.random(), reverse=True)
            self.society_idx = 0
            # Replinish environmental resources
            for key, resource in self.environment.items():
                self.environment[key] = self.resource_total

        return self.state, reward, done, truncated, {}

    def reset(self, seed=None):
        # Reset the environment state
        if len(self.societies) != 0:
            self.state = self.get_state()  # Example initialization
        return self.state, {}

    def render(self, mode='human', close=False):
        # Optional: Implement rendering for visualization if needed
        #   output = "{} - Happiness: {}".format(self.society_idx, self.societies[self.society_idx].happiness)
        #   logger.info(output)
        pass

    # Gets the current observable state for the current society the RL Agent is managing
    def get_state(self):
        # Someone got wiped out -- check here in case
        if self.society_idx >= len(self.societies):
            self.society_idx = 0
        return self.societies[self.society_idx].observe()

    # Create randomized sociological groups based on an apex species Species class
    def create(self, apex_species):
        # Identify the apex species in the ecosystem
        for i in range(NUM_GROUPS_AT_START):
            society = SociologicalGroup(apex_species.population/NUM_GROUPS_AT_START, apex_species)
            self.societies.append(society)
        self.num_societies = len(self.societies)

    @classmethod
    def apex(cls, species):
        return species.get_apex_species()

    @classmethod
    def run(cls, species_ids=[]):
        # Set the environment and civilization
        analysis_engine = TimeSeriesPlotterManager(["population", "technology"])
        civ = CivilizationRunner(species_ids, analysis_engine)

        # Vectorize the environment
        env = make_vec_env(civ.make_env, n_envs=len(species_ids))
        print(env)

        # Run the civilization
        model = PPO("MlpPolicy", env, verbose=1)
        model.learn(total_timesteps=200000)

        # Save the trained model
        model.save("civilization")

        # Presentation layer
        civ.analysis_engine.show()
        logger.info(str(env.envs[0].get_wrapper_attr('action_metrics')))
        for society in env.envs[0].get_wrapper_attr('dead_societies'):
            logger.info(society)
            wars = [i for i in society.action_history.action_histories[6].effects if len(i) is not 0]
            logger.info(wars)
        for society in env.envs[0].get_wrapper_attr('societies'):
            logger.info(society)
            print(society.action_history.get_stats())
            civ.civilization_generator.generate("Terrestrial", "Forest", society.era, society.government, " ".join(society.values.values))
            # json_str = json.dumps(society.action_history.get_stats(), indent=4)
            # logger.info(json_str)

        logger.info(f"Wars: {len(env.envs[0].get_wrapper_attr('wars'))}")
        logger.info(f"Year: {env.envs[0].get_wrapper_attr('year')}")
        logger.info(f"Season: {env.envs[0].get_wrapper_attr('season')}")
      