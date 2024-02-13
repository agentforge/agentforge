import numpy as np

## Frameworks make up a society like a genetic code
class SocialFramework():
  def __init__(self) -> None:
    self.dimension_values = {}
    self.state_values = {}
    
    # controls the progress of state_values
    self.progress = 0.0

    for dim in self.dimensions.keys():
      self.dimension_values[dim] = round(np.random.uniform(0, 1), 2)
    for state in self.states.keys():
      self.state_values[state] = 0

  def get_state_value(self, state: str) -> dict:
    return self.state_values[state]

  def get_dimension_value(self, dimension: str) -> float:
    return self.dimension_values[dimension]

  def values(self) -> dict:
    return list(self.dimension_values.values()) + list(self.state_values.values())

  def research(self, value: float) -> None:
    for dimension in self.state_values.keys():
      self.state_values[dimension] += value

  def __str__(self) -> str:
    state_vals = {}
    for state in self.states.keys():
      state_vals[state] = self.states[state][int(self.state_values[state] * (len(self.states[state]) - 1))]["name"]
    return str(state_vals) + "\n" + str(self.dimension_values)    
