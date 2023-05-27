from typing import Dict, Any
from agentforge.ai.routines.reactive import ReactiveRoutine

class SimpleDecision:
    def __init__(self):
        pass

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Use the context, config, and user_id to decide on a routine
        self.routine = ReactiveRoutine()
        output = self.routine.run(context)
        return output