from agentforge.ai.worldmodel.socialframework import SocialFramework

# Tech tree for pre-interstellar society
class TechnologicalFramework(SocialFramework):
  def __init__(self):
    super().__init__()

  dimensions = {
      "Innovation Focus": [0, 1],  # Measures the adoption and sophistication of scientific methodologies.
      "Defense": [0, 1],  # Assesses the development of technologies aimed at ensuring the safety and security of the society.
      "Transportation": [0, 1],  # Reflects the efficiency, diversity, and reach of transportation technologies.
      "Energy Usage": [0, 1],  # Evaluates the extent and sustainability of energy consumption and generation methods.
      "Resource Extraction Technology": [0, 1],  # Assesses the efficiency and environmental impact of resource extraction methods.
  }

  states = {
    "Warfare": [
        {"name": "Stone Weapons and Tools", "point": 0},
        {"name": "Wooden Palisades and Earthworks", "point": 0.05},
        {"name": "Bronze Age Fortifications and Weapons", "point": 0.1},
        {"name": "Iron Age Defenses and Weaponry", "point": 0.15},
        {"name": "City Walls and Fortifications", "point": 0.2},
        {"name": "Gunpowder and Cannons", "point": 0.3},
        {"name": "Rifling and Breech-loading Weapons", "point": 0.4},
        {"name": "Machine Guns and Artillery", "point": 0.5},
        {"name": "Tanks and Armored Vehicles", "point": 0.6},
        {"name": "Radar and Electronic Warfare", "point": 0.7},
        {"name": "Nuclear Weapons", "point": 0.75},
        {"name": "Missile Defense Systems", "point": 0.8},
        {"name": "Stealth Technology", "point": 0.85},
        {"name": "Cyberwarfare and Information Security", "point": 0.9},
        {"name": "Drones and Autonomous Weapons", "point": 0.95},
        {"name": "Laser and Directed Energy Weapons", "point": 1}
    ],
    "Transportation": [
        {"name": "Walking and Animal Riding", "point": 0},
        {"name": "Wheel and Sail", "point": 0.25},
        {"name": "Steam Power", "point": 0.5},
        {"name": "Internal Combustion and Early Flight", "point": 0.75},
        {"name": "Electric and Autonomous Vehicles, Advanced Air and Space Travel", "point": 1}
    ],
    "Information Technology": [
        {"name": "Oral Tradition and Manuscript Culture", "point": 0},
        {"name": "Printed Press", "point": 0.25},
        {"name": "Telegraph and Telephone", "point": 0.5},
        {"name": "Personal Computing and Internet", "point": 0.75},
        {"name": "Quantum Computing and AI", "point": 1}
    ],
    "Life Science": [
        {"name": "Herbal Remedies", "description": "Use of plants and natural substances to treat illnesses.", "point": 0},
        {"name": "Anatomical Study", "description": "Early understanding of body structures and functions.", "point": 0.25},
        {"name": "Germ Theory", "description": "Recognition of microbes causing diseases, leading to advances in hygiene and medicine.", "point": 0.5},
        {"name": "Genetics and Biotechnology", "description": "Manipulation of genetic material for medical treatments and agricultural improvements.", "point": 0.75},
        {"name": "Personalized Medicine", "description": "Tailoring medical treatments to the individual genetic makeup.", "point": 1}
    ],
    "Physical Sciences": [
        {"name": "Basic Elements", "description": "Early classification of matter into earth, water, air, and fire.", "point": 0},
        {"name": "Classical Mechanics", "description": "Foundational principles of physics that explain motion and physical laws.", "point": 0.25},
        {"name": "Chemical Revolution", "description": "Understanding of chemical reactions, elements, and the periodic table.", "point": 0.5},
        {"name": "Quantum Mechanics", "description": "Study of particles at the smallest scales, fundamentally changing our understanding of matter and energy.", "point": 0.75},
        {"name": "Unified Field Theory", "description": "Theoretical framework that attempts to describe all fundamental forces and matter in a single, all-encompassing theory.", "point": 1}
    ],
    "Engineering": [
        {"name": "Simple Machines", "description": "Invention of lever, wheel, and pulley to perform tasks more efficiently.", "point": 0},
        {"name": "Civil Engineering", "description": "Design and construction of infrastructure like bridges, roads, and aqueducts.", "point": 0.25},
        {"name": "Industrial Revolution", "description": "Major advancements in manufacturing and production technologies.", "point": 0.5},
        {"name": "Electronic Age", "description": "Development of electronic devices, computers, and telecommunications.", "point": 0.75},
        {"name": "Nanotechnology", "description": "Manipulation of matter on an atomic, molecular, and supramolecular scale for industrial purposes.", "point": 1}
    ],
    "Applied Sciences": [
        {"name": "Agricultural Innovations", "description": "Early tools and techniques to improve farming efficiency.", "point": 0},
        {"name": "Medical Practice", "description": "Application of scientific knowledge to diagnose, treat, and prevent illness.", "point": 0.25},
        {"name": "Environmental Science", "description": "Study and application of practices to protect the environment and human health.", "point": 0.5},
        {"name": "Information Technology", "description": "Use of computers and software to manage information.", "point": 0.75},
        {"name": "Biotechnological Applications", "description": "Use of living systems and organisms to develop or make products.", "point": 1}
    ],
    "Agriculture and Pastoralism": [
        {"name": "Nomadic Herding", "description": "Moving herds from place to place to find fresh pasture.", "point": 0},
        {"name": "Subsistence Farming", "description": "Growing crops and raising livestock to meet personal or community needs, not for sale.", "point": 0.25},
        {"name": "Agricultural Revolution", "description": "Advancements in farming techniques and tools that increase efficiency.", "point": 0.5},
        {"name": "Industrial Agriculture", "description": "Large-scale farming using industrial techniques for mass production.", "point": 0.75},
        {"name": "Sustainable Agriculture", "description": "Practices that maintain the productivity of the land over time, emphasizing ecological balance.", "point": 1}
    ],
    "Interdisciplinary Science": [
        {"name": "Early Cross-Disciplinary Studies", "description": "Combining knowledge from different fields in a basic form.", "point": 0},
        {"name": "Systems Biology", "description": "Integrating biological data to understand complex biological systems.", "point": 0.25},
        {"name": "Cognitive Science", "description": "Interdisciplinary study of mind and intelligence, integrating psychology, linguistics, and neuroscience.", "point": 0.5},
        {"name": "Nano-Bio-Info-Cogno Convergence", "description": "Fusion of nanotechnology, biotechnology, information technology, and cognitive science.", "point": 0.75},
        {"name": "Quantum Information Science", "description": "Study that applies quantum mechanics to information processing, including computation and communication.", "point": 1}
    ],
}