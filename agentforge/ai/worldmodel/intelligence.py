import gym
from gym import spaces
import numpy as np

# A simple RL Agent for developing realistic pre-warp societies
class PreWarpAgentTrainer(gym.Env):
    def __init__(self):

        super(PreWarpAgentTrainer, self).__init__()
        # Define action space (6 actions)
        # 0: build, 1: create, 2: gather, 3: war, 4: trade, 5: rest, 6: research, 7: ally
        self.action_space = spaces.Discrete(6)

        # Define observation space
        self.observation_space = spaces.Box(low=0, high=100, shape=(7,), dtype=np.float32)

        # [corruption, happiness, disease, housing, forums, artifacts, food_surplus]
        self.state = np.array([0, 50, 0, 50, 0, 0, 50])
        self.reset()

    def step(self, action):
        done = False
        info = {}
        
        # Ensure state bounds are maintained
        self.state = np.clip(self.state, self.observation_space.low, self.observation_space.high)

        reward = 0
        
        return self.state, reward, done, info
    
    def reset(self):
        # Reset the state to initial conditions
        self.state = np.array([0, 50, 0, 50, 0, 0, 50])
        return self.state
    
    def render(self, mode='human'):
        # For simplicity, just print the state
        print(f"State: {self.state}")
    
    def close(self):
        pass

    # Train the model
    @classmethod
    def train(cls, iterations: int = 10000, model_name: str = "society_management_model"):
        from stable_baselines3 import PPO
        from stable_baselines3.common.env_util import make_vec_env

        # Initialize the environment
        env = make_vec_env(lambda: PreWarpAgentTrainer(), n_envs=1)

        # Initialize the model
        model = PPO("MlpPolicy", env, verbose=1)

        # Train the model
        model.learn(total_timesteps=iterations)

        # Save the model
        model.save(model_name)