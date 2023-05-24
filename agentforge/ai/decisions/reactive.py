# TODO: Implement default decision --> decisions are markov chains w/ subroutines as nodes
### i.e. the simplest example: generate text response -> generate wav file -> generate mp4 -> return
from typing import Dict, Any, List, Protocol, Optional
from agentforge.ai import Subroutine

class ReactiveRoutine:
    def __init__(self, subroutines: List[Subroutine]):
        self.subroutines = subroutines

    def run(self, initial_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        context = initial_context
        for subroutine in self.subroutines:
            context = subroutine.execute(context)
        return context
