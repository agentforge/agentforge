from typing import Dict, Any
from agentforge.ai.routines.reactive import ReactiveRoutine
from agentforge.ai.cognition.memory import Memory

class SimpleDecision:
    def __init__(self):
        self.routine = ReactiveRoutine()
        self.memory = Memory()

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Use the context, config, and user_id to decide on a routine
        context['memory'] = Memory()
        output = self.routine.run(context)
        return output
