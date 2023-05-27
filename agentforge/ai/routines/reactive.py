# TODO: Implement default decision --> decisions are markov chains w/ subroutines as nodes
### i.e. the simplest example: generate text response -> generate wav file -> generate mp4 -> return
from typing import Dict, Any, List, Protocol, Optional
from agentforge.ai import Respond, Parse, Speak, Lipsync, Remember, Recall
from agentforge.ai.routines.routine import Routine

### Simplest reactive routine for a decision timestep/run
class ReactiveRoutine(Routine):
    def __init__(self):
        self.subroutines = [Remember(), Recall(), Parse(), Respond(), Speak(), Lipsync()]
