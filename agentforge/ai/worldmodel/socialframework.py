import numpy as np
import random

## Frameworks make up a society like a genetic code
class SocialFramework():
  def __init__(self, mods = {}) -> None:
    self.dimension_values = {}
    self.state_values = {}
    
    # controls the progress of state_values
    self.progress = 0.0

    for dim in self.dimensions.keys():
      self.dimension_values[dim] = round(np.random.uniform(0, 1), 2)
    for state in self.states.keys():
      self.state_values[state] = 0

  def serialize(self) -> dict:
    return {
      "dimension_values": self.dimension_values,
      "state_values": self.state_values
    }
  
  # Returns the dimensions that are mostly high or low
  def define_dimensions(self, n=None) -> None:
    high_dimensions = [k for k,v in self.dimension_values.items() if v > 0.75]
    low_dimensions = [k for k,v in self.dimension_values.items() if v < 0.25]
    if n:
      if n > len(high_dimensions):
        n = len(high_dimensions)
      # sort the dimensions by highest to lowest and take top n
      high_dimensions = sorted(high_dimensions, key=lambda x: self.dimension_values[x], reverse=True)[:n]
      low_dimensions = sorted(low_dimensions, key=lambda x: self.dimension_values[x])[:n]
    return high_dimensions, low_dimensions

  @classmethod
  def deserialize(cls, data: dict):
    instance = cls()
    instance.dimension_values = data["dimension_values"]
    instance.state_values = data["state_values"]
    return instance

  def get_progress(self) -> float:
    return sum(self.state_values.values()) / len(self.state_values)

  def get_state_value(self, state: str) -> dict:
    return self.state_values[state]

  def get_dimension_value(self, dimension: str) -> float:
    return self.dimension_values[dimension]

  def values(self) -> dict:
    return list(self.dimension_values.values()) + list(self.state_values.values())
  
  def calculate_similarity(self, other):
      """Calculate similarity based on sociological dimensions between self and another society."""
      dimensions = list(self.dimension_values.keys())
      similarity = sum([1 - abs(self.dimension_values[dim] - other.dimension_values[dim]) for dim in dimensions]) / len(dimensions)
      return similarity

  def research(self, value: float) -> None:
    key = random.choice(list(self.state_values.keys()))
    self.state_values[key] += value
    self.state_values[key] = min(1, self.state_values[key])
    return key

  def mutate(self, dimension: str, value: float) -> None:
    self.dimension_values[dimension] += value
    self.dimension_values[dimension] = min(1, self.dimension_values[dimension])
    self.dimension_values[dimension] = max(0, self.dimension_values[dimension])

  def __str__(self) -> str:
    state_vals = {}
    for state in self.states.keys():
      state_vals[state] = self.states[state][int(self.state_values[state] * (len(self.states[state]) - 1))]["name"]
    return str(state_vals) + "\n" + str(self.dimension_values)    
