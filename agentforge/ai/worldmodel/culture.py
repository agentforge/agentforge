import json, os
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

  states = json.load(open(os.environ.get("WORLDGEN_DATA_DIR", "./") + "culture_states.json"))