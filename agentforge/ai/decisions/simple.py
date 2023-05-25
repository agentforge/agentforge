from typing import Dict, Any
from agentforge.ai.routines.reactive import ReactiveRoutine

class SimpleDecision:
    def __init__(self):
        self.routine = ReactiveRoutine()

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Use the context, config, and user_id to decide on a routine
        output = ReactiveRoutine.run(context)
        return output