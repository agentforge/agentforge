from agentforge.ai.planning.plan import Plan
from agentforge.ai.routines.routine import Routine
from agentforge.ai.agents.statemachine import Node
from agentforge.ai.communication.ack import Acknowledge
from typing import List

"""
Input - domain: PDDL domain name, plan_prompts: List of prompts to trigger planning
Output - None

Planning Routine - This routine is triggered when the user asks for help with planning a task
"""
class PlanningRoutine(Routine):
    def __init__(self, domain: str, plan_prompts: List[str], goals: List[str]):
        super().__init__(domain, plan_prompts)
        ack = Node(Acknowledge(domain).execute, [])
        self.subroutines = [
            ack,
            Node(Plan(domain, goals).execute, [ack]),
        ]