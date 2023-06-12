from agentforge.ai import Subroutine
from typing import Dict, Any, Protocol, List, Optional
from agentforge.exceptions import SubroutineException

### Describes a routine, i.e. going to the grocery store or reacting to user input
### A routine is a collection of subroutines with a specific order
class Routine():
    def __init__(self) -> None:
        self.subroutines = []

    def run(self, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        for subroutine in self.subroutines:
            print(subroutine)
            context = subroutine.execute(context)
        return context
