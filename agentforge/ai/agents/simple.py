from typing import Dict, Any
from agentforge.ai.routines.reactive import ReactiveRoutine
from agentforge.ai.routines.planning import PlanningRoutine
from agentforge.ai.beliefs.memory import Memory
from agentforge.ai.agents.statemachine import StateMachine
from agentforge.ai.agents.context import Context
from agentforge.ai.reasoning.query_engine import QueryEngine

import threading

class SimpleAgent:
    def __init__(self):
        self.routine = ReactiveRoutine()
        self.additional_routines = {'plan': PlanningRoutine()}

    def run(self, input: Dict[str, Any]) -> Dict[str, Any]:

        context = Context(input)
        context.query_engine = QueryEngine(input["input"]['user_id'], input["input"]['model_id'])
        context.memory =  Memory()

        state_machine = StateMachine(self.routine.subroutines, self.additional_routines)
        threading.Thread(target=state_machine.run, args=(context,)).start()
        return True