from agentforge.ai.planning.plan import Plan
from agentforge.ai.routines.routine import Routine
from agentforge.ai.agents.statemachine import Node
from agentforge.ai.beliefs.remember import GetResponse
from typing import List

"""
Input - domain: PDDL domain name, plan_prompts: List of prompts to trigger planning
Output - None

Planning Routine - This routine is triggered when the user asks for help with planning a task
"""
class PlanningRoutine(Routine):
    def __init__(self, domain: str, plan_prompts: List[str], goals: List[str]):
        super().__init__(domain, plan_prompts)
        get_response = Node(GetResponse(domain).execute, [])
        self.subroutines = [
            get_response,
            Node(Plan(domain, goals).execute, [get_response]),
        ]