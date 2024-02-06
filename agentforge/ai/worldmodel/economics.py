from agentforge.ai.worldmodel.socialframework import SocialFramework

class EconomicFramework(SocialFramework):
  def __init__(self):
    super().__init__()

  dimensions = {
    "Wealth Distribution": [0,1],  # Measures the spread of wealth across a society, from highly unequal (0) to perfectly equitable (1).
    "Trade Efficiency": [0,1],  # Measures the efficiency and effectiveness of trade and commerce within a society.
  }

  states = {
    "Resource Acquisition Methods": [
      {"name": "Foraging and Hunting", "point": 0},
      {"name": "Agriculture and Domestication", "point": 0.25},
      {"name": "Industrialized Resource Extraction", "point": 0.5},
      {"name": "Renewable and Sustainable Practices", "point": 0.75},
      {"name": "Advanced Automation in Resource Acquisition", "point": 1}
    ],
    "Trade and Barter Systems": [
      {"name": "Direct Barter", "point": 0},
      {"name": "Introduction of Commodity Money", "point": 0.25},
      {"name": "Use of Coinage and Paper Money", "point": 0.5},
      {"name": "Electronic Transactions and Banking", "point": 0.75},
      {"name": "Digital Currencies and Decentralized Trade", "point": 1}
    ],
    "Currency Systems": [
      {"name": "Barter System", "point": 0},
      {"name": "Commodity Money", "point": 0.25},
      {"name": "Physical Currency", "point": 0.5},
      {"name": "Electronic Money", "point": 0.75},
      {"name": "Cryptocurrencies and Digital Money", "point": 1}
    ],
    "Economic Models": [
      {"name": "Tribal and Kinship-based Economies", "point": 0},
      {"name": "Feudal and Agrarian Economies", "point": 0.25},
      {"name": "Industrial Capitalism and Socialism", "point": 0.5},
      {"name": "Mixed Economies", "point": 0.75},
      {"name": "Post-Scarcity and Distributed Economies", "point": 1}
    ],
    "Production Focus": [
      {"name": "Handcrafting and Artisanal Goods", "point": 0},
      {"name": "Agricultural Production", "point": 0.25},
      {"name": "Industrial Manufacturing", "point": 0.5},
      {"name": "Service and Information Economy", "point": 0.75},
      {"name": "High-tech and Sustainable Production", "point": 1}
    ],
    "Labor Roles": [
      {"name": "Hunter-Gatherer Societies", "point": 0},
      {"name": "Agrarian Labor", "point": 0.25},
      {"name": "Industrial Labor", "point": 0.5},
      {"name": "Service-oriented Labor", "point": 0.75},
      {"name": "Knowledge Economy and Automation", "point": 1}
    ],
    "Land Use": [
      {"name": "Nomadic Hunter-Gatherer", "point": 0},  # Land is used communally, with no permanent settlements or ownership.
      {"name": "Agricultural Settlements", "point": 0.25},  # Emergence of agriculture leads to settled communities and the beginnings of land ownership.
      {"name": "Feudal Systems", "point": 0.5},  # Land is owned by nobility, with peasants working the land under feudal obligations.
      {"name": "Private Ownership and Industrial Farming", "point": 0.75},  # Shift towards private land ownership and the use of industrial techniques in farming.
      {"name": "Sustainable and Integrated Land Management", "point": 1}  # Modern approaches to land use that emphasize sustainability, conservation, and integrated management practices.
    ],
    "Market Dynamics": [
      {"name": "Localized Markets", "point": 0},
      {"name": "Regional Trade", "point": 0.25},
      {"name": "National Economies", "point": 0.5},
      {"name": "Globalized Trade", "point": 0.75},
      {"name": "Integrated Global Market Systems", "point": 1}
    ],
    "Financial Institutions": [
      {"name": "Informal Lending and Savings Groups", "point": 0},
      {"name": "Early Banking Systems", "point": 0.25},
      {"name": "National Banks and Stock Exchanges", "point": 0.5},
      {"name": "International Financial Institutions", "point": 0.75},
      {"name": "Decentralized Financial Networks", "point": 1}
    ],
    "Trade Agreements and Policies": [
      {"name": "Bilateral Trade Pacts", "point": 0},
      {"name": "Regional Trade Agreements", "point": 0.25},
      {"name": "Multinational Trade Organizations", "point": 0.5},
      {"name": "Global Trade Frameworks", "point": 0.75},
      {"name": "Universal Trade Protocols", "point": 1}
    ],
    "Sustainability and Environmental Economics": [
      {"name": "Exploitative Use of Resources", "point": 0},
      {"name": "Recognition of Environmental Costs", "point": 0.25},
      {"name": "Sustainable Practices and Regulations", "point": 0.5},
      {"name": "Circular Economy", "point": 0.75},
      {"name": "Fully Sustainable and Regenerative Economies", "point": 1}
    ],
    "Property Rights and Ownership Models": [
      {"name": "Tribal and Common Ownership", "point": 0},
      {"name": "Feudal Land Ownership", "point": 0.25},
      {"name": "Private Property Rights", "point": 0.5},
      {"name": "Intellectual Property Laws", "point": 0.75},
      {"name": "Shared and Cooperative Ownership Models", "point": 1}
    ],
    "Economic Adaptability": [
      {"name": "Rigid Traditional Economies", "point": 0},
      {"name": "Early Industrial Adaptability", "point": 0.25},
      {"name": "Flexible Market Economies", "point": 0.5},
      {"name": "Adaptive and Resilient Economies", "point": 0.75},
      {"name": "Highly Dynamic and Responsive Economies", "point": 1}
    ],
    "Crisis and Recovery Mechanisms": [
      {"name": "Localized and Informal Support Systems", "point": 0},
      {"name": "Early State Interventions", "point": 0.25},
      {"name": "Structured Economic Bailouts and Policies", "point": 0.5},
      {"name": "Comprehensive Social Safety Nets", "point": 0.75},
      {"name": "Predictive and Preemptive Economic Management", "point": 1}
    ]
  }
