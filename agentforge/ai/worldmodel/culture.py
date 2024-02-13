from agentforge.ai.worldmodel.socialframework import SocialFramework

### The CulturalFramework class describes the sociopolitical framework of a culture
class CulturalFramework(SocialFramework):
  def __init__(self) -> None:
    super().__init__()

  dimensions = {
    "Family Roles": [0,1], # The structure and function of family units within a society.
    "Art & Aesthetics": [0,1], # The importance and role of art, beauty, and creativity in a society.
    "Organized Religion": [0,1],
    "Belief Systems": [0,1], # Animism, Polytheism, Monotheism, Secularism
    "Spirituality": [0,1],
    "Diversity": [0,1],
    "Creativity": [0,1],
    "Ritual Importance": [0,1],
    "Zealotry": [0,1], # The degree to which a society is driven by ideological fervor.
    "Cultural Homogeneity": [0,1], # Indicates the extent to which a government promotes a singular cultural or ethnic identity.
    "Diversity of Belief": [0, 1],  # Measures the diversity and complexity of belief systems, including religion, philosophy, and worldview.
  }

  states = {
    "Language and Communication": [
      {"name": "Non-verbal Communication", "description": "The earliest form of communication involving gestures, facial expressions, and body language before the development of language.", "point": 0.0},
      {"name": "Gesture and Sign Languages", "description": "Early forms of human communication using gestures and signs before the development of spoken language.", "point": 0.11},
      {"name": "Oral Tradition", "description": "Cultures primarily using spoken word for communication and storytelling.", "point": 0.22},
      {"name": "Pictograms and Ideograms", "description": "The use of symbolic pictures and designs to represent objects and concepts.", "point": 0.33},
      {"name": "Cuneiform and Hieroglyphics", "description": "Early writing systems developed in ancient civilizations for record-keeping and communication.", "point": 0.44},
      {"name": "Alphabets and Writing Systems", "description": "Development of alphabetic and phonetic writing systems allowing for more precise expression.", "point": 0.56},
      {"name": "Printed Literature", "description": "The invention of the printing press and the widespread production and distribution of written materials.", "point": 0.67},
      {"name": "Mass Media", "description": "The emergence of newspapers, radio, and television as means of mass communication.", "point": 0.78},
      {"name": "Digital Communication", "description": "Use of digital platforms and technology for communication, including the internet, social media, and mobile communication.", "point": 0.89},
      {"name": "Augmented and Virtual Reality", "description": "Advanced technologies providing immersive communication experiences.", "point": 0.95},
      {"name": "Universal Language", "description": "Adoption or development of a language understood by all members of a society, possibly facilitated by real-time translation technologies.", "point": 1.0}
    ],
    "Rituals and Ceremonies": [
      {"name": "Primitive Rituals", "description": "Early human rituals surrounding life, death, and the natural world, often tied to animism and the spiritual significance of nature.", "point": 0.0},
      {"name": "Seasonal and Harvest Ceremonies", "description": "Rituals that celebrate seasonal changes and harvest times.", "point": 0.22},
      {"name": "Rites of Passage", "description": "Ceremonies marking important transitional stages in a person's life, such as birth, coming of age, marriage, and death.", "point": 0.44},
      {"name": "State Ceremonies", "description": "Formal rituals conducted by the state, including coronations, national holidays, and military honors.", "point": 0.67},
      {"name": "Secular Celebrations", "description": "Non-religious festivals and celebrations that have cultural significance, such as independence days and cultural festivals.", "point": 0.89},
      {"name": "Global and Interconnected Celebrations", "description": "Festivals and ceremonies that transcend cultural and geographical boundaries, facilitated by digital connectivity.", "point": 1.0}
    ],
    "Artistic Expression": [
      {"name": "Primitive Art Forms", "description": "The earliest forms of artistic expression, including simple musical instruments and basic ornamentation.", "point": 0.0},
      {"name": "Cave Paintings and Tribal Dances", "description": "Early forms of artistic expression used by hunter-gatherer societies.", "point": 0.11},
      {"name": "Classical Arts", "description": "Development of structured art forms like painting, sculpture, music, and literature.", "point": 0.22},
      {"name": "Renaissance Art", "description": "The flourishing of art during the Renaissance, focusing on humanism, realism, and perspective.", "point": 0.33},
      {"name": "Modernism", "description": "Artistic movements that reject traditional forms and experiment with new techniques and perspectives.", "point": 0.44},
      {"name": "Abstract and Conceptual Art", "description": "Movements that emphasize the idea behind the work of art over its aesthetic or material properties.", "point": 0.56},
      {"name": "Digital and Multimedia Art", "description": "Use of digital technology to create art that encompasses multiple mediums and interactive experiences.", "point": 0.78},
      {"name": "Virtual and Augmented Reality Art", "description": "Art that utilizes VR and AR technologies to create immersive and interactive artistic experiences.", "point": 0.89},
      {"name": "AI-generated Art", "description": "Art created with the assistance or sole authorship of artificial intelligence, exploring the boundaries of creativity.", "point": 1.0}
    ]
  }
