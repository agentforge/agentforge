from typing import Dict, Any, Protocol

### Primary Root of the interface for a decision timestep
### i.e. when the agent must respond to user input or alternatively 
### when the agent must initiate a decision without user input based
### on an event initiated in previous interactions
class Decision(Protocol):
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]: ...
