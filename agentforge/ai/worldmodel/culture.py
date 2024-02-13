from agentforge.ai.worldmodel.socialframework import SocialFramework

### The CulturalFramework class describes the sociopolitical framework of a culture
class CulturalFramework(SocialFramework):
  def __init__(self) -> None:
    super().__init__()

  dimensions = {
    "Art & Aesthetics": [0,1],
    "Organized Religion": [0,1],
    "Spirituality": [0,1],
    "Diversity": [0,1],
    "Creativity": [0,1],
    "Ritual Importance": [0,1],
    "Zealotry": [0,1], # The degree to which a society is driven by ideological fervor.
    "Cultural Homogeneity": [0,1], # Indicates the extent to which a government promotes a singular cultural or ethnic identity.
    "Diversity of Belief": [0, 1],  # Measures the diversity and complexity of belief systems, including religion, philosophy, and worldview.
  }

  states = {
    "Family Roles": [
        {"name": "Matrilineal", "description": "Inheritance and lineage traced through the mother's line.", "point": 0.2},
        {"name": "Patrilineal", "description": "Inheritance and lineage traced through the father's line.", "point": 0.4},
        {"name": "Bilateral", "description": "Inheritance and lineage traced through both parents.", "point": 0.6},
        {"name": "Non-traditional", "description": "Flexible or non-conventional family structures, including chosen families.", "point": 0.8},
    ],
    "Language and Communication": [
        {"name": "Gesture and Sign Languages", "description": "Early forms of human communication using gestures and signs before the development of spoken language.", "point": 0.1},
        {"name": "Oral Tradition", "description": "Cultures primarily using spoken word for communication and story-telling.", "point": 0.2},
        {"name": "Pictograms and Ideograms", "description": "The use of symbolic pictures and designs to represent objects and concepts.", "point": 0.3},
        {"name": "Cuneiform and Hieroglyphics", "description": "Early writing systems developed in ancient civilizations for record-keeping and communication.", "point": 0.4},
        {"name": "Alphabets and Writing Systems", "description": "Development of alphabetic and phonetic writing systems allowing for more precise expression.", "point": 0.5},
        {"name": "Printed Literature", "description": "The invention of the printing press and the widespread production and distribution of written materials.", "point": 0.6},
        {"name": "Mass Media", "description": "The emergence of newspapers, radio, and television as means of mass communication.", "point": 0.7},
        {"name": "Digital Communication", "description": "Use of digital platforms and technology for communication, including the internet, social media, and mobile communication.", "point": 0.8},
        {"name": "Augmented and Virtual Reality", "description": "Advanced technologies providing immersive communication experiences.", "point": 0.9},
        {"name": "Universal Language", "description": "Adoption or development of a language understood by all members of a society, possibly facilitated by real-time translation technologies.", "point": 1.0},
    ],
    "Belief Systems": [
        {"name": "Animism", "description": "Belief that natural objects, natural phenomena, and the universe itself possess souls.", "point": 0.2},
        {"name": "Polytheism", "description": "Belief in or worship of more than one god.", "point": 0.4},
        {"name": "Monotheism", "description": "Belief in the existence of only one god that created the world, a central figure in the religious doctrine.", "point": 0.6},
        {"name": "Secularism", "description": "A move towards separation of religion from political, social, and educational matters.", "point": 0.8},
    ],
    "Rituals and Ceremonies": [
        {"name": "Seasonal and Harvest Ceremonies", "description": "Rituals that celebrate seasonal changes and harvest times.", "point": 0.2},
        {"name": "Rites of Passage", "description": "Ceremonies marking important transitional stages in a person's life, such as birth, coming of age, marriage, and death.", "point": 0.4},
        {"name": "State Ceremonies", "description": "Formal rituals conducted by the state, including coronations, national holidays, and military honors.", "point": 0.6},
        {"name": "Secular Celebrations", "description": "Non-religious festivals and celebrations that have cultural significance, such as independence days and cultural festivals.", "point": 0.8},
    ],
    "Artistic Expression": [
        {"name": "Cave Paintings and Tribal Dances", "description": "Early forms of artistic expression used by hunter-gatherer societies.", "point": 0.2},
        {"name": "Classical Arts", "description": "Development of structured art forms like painting, sculpture, music, and literature.", "point": 0.4},
        {"name": "Modernism", "description": "Artistic movements that reject traditional forms and experiment with new techniques and perspectives.", "point": 0.6},
        {"name": "Digital and Multimedia Art", "description": "Use of digital technology to create art that encompasses multiple mediums and interactive experiences.", "point": 0.8},
    ],
  }