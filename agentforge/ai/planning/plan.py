from typing import Any, Dict, List
from agentforge.ai.planning.planner import PlanningController
from agentforge.ai.beliefs.symbolic import SymbolicMemory
from agentforge.ai.attention.tasks import TaskManager
from agentforge.utils.stream import stream_string
from agentforge.interfaces import interface_interactor

### PLANNING SUBROUTINE: Executes PDDL plans with help from LLM resource
class Plan:
    ### Executes PDDL plans with help from LLM resource
    def __init__(self, domain: str, goals: List[str]):
        self.service = interface_interactor.get_interface("llm")
        self.planner = PlanningController(domain)
        self.task_management = TaskManager()
        self.domain = domain
        self.goals = goals

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
        # If there are no remaining queries for the planning task, we can execute the plan
        task = context.get("task")
        done = task.done()

        print(f"PLAN PLAN PLAN{task != None} and {not done} and {len(task.all())}")
        print(task != None and not done and len(task.all()))
        print(task)

        if task != None and not done and len(task.all()) == 0:
            # Get the current goal
            goal = self.goals[task.stage]
            print("GOAL", goal)
            queries = self.planner.create_queries(goal)
            print(f"{queries=}")
            list(map(task.push, queries)) # efficiently push queries to the task
            context.set("response", task.activate(context, self.service))
            print(task.to_dict())
            self.task_management.save(task)

        elif task != None and done:
            finalize_reponse = "I have all the info I need, let me finalize the plan."

            # TODO: Make channel user specific, make text plan specific
            stream_string('channel', finalize_reponse, end_token=" ")

            context.set("response", finalize_reponse)
            response = self.planner.execute(context.get_model_input(), task)

            task.active = True
            self.task_management.save(task)
            context.set("response", response)
            return context

        return context
