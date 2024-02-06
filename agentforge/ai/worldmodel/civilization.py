from agentforge.interfaces import interface_interactor
from agentforge.ai.worldmodel.society import SociologicalGroup
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import gym
from agentforge.ai.worldmodel.species import Species
from gym import spaces
import numpy as np

NUM_GROUPS_AT_START = 10

### Encompasses sociological groups coordinated by an RL Agent that plays
### a game of society management through self-play to determine
### the sociological history of this planet and historical events
class Civilization(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self) -> None:
    super(Civilization, self).__init__()    
    self.societies = []
    self.society_idx = 0
    self.action_space = spaces.Discrete(6)  # Define your actions here
    self.observation_space = spaces.Box(low=0, high=1, shape=(7,), dtype=np.float32)  # Define your state space here

    # Initialize state and other necessary variables
    self.reset()

  def step(self, action):
      # Implement action logic, state transition, and reward calculation
      # Example: self.state, reward, done, info = self.transition(action)
      society = self.societies[self.society_idx]
      society.run_epoch(action)
      
      reward = self.calculate_reward()
      done = False
      if len(self.societies) == 1: # We have a winner
          done = True
      self.sosciety_idx += 1
      if self.society_idx >= len(self.societies):
          self.society_idx = 0
      return self.state, reward, done, {}

  def reset(self):
      # Reset the environment state
      self.state = self.get_state()  # Example initialization
      return self.state

  def render(self, mode='human', close=False):
      # Optional: Implement rendering for visualization if needed
      pass

  def calculate_reward(self):
      # Implement your custom reward function
      return np.random.rand()  # Placeholder reward calculation

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
  def runner(cls, species_id="472180b0-6dd3-4294-986b-a6aaaa33f967"):
      # Get DB interface
      db = interface_interactor.get_interface("db")
      
      # Set the environment and civilization
      civ = Civilization()
      species = Species.load(db, "species", species_id)
      civ.create(species)

      # Vectorize the environment
      env = make_vec_env(lambda: civ, n_envs=4)

      # Run the civilization
      model = PPO("MlpPolicy", env, verbose=1)
      model.learn(total_timesteps=20000)

      # Save the trained model
      model.save("civilization-{}".format(species_id))
      
      # print(society.sociopolitical)
      # print(society.economy)
      # print(society.values.values)
      # print(fitness)
      # print(society)