from agentforge.interfaces import interface_interactor
from agentforge.ai.worldmodel.society import SociologicalGroup
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from gymnasium import spaces
import gymnasium as gym
from agentforge.ai.worldmodel.species import Species
import numpy as np
from agentforge.utils import logger

NUM_GROUPS_AT_START = 10

class CivilizationRunner():
  def __init__(self, species_ids=[]):
      self.species_ids = species_ids

  def make_env(self):
      # Get DB interface and get species
      db = interface_interactor.get_interface("db")
      species_id = self.species_ids.pop()
      species = Species.load(db, "species", species_id)
      
      # Set the environment and civilization
      return Civilization(species)

### Encompasses sociological groups coordinated by an RL Agent that plays
### a game of society management through self-play to determine
### the sociological history of this planet and historical events
class Civilization(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self, species=None) -> None:
    super(Civilization, self).__init__()    
    self.societies = []
    self.society_idx = 0
    self.action_space = spaces.Discrete(6)  # Define your actions here
    self.observation_space = spaces.Box(low=0, high=1, shape=(71,), dtype=np.float32)  # Define your state space here
    if species:
        self.create(species)
        self.state = self.get_state()  # Example initialization

  def step(self, action):
    # Implement action logic, state transition, and reward calculation
    # Example: self.state, reward, done, info = self.transition(action)
    society = self.societies[self.society_idx]
    society.run_epoch(action)
    reward = self.calculate_reward()
    done = False
    truncated = False
    if len(self.societies) == 1: # We have a winner
        done = True
    if society.population <= 0:
        self.societies.remove(society)

    # Setup for the next step
    self.society_idx += 1
    if self.society_idx >= len(self.societies):
        self.society_idx = 0
    output = "{} - Happiness: {}".format(self.society_idx, self.societies[self.society_idx].happiness)
    logger.info(output)
    return self.state, reward, done, truncated, {}

  def reset(self, seed=None):
    # Reset the environment state
    self.state = self.get_state()  # Example initialization
    return self.state, {}

  def render(self, mode='human', close=False):
      # Optional: Implement rendering for visualization if needed
      output = "{} - Happiness: {}".format(self.society_idx, self.societies[self.society_idx].happiness)
      logger.info(output)

  def calculate_reward(self):
      # Implement your custom reward function
      return self.societies[self.society_idx].fitness()

  # Gets the current observable state for the current society the RL Agent is managing
  def get_state(self):
      return self.societies[self.society_idx].observe()

  # Create randomized sociological groups based on an apex species Species class
  def create(self, apex_species):
      # Identify the apex species in the ecosystem
      for i in range(NUM_GROUPS_AT_START):
          society = SociologicalGroup(apex_species.population/NUM_GROUPS_AT_START, apex_species)
          self.societies.append(society)

  @classmethod
  def run(cls, species_ids=["a104d248-3df1-49ac-ae15-543e8e01168f"]):
      # Get DB interface
      db = interface_interactor.get_interface("db")
      
      # Set the environment and civilization
      civ = CivilizationRunner(species_ids)

      # Vectorize the environment
      env = make_vec_env(civ.make_env, n_envs=len(species_ids))
      print(env)

      # Run the civilization
      model = PPO("MlpPolicy", env, verbose=1)
      model.learn(total_timesteps=20000)

      # Save the trained model
      model.save("civilization")

      for society in env.envs[0].societies:
          print(society)