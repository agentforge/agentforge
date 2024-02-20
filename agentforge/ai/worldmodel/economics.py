import json, os
from agentforge.ai.worldmodel.socialframework import SocialFramework

class EconomicFramework(SocialFramework):
  def __init__(self):
    super().__init__()

  dimensions = {
    "Wealth Distribution": [0,1],  # Measures the spread of wealth across a society, from highly unequal (0) to perfectly equitable (1).
    "Trade Efficiency": [0,1],  # Measures the efficiency and effectiveness of trade and commerce within a society.
    "Autarky": [0,1], # The degree to which a society is self-sufficient and minimizes reliance on external entities.
    "Economic Control": [0,1],
    "State Intervention": [0,1], # The extent of state involvement in the economy.
    "Economic Equality": [0,1], # Reflects the degree of income and wealth equality enforced by the government.
  }

  states = json.load(open(os.environ.get("WORLDGEN_DATA_DIR", "./") + "economic_states.json"))
