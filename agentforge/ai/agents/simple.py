from typing import Dict, Any
from agentforge.ai.routines.reactive import ReactiveRoutine, PlanningRoutine
from agentforge.ai.cognition.memory import Memory
from agentforge.ai.agents.statemachine import StateMachine
import threading

class SimpleAgent:
    def __init__(self):
        self.routine = ReactiveRoutine()
        self.flows = {'plan': PlanningRoutine()}

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Use the context, config, and user_id to decide on a routine
        context['memory'] = Memory()
        threading.Thread(target=StateMachine(self.routine.subroutines, self.flows).run, args=(context,)).start()

        # Return True immediately after starting the StateMachine
        return True