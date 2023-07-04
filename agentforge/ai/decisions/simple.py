from typing import Dict, Any
from agentforge.ai.routines.reactive import ReactiveRoutine, PlanningRoutine
from agentforge.ai.cognition.memory import Memory
from agentforge.exceptions import BreakRoutineException

class SimpleDecision:
    def __init__(self):
        self.routine = ReactiveRoutine()
        self.memory = Memory()
        self.flows = {'plan': PlanningRoutine()}

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Use the context, config, and user_id to decide on a routine
        context['memory'] = Memory()

        # Our decision loop is responsible for handling top level subroutines so
        # we can keep on eye on interruptions and other state changes
        for subroutine in self.routine.subroutines:
            print(subroutine)
            try:
                context = subroutine.execute(context)
            except BreakRoutineException as interruption:
                # Handle the custom exception -- acts as an interruption in our decision flow
                context = self.flows[str(interruption)].run(context)

        return context
