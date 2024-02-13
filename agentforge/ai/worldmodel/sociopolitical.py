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
    return (self.get_dimension_value("Economic Control") + self.get_dimension_value("Economic Equality") + self.get_dimension_value("State Intervention")) / 2.0
  
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

  states = {
    "Ethics": [
      {"name": "Tribal Taboos and Oral Moral Codes", "point": 0},
      {"name": "Emergence of Religious and Philosophical Ethics", "point": 0.25},
      {"name": "Codification of Ethical Systems in Written Laws", "point": 0.5},
      {"name": "Development of Secular and Human Rights Ethics", "point": 0.75},
      {"name": "Advanced Universal Ethical Systems", "point": 1}
    ],
    "Healthcare": [
      {"name": "Herbal Remedies and Shamanic Practices", "point": 0},
      {"name": "Institutionalized Medicine and Early Hospitals", "point": 0.25},
      {"name": "Development of Modern Medicine and Public Health", "point": 0.5},
      {"name": "Universal Healthcare Systems", "point": 0.75},
      {"name": "Personalized Medicine and AI-enhanced Healthcare", "point": 1}
    ],
    "Education": [
      {"name": "Oral Traditions and Apprenticeships", "point": 0},
      {"name": "Establishment of Formal Schools and Texts", "point": 0.25},
      {"name": "Universal Public Education and Literacy", "point": 0.5},
      {"name": "Digital Learning Platforms and Global Access to Education", "point": 0.75},
      {"name": "AI-enhanced Knowledge Acquisition and Skills Development", "point": 1}
    ],
    "Social Support": [
      {"name": "Family and Tribe-based Support Systems", "point": 0},
      {"name": "Community and Religious Support Networks", "point": 0.25},
      {"name": "State Welfare and Social Security Systems", "point": 0.5},
      {"name": "Universal Basic Income and Social Services", "point": 0.75},
      {"name": "Advanced Social Support Systems with AI Integration", "point": 1}
    ],
    "Diplomacy": [
      {"name": "Tribal and Familial Alliances", "point": 0},
      {"name": "Emergence of Diplomatic Protocols among City-States", "point": 0.25},
      {"name": "Nation-State Diplomacy and International Law", "point": 0.5},
      {"name": "Global Governance and Multilateral Institutions", "point": 0.75},
      {"name": "Confederated Diplomacy across Societal Sectors", "point": 1}
    ],
    "Legal Systems": [
      {"name": "Tribal Customs and Oral Laws", "point": 0},
      {"name": "Codification of Laws in Early Civilizations", "point": 0.25},
      {"name": "Establishment of National Legal Systems", "point": 0.5},
      {"name": "International Legal Standards and Human Rights", "point": 0.75},
      {"name": "Advanced Global Legal Frameworks", "point": 1}
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
    "Economic Control": [0,1],
    "Open Borders": [0,1],
    "Education System": [0,1],
    "Healthcare System": [0,1],
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
    "State Intervention": [0,1], # The extent of state involvement in the economy and social services.
    "Economic Equality": [0,1], # Reflects the degree of income and wealth equality enforced by the government.
    "Autarky": [0,1], # The degree to which a society is self-sufficient and minimizes reliance on external entities.
    "Merit-based Advancement": [0,1], # Reflects the degree to which advancement is based on merit, skill, and achievement.
    "Innovation Encouragement": [0,1], # Focus on incentives and support for technological and scientific advancement.
    "Public Commons": [0,1], # Extent to which resources are managed as public commons rather than private property.
    "Historical Continuity": [0,1], # The extent to which governance structures are rooted in historical and traditional precedents.
    "Ideological Enforcement": [0,1], # The extent to which governments enforce a particular ideology or set of beliefs.
    "Participatory Governance": [0,1], # Emphasizes direct participation of citizens in decision-making processes.
    "Sustainability Focus": [0,1], # A focus on sustainable living and ecological balance.
    "Global Solidarity": [0,1] # The extent to which a society or government works with others globally.
  }