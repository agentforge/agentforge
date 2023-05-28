# TODO: Implement default decision --> decisions are markov chains w/ subroutines as nodes
### i.e. the simplest example: generate text response -> generate wav file -> generate mp4 -> return
from typing import Dict, Any, List, Protocol, Optional
from agentforge.ai.subroutines.respond import Respond
from agentforge.ai.subroutines.parse import Parse
from agentforge.ai.subroutines.speak import Speak
from agentforge.ai.subroutines.lipsync import Lipsync
from agentforge.ai.subroutines.remember import Remember
from agentforge.ai.subroutines.recall import Recall
from agentforge.ai.routines.routine import Routine

### Simplest reactive routine for a decision timestep/run
class ReactiveRoutine(Routine):
    def __init__(self):
        self.subroutines = [Remember(), Recall(), Parse(), Respond()] #, Speak(), Lipsync()]
