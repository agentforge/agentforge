import numpy as np
from agentforge.ai.worldmodel.socialframework import SocialFramework

### The Sociopolitical class describes the sociopolitical framework of a society
class SocioPoliticalFramework(SocialFramework):
  def __init__(self) -> None:
    super().__init__()

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

  states = {
    "Ethics": [
      {"name": "Instinctual Behavior and Early Social Norms", "point": 0.0},
      {"name": "Tribal Taboos and Oral Moral Codes", "point": 0.11},
      {"name": "Emergence of Religious and Philosophical Ethics", "point": 0.22},
      {"name": "Codification of Ethical Systems in Written Laws", "point": 0.33},
      {"name": "Humanism and the Questioning of Traditional Ethics", "point": 0.44},
      {"name": "Development of Secular and Human Rights Ethics", "point": 0.56},
      {"name": "Ethical Considerations of Industrial and War Ethics", "point": 0.67},
      {"name": "Expansion of Civil Rights and Environmental Ethics", "point": 0.78},
      {"name": "Ethical Debates on Technology and AI", "point": 0.89},
      {"name": "Advanced Universal Ethical Systems", "point": 1.0}
    ],
    "Healthcare": [
      {"name": "Primitive Healing Practices and Rituals", "point": 0.0},
      {"name": "Herbal Remedies and Shamanic Practices", "point": 0.11},
      {"name": "Institutionalized Medicine and Early Hospitals", "point": 0.22},
      {"name": "Development of Modern Medicine and Public Health", "point": 0.33},
      {"name": "Advancements in Surgery and Anatomical Knowledge", "point": 0.44},
      {"name": "Introduction of Sanitation and Vaccines", "point": 0.56},
      {"name": "Universal Healthcare Systems", "point": 0.67},
      {"name": "Biotechnological Innovations and Ethics", "point": 0.78},
      {"name": "Integration of Digital Health and Telemedicine", "point": 0.89},
      {"name": "Personalized Medicine and Gene Editing", "point": 1.0}
    ],
    "Education": [
      {"name": "Knowledge Transmission through Oral Traditions", "point": 0.0},
      {"name": "Oral Traditions and Apprenticeships", "point": 0.11},
      {"name": "Establishment of Formal Schools and Texts", "point": 0.22},
      {"name": "Emergence of the University and Scholar Guilds", "point": 0.33},
      {"name": "Renaissance Humanism and the Revival of Classical Knowledge", "point": 0.44},
      {"name": "Foundations of the Scientific Method and Academies", "point": 0.56},
      {"name": "Universal Public Education and Literacy", "point": 0.67},
      {"name": "Expansion of Higher Education and Research", "point": 0.78},
      {"name": "Digital Learning Platforms and Global Access", "point": 0.89},
      {"name": "AI-enhanced Knowledge Acquisition and Skills Development", "point": 1.0}
    ],
    "Social Support": [
      {"name": "Support Within Hunter-Gatherer Bands", "point": 0.0},
      {"name": "Family and Tribe-based Support Systems", "point": 0.11},
      {"name": "Community and Religious Support Networks", "point": 0.22},
      {"name": "Feudal Obligations and Charitable Alms", "point": 0.33},
      {"name": "Guilds and Mutual Aid Societies", "point": 0.44},
      {"name": "State Welfare and Social Security Systems", "point": 0.56},
      {"name": "Development of Modern Welfare States", "point": 0.67},
      {"name": "Emergence of Non-Governmental Organizations", "point": 0.78},
      {"name": "Universal Basic Income and Social Services", "point": 0.89},
      {"name": "Advanced Social Support Systems with AI Integration", "point": 1.0}
    ],
    "Diplomacy": [
      {"name": "Inter-Tribal Communications and Alliances", "point": 0.0},
      {"name": "Tribal and Familial Alliances", "point": 0.11},
      {"name": "Emergence of Diplomatic Protocols among City-States", "point": 0.22},
      {"name": "Medieval Treaties and Papal Mediation", "point": 0.33},
      {"name": "Diplomatic Missions and Resident Ambassadors", "point": 0.44},
      {"name": "Nation-State Diplomacy and International Law", "point": 0.56},
      {"name": "Colonialism, Imperialism, and Global Exploration", "point": 0.67},
      {"name": "Creation of International Organizations", "point": 0.78},
      {"name": "Global Governance and Multilateral Institutions", "point": 0.89},
      {"name": "Confederated Diplomacy across Societal Sectors", "point": 1.0}
    ],
    "Legal Systems": [
      {"name": "Pre-Legal Societal Norms and Conflict Resolution", "point": 0.0},
      {"name": "Tribal Customs and Oral Laws", "point": 0.11},
      {"name": "Codification of Laws in Early Civilizations", "point": 0.22},
      {"name": "Medieval Legal Traditions and Canon Law", "point": 0.33},
      {"name": "Development of National Legal Codes", "point": 0.44},
      {"name": "Codification and Standardization of Laws", "point": 0.56},
      {"name": "Establishment of Constitutional Democracies", "point": 0.67},
      {"name": "International Legal Standards and Human Rights", "point": 0.78},
      {"name": "Supranational Courts and Transnational Law", "point": 0.89},
      {"name": "Advanced Global Legal Frameworks", "point": 1.0}
    ]
  }

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
    "Civic Participation": [0,1],
    "Diplomatic": [0,1],
    "Isolationism": [0,1],
    "Nationalism": [0,1],
    "Militaristic": [0,1],
    "Open Borders": [0,1],
    "Property Ownership": [0,1],
    "Freedom of Assembly": [0,1],
    "Press Freedom": [0,1],
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