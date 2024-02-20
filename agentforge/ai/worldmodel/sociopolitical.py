import json, os
import numpy as np
from agentforge.ai.worldmodel.socialframework import SocialFramework

### The Sociopolitical class describes the sociopolitical framework of a society
class SocioPoliticalFramework(SocialFramework):
  def __init__(self) -> None:
    super().__init__()

  def setup_values(self, value_framework):
    for value, mods in value_framework.sociopolitical_mods.items():
      if value_framework.has(value):
        for mod, value in mods:
          self.dimension_values[mod] += value
          self.dimension_values[mod] = max(min(1, self.dimension_values[mod]), 0)

  def military_focus(self) -> float:
    return (self.get_dimension_value("Militaristic") + self.get_dimension_value("Compulsory Military Service")) / 2.0
  
  def diplomacy_focus(self) -> float:
    return (self.get_dimension_value("Diplomatic") + self.get_dimension_value("Global Solidarity")) / 2.0
  
  def federalism_focus(self) -> float:
    return (self.get_dimension_value("Centralization") + self.get_dimension_value("Participatory Governance")) / 2.0
  
  def state_economic_focus(self) -> float:
    return (self.get_dimension_value("Economic Control") + self.get_dimension_value("State Intervention")) / 2.0
  
  def social_focus(self) -> float:
    return (self.get_dimension_value("Social Welfare") + self.get_dimension_value("Egalitarianism")) / 2.0
  
  def rights_focus(self) -> float:
    return (self.get_dimension_value("Rights") + self.get_dimension_value("Privacy") + self.get_dimension_value("Rule of Law") + self.get_dimension_value("Freedom of Assembly") + self.get_dimension_value("Press Freedom")) / 4.0

  def security_focus(self) -> float:
    return (self.get_dimension_value("Security") + self.get_dimension_value("Nationalism")) / 2.0
  
  def political_focus(self) -> float:
    return (self.get_dimension_value("Political Freedom") + self.get_dimension_value("Democracy") + self.get_dimension_value("Civic Participation")) / 3.0
  
  def technological_focus(self) -> float:
    return (self.get_dimension_value("Technological Integration") + self.get_dimension_value("Innovation and Research")) / 2.0
  
  # the opposite of feudalism_focus
  def classless_focus(self) -> float:
    return (self.get_dimension_value("Class Stratification") + self.get_dimension_value("Social Mobility")) / 2.0
  
  def feudalism_focus(self) -> float:
    return (1-self.classless_focus())
  
  def worker_control_focus(self) -> float:
    return (self.get_dimension_value("Worker Self-Management") + self.get_dimension_value("Collective Ownership")) / 2.0

  @staticmethod
  def align_dimensions(dim1, dim2):
      """Align two sets of dimensions, returning arrays of matched dimensions."""
      common_keys = set(dim1.keys()) & set(dim2.keys())
      dim1_aligned = np.array([dim1[key] for key in common_keys])
      dim2_aligned = np.array([dim2[key] for key in common_keys])
      return dim1_aligned, dim2_aligned

  def calculate_alliance_factor(self, other):
      contributing_factors = ['Diplomatic', 'Global Solidarity', 'Environmental Sustainability', 'Open Borders', 'Religious Tolerance', 'Information Freedom', 'Political Freedom', 'Social Welfare']
      detracting_factors = ['Nationalism', 'Militaristic', 'Isolationism']

      # Extract and align dimensions for contributing and detracting factors
      contrib_dim1, contrib_dim2 = self.align_dimensions({k: self.dimension_values[k] for k in contributing_factors if k in self.dimension_values},
                                                          {k: other.dimension_values[k] for k in contributing_factors if k in other.dimension_values})
      
      detract_dim1, detract_dim2 = self.align_dimensions({k: self.dimension_values[k] for k in detracting_factors if k in self.dimension_values},
                                                          {k: other.dimension_values[k] for k in detracting_factors if k in other.dimension_values})

      # Calculate the base similarity and detracting factor using NumPy operations
      if contrib_dim1.size > 0:  # Ensure arrays are not empty
          base_similarity = np.mean(1 - np.abs(contrib_dim1 - contrib_dim2))
      else:
          base_similarity = 0

      if detract_dim1.size > 0:
          detracting_factor = np.mean(np.abs(detract_dim1 - detract_dim2))
      else:
          detracting_factor = 0

      adjusted_similarity = base_similarity - detracting_factor * 0.5

      # Final alliance factor calculation
      return adjusted_similarity
  
   
  def calculate_war_potential(self, other, wealth, war_weariness, other_wealth, other_war_weariness):
      """Calculate the war potential against another society."""
      # Simplified formula considering directly relevant factors
      self_potential = (self.dimension_values['Militaristic'] + self.dimension_values['Technological Integration'] +
                        wealth - war_weariness + (self.dimension_values['Compulsory Military Service'] * 0.5))
      other_potential = (other.dimension_values['Militaristic'] + other.dimension_values['Technological Integration'] +
                          other_wealth - other_war_weariness + (other.dimension_values['Compulsory Military Service'] * 0.5))
      
      # Adjusting for diplomatic stance and potential alliances
      diplomatic_adjustment = self.dimension_values['Diplomatic'] - other.dimension_values['Diplomatic']

      # Calculating the net war potential difference
      net_war_potential = self_potential - other_potential + diplomatic_adjustment
      
      return net_war_potential

  states = json.load(open(os.environ.get("WORLDGEN_DATA_DIR", "./") + "sociopolitical_states.json"))

  dimensions = {
    "Rights": [0,1],
    "Security": [0,1],
    "Rule of Law": [0,1],
    "Gender Equality": [0,1],
    "Religious Tolerance": [0,1],
    "Political Freedom": [0,1],
    "Social Welfare": [0,1],
    "Social Mobility": [0,1],
    "Centralization": [0,1],
    "Democracy": [0,1],
    "Environmental Sustainability": [0,1],
    "Information Freedom": [0,1],
    "Privacy": [0,1],
    "Urbanization": [0,1],
    "Civic Participation": [0,1],
    "Diplomatic": [0,1],
    "Isolationism": [0,1],
    "Nationalism": [0,1],
    "Militaristic": [0,1],
    "Open Borders": [0,1],
    "Property Ownership": [0,1],
    "Freedom of Assembly": [0,1],
    "Press Freedom": [0,1],
    "Perception of Threat": [0,1], # Reflects the perception of external and internal threats: 0 for minimal perceived threat and 1 for significant perceived threat -- leads to higher paranoia and intelligence apparatus
    "Innovation and Research": [0,1], # Reflects the emphasis on and support for innovation and research: 0 for minimal support and 1 for significant investment and encouragement.
    "State Religion": [0,1],
    "Compulsory Military Service": [0,1],
    "Egalitarianism": [0,1], # Indicates a commitment to egalitarian principles: 0 for societies with significant class distinctions and 1 for those striving towards equality across various dimensions (beyond gender equality).
    "Class Stratification": [0,1], # Measures the presence and impact of social class divisions: 0 for rigid class systems and 1 for societies with minimal or no class stratification.
    "Technological Integration": [0,1],
    "Collective Ownership": [0,1], # Reflects the degree to which property and productive assets are owned collectively or by the state.
    "Worker Self-Management": [0,1], # Indicates the degree to which workers directly control the means of production.
    "Merit-based Advancement": [0,1], # Reflects the degree to which advancement is based on merit, skill, and achievement.
    "Public Commons": [0,1], # Extent to which resources are managed as public commons rather than private property.
    "Historical Continuity": [0,1], # The extent to which governance structures are rooted in historical and traditional precedents.
    "Ideological Enforcement": [0,1], # The extent to which governments enforce a particular ideology or set of beliefs.
    "Participatory Governance": [0,1], # Emphasizes direct participation of citizens in decision-making processes.
    "Sustainability Focus": [0,1], # A focus on sustainable living and ecological balance.
    "Global Solidarity": [0,1] # The extent to which a society or government works with others globally.
  }