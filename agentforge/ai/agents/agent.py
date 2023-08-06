from typing import Dict, Any, Protocol

### Primary Root of the interface for a agent timestep
### i.e. when the agent must respond to user input or alternatively 
### when the agent must initiate a agent_interactor without user input based
### on an event initiated in previous interactions
class Agent(Protocol):
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]: ...
