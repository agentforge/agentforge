import json, os
from agentforge.ai.worldmodel.socialframework import SocialFramework

class EconomicFramework(SocialFramework):
  def __init__(self):
    super().__init__()

  dimensions = {
    "Economic Equality": [0, 1], # The degree of economic equality or inequality in a society.
    "Corporate Power": [0,1], # The extent of corporate influence and power in the economy.
    "Consumerism": [0,1], # The degree to which a society is driven by consumerism and materialism.
    "Economic Autonomy": [0, 1], # From complete dependence on external economies (0) to total self-sufficiency (1).
    "Market Mechanism": [0, 1], # From fully planned economies with no market mechanism (0) to complete market-driven economies (1).
    "Economic Planning": [0, 1], # From economies with no central planning (0) to highly centralized economic planning (1).
    "Resource Allocation Method": [0, 1], # From allocation based on status or command (0) to allocation based on market forces or community decisions (1).
    "Trade and Exchange System": [0, 1], # From barter or gift economies with no formal currency (0) to economies with complex monetary trade systems (1).
    "Capital Accumulation": [0, 1], # From economies where capital accumulation is discouraged or impossible (0) to economies focused on maximizing capital accumulation (1).
    "Economic Integration": [0, 1], # From isolated economies with little external interaction (0) to fully integrated into the global economy (1).
    "Economic Diversity": [0, 1], # From economies dependent on a narrow range of sectors (0) to highly diversified economies (1).
    "Supply Chain Resilience": [0, 1], # From economies with fragile, easily disrupted supply chains (0) to economies with robust, adaptable supply chains (1).
    "Economic Adaptability": [0, 1], # From economies resistant to change (0) to economies that are highly adaptable and responsive to economic shifts (1).
    "Monetary System": [0, 1], # From economies without a standardized monetary system (0) to those with a complex, regulated monetary system (1).
    "Commodities": [0, 1], # From economies primarily focused on subsistence or internal consumption (0) to those engaged extensively in the exchange of goods and services (1).
    "Energy Efficiency": [0, 1], # From economies with low energy efficiency and poor management (0) to those with high energy efficiency and sustainable management practices (1).
    "Information and Knowledge Dissemination": [0, 1] # From economies with restricted access to information (0) to those with open and widespread dissemination of knowledge (1).
  }

  states = json.load(open(os.environ.get("WORLDGEN_DATA_DIR", "./") + "economic_states.json"))
