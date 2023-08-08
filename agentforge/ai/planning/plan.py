from typing import Any, Dict
from agentforge.ai.planning.planner import PlanningController
from agentforge.ai.beliefs.symbolic import SymbolicMemory
from agentforge.ai.attention.tasks import TaskManagement
from agentforge.utils.stream import stream_string
from agentforge.ai.attention.attention import Attention

### PLANNING: Executes PDDL plans with help from LLM resource
class Plan:
    ### Executes PDDL plans with help from LLM resource
    def __init__(self, domain: str):
        self.planner = PlanningController()
        self.symbolic_memory = SymbolicMemory()
        self.attention = Attention()
        self.task_management = TaskManagement()
        self.domain = domain

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:

        user_id = context.get('input.user_id')
        session_id = context.get('input.model_id')
        key = f"{user_id}:{session_id}:{self.domain}"

        ## TODO: CHECK BELIEFS
        ## Check if a plan already exists and there is no other queries in progress
        ## If this is the case we enquire if the user wants to browse other plans or
        ## create a new plan
        ## This step is the confirmation step preferably achieved by CoT Reasoning Engine

        ### PLANNING
        # If the predicate memory attention is satisfied kick off the plan
        if self.attention.attention_satisfied(key):
            print("attention satisfied...")
            finalize_reponse = "I have all the info I need, let me finalize the plan."
            stream_string('channel', finalize_reponse, end_token=" ") # TODO: Make channel user specific, make text plan specific

            context["response"] = finalize_reponse
            response = self.planner.execute(context.get_model_input(), self.attention.get_attention(key))

            self.task_management.update_task(user_id, context["input"]["model_id"], "plan", is_active=False)
            print("[PLAN][update_task]", user_id, context["input"]["model_id"], "plan", False)
            context["response"] = response
            return context

        return context