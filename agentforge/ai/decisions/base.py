from typing import Dict, Any, List, Protocol, Optional
from agentforge.ai import Subroutine


### Describes a routine, i.e. going to the grocery store or reacting to user input
### A routine is a collection of subroutines with a specific order
class Routine(Protocol):
    subroutines: List[Subroutine]

    def run(self, initial_context: Optional[Dict[str, Any]]) -> Dict[str, Any]: ...


### Primary Root of the interface for a decision timestep
### i.e. when the agent must respond to user input or alternatively 
### when the agent must initiate a decision without user input based
### on an event initiated in previous interactions
class Decision(Protocol):
    def decide(self, context: Dict[str, Any], config: Dict[str, Any], user_id: str) -> Routine: ...
