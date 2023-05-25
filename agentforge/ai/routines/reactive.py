# TODO: Implement default decision --> decisions are markov chains w/ subroutines as nodes
### i.e. the simplest example: generate text response -> generate wav file -> generate mp4 -> return
from typing import Dict, Any, List, Protocol, Optional
from agentforge.ai import Respond, Parse, Speak, Lipsync, Remember

### Simplest reactive routine for a decision timestep/run
class ReactiveRoutine:
    def __init__(self):
        self.subroutines = [Remember(), Parse(), Respond(), Speak(), Lipsync()]

    def run(self, initial_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        context = initial_context
        for subroutine in self.subroutines:
            context = subroutine.execute(context)
        return context
