from typing import Dict, Any
from agentforge.ai.routines.reactive import ReactiveRoutine
from agentforge.ai.routines.planning import PlanningRoutine
from agentforge.ai.cognition.memory import Memory
from agentforge.ai.agents.statemachine import StateMachine
import threading

class SimpleAgent:
    def __init__(self):
        self.routine = ReactiveRoutine()
        self.additional_routines = {'plan': PlanningRoutine()}

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Use the context, config, and user_id to decide on a routine
        context['memory'] = Memory()
        state_machine = StateMachine(self.routine.subroutines, self.additional_routines)
        threading.Thread(target=state_machine.run, args=(context,)).start()
        # Return True immediately after starting the StateMachine
        return True