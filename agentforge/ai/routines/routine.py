from agentforge.ai import Subroutine
from typing import Dict, Any, Protocol, List, Optional

### Describes a routine, i.e. going to the grocery store or reacting to user input
### A routine is a collection of subroutines with a specific order
class Routine(Protocol):
    subroutines: List[Subroutine]

    def run(self, initial_context: Optional[Dict[str, Any]]) -> Dict[str, Any]: ...
