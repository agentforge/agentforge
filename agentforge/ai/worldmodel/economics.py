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

  states = {
    "Resource Acquisition Methods": [
      {"name": "Primitive Gathering and Hunting", "point": 0.0},
      {"name": "Foraging and Hunting", "point": 0.11},
      {"name": "Agriculture and Domestication", "point": 0.22},
      {"name": "Early Trade and Resource Exchange", "point": 0.33},
      {"name": "Expansion of Agricultural Techniques", "point": 0.44},
      {"name": "Industrialized Resource Extraction", "point": 0.56},
      {"name": "Mechanization of Agriculture", "point": 0.67},
      {"name": "Renewable and Sustainable Practices", "point": 0.78},
      {"name": "Biotechnological Innovations in Agriculture", "point": 0.89},
      {"name": "Advanced Automation in Resource Acquisition", "point": 1.0}
    ],
    "Trade and Barter Systems": [
      {"name": "Early Barter and Gift Economies", "point": 0.0},
      {"name": "Direct Barter", "point": 0.11},
      {"name": "Introduction of Commodity Money", "point": 0.22},
      {"name": "Development of Marketplaces", "point": 0.33},
      {"name": "Expansion of Trade Networks", "point": 0.44},
      {"name": "Use of Coinage and Paper Money", "point": 0.56},
      {"name": "Mercantilism and Early Capitalism", "point": 0.67},
      {"name": "Electronic Transactions and Banking", "point": 0.78},
      {"name": "Globalization of Financial Markets", "point": 0.89},
      {"name": "Digital Currencies and Decentralized Trade", "point": 1.0}
    ],
    "Currency Systems": [
      {"name": "Primitive Forms of Value Exchange", "point": 0.0},
      {"name": "Barter System", "point": 0.11},
      {"name": "Commodity Money", "point": 0.22},
      {"name": "Emergence of Monetary Systems", "point": 0.33},
      {"name": "Standardization of Currency", "point": 0.44},
      {"name": "Physical Currency", "point": 0.56},
      {"name": "Introduction of Banknotes", "point": 0.67},
      {"name": "Electronic Money", "point": 0.78},
      {"name": "Expansion of Electronic Financial Services", "point": 0.89},
      {"name": "Cryptocurrencies and Digital Money", "point": 1.0}
    ],
    "Economic Models": [
      {"name": "Hunter-Gatherer and Tribal Economies", "point": 0.0},
      {"name": "Tribal and Kinship-based Economies", "point": 0.11},
      {"name": "Feudal and Agrarian Economies", "point": 0.22},
      {"name": "City-States and Mercantile Economies", "point": 0.33},
      {"name": "Renaissance Banking and Early Capitalism", "point": 0.44},
      {"name": "Industrial Capitalist and Socialist Economies", "point": 0.56},
      {"name": "Expansion of Global Trade", "point": 0.67},
      {"name": "Mixed Economies", "point": 0.78},
      {"name": "Digital Economy and Globalization", "point": 0.89},
      {"name": "Post-Scarcity and Distributed Economies", "point": 1.0}
    ],
    "Production Focus": [
      {"name": "Basic Tool Use and Simple Crafts", "point": 0.0},
      {"name": "Handcrafting and Artisanal Goods", "point": 0.11},
      {"name": "Agricultural Production", "point": 0.22},
      {"name": "Craft Guilds and Workshops", "point": 0.33},
      {"name": "Renaissance Art and Innovation", "point": 0.44},
      {"name": "Industrial Manufacturing", "point": 0.56},
      {"name": "Mass Production and Assembly Lines", "point": 0.67},
      {"name": "Service and Information Economy", "point": 0.78},
      {"name": "Technology-Driven Production", "point": 0.89},
      {"name": "High-tech and Sustainable Production", "point": 1.0}
    ],
    "Labor Roles": [
      {"name": "Early Human Survival Tasks", "point": 0.0},
      {"name": "Hunter-Gatherer Societies", "point": 0.11},
      {"name": "Agrarian Labor", "point": 0.22},
      {"name": "Feudal Peasantry and Craftsmanship", "point": 0.33},
      {"name": "Artisans and Guild Members", "point": 0.44},
      {"name": "Industrial Labor", "point": 0.56},
      {"name": "Factory Workers and Unionization", "point": 0.67},
      {"name": "Service-oriented Labor", "point": 0.78},
      {"name": "Information Technology and Service Industry", "point": 0.89},
      {"name": "Knowledge Economy and Automation", "point": 1.0}
    ],
    "Land Use": [
      {"name": "Nomadic and Seasonal Land Use", "point": 0.0},
      {"name": "Nomadic Hunter-Gatherer", "point": 0.11},
      {"name": "Agricultural Settlements", "point": 0.22},
      {"name": "Feudal Estates and Manorial Systems", "point": 0.33},
      {"name": "Agrarian Reforms and Land Ownership", "point": 0.44},
      {"name": "Feudal Systems", "point": 0.56},
      {"name": "Enclosures and Early Industrial Farming", "point": 0.67},
      {"name": "Private Ownership and Industrial Farming", "point": 0.78},
      {"name": "Urbanization and Land Development", "point": 0.89},
      {"name": "Sustainable and Integrated Land Management", "point": 1.0}
    ],
    "Markets": [
      {"name": "Local Trading and Marketplaces", "point": 0.0},
      {"name": "Localized Markets", "point": 0.11},
      {"name": "Regional Trade", "point": 0.22},
      {"name": "Medieval Fairs and Long-Distance Trade", "point": 0.33},
      {"name": "Mercantile Trade Networks", "point": 0.44},
      {"name": "National Economies", "point": 0.56},
      {"name": "Industrial Markets and Commodities", "point": 0.67},
      {"name": "Globalized Trade", "point": 0.78},
      {"name": "International Trade Agreements", "point": 0.89},
      {"name": "Integrated Global Market Systems", "point": 1.0}
    ],
    "Financial Institutions": [
      {"name": "Primitive Lending and Mutual Aid", "point": 0.0},
      {"name": "Informal Lending and Savings Groups", "point": 0.11},
      {"name": "Early Banking Systems", "point": 0.22},
      {"name": "Medieval Banking and Credit", "point": 0.33},
      {"name": "Renaissance Banking Houses", "point": 0.44},
      {"name": "National Banks and Stock Exchanges", "point": 0.56},
      {"name": "Central Banking Systems", "point": 0.67},
      {"name": "International Financial Institutions", "point": 0.78},
      {"name": "Global Financial Markets", "point": 0.89},
      {"name": "Decentralized Financial Networks", "point": 1.0}
    ]
  }
