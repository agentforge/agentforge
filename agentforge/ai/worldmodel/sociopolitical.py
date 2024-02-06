from agentforge.ai.worldmodel.socialframework import SocialFramework

### The Sociopolitical class describes the sociopolitical framework of a society
class SocioPoliticalFramework(SocialFramework):
  def __init__(self) -> None:
    super().__init__()

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
      {"name": "Tribal Alliances", "point": 0},
      {"name": "Emergence of Diplomatic Protocols among City-States", "point": 0.25},
      {"name": "Nation-State Diplomacy and International Law", "point": 0.5},
      {"name": "Global Governance and Multilateral Institutions", "point": 0.75},
      {"name": "Confederated Diplomacy across Societal Sectors", "point": 1}
    ],
    "Immigration Policies": [
      {"name": "Tribal Nomadism with Open Migration", "point": 0},
      {"name": "Early Settlement Controls and Guest Worker Systems", "point": 0.25},
      {"name": "Nation-State Citizenship and Immigration Laws", "point": 0.5},
      {"name": "Multinational Agreements on Movement and Residency", "point": 0.75},
      {"name": "Open and Regulated Global Mobility", "point": 1}
    ],
    "Military": [
      {"name": "Tribal Warriors and Militias", "point": 0},
      {"name": "Formation of Standing Armies and Fortifications", "point": 0.25},
      {"name": "National Armed Forces with Advanced Weaponry", "point": 0.5},
      {"name": "International Peacekeeping Forces", "point": 0.75},
      {"name": "Integrated Global Defense and Security Networks", "point": 1}
    ],
    "Law": [
      {"name": "Tribal Customs and Oral Laws", "point": 0},
      {"name": "Codification of Laws in Early Civilizations", "point": 0.25},
      {"name": "Establishment of National Legal Systems", "point": 0.5},
      {"name": "International Legal Standards and Human Rights", "point": 0.75},
      {"name": "Advanced Global Legal Frameworks", "point": 1}
    ],
    "Class Stratification": [
      {"name": "Tribal and Caste Hierarchies", "point": 0},
      {"name": "Emergence of Social Classes and Estates", "point": 0.25},
      {"name": "Industrial and Economic Class Divisions", "point": 0.5},
      {"name": "Global Wealth and Opportunity Disparities", "point": 0.75},
      {"name": "Universal Equity and Opportunity", "point": 1}
    ],
  }

  dimensions = {
    "Rights": [0,1], # The degree of protection and respect for human rights in a society.
    "Security": [0,1], # The degree of security and safety in a society.
    "Peace": [0,1], # The degree of peace and stability in a society.
    "Rule of Law": [0,1], # The degree of adherence to the rule of law in a society.
    "Corruption": [0,1], # The degree of corruption and transparency in a society.
    "Gender Equality": [0,1], # The degree of equality between the genders in a society.
    "Religious Tolerance": [0,1], # The degree of acceptance of various religious beliefs and practices.
    "Political Freedom": [0,1], # The degree of political freedom and civil liberties in a society.
    "Social Welfare": [0,1], # The degree of well-being and social support for all citizens.
    "Social Mobility": [0,1], # The ability of individuals or families to move between social strata.
    "Centralization": [0,1], # The degree of centralization of power and authority in a society.
    "Democracy": [0,1], # The degree of democratic governance in a society.
    "Environmental Sustainability": [0,1], # The degree of environmental sustainability and stewardship in a society.
    "Information Freedom": [0,1], # The degree of freedom of information and expression in a society.
    "Privacy": [0,1], # The degree of privacy protection and privacy rights in a society.
    "Civic Participation": [0,1], # The degree of civic participation and engagement in a society.
    "Diplomacy": [0,1], # The degree of diplomatic engagement and international relations in a society.
    "Isolationism": [0,1], # The degree of isolationism or engagement with the global community in a society.
    "Nationalism": [0,1], # The degree of nationalism and national identity in a society.
  }