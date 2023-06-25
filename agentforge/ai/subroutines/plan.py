from typing import Any, Dict
from agentforge.interfaces import interface_interactor
from agentforge.utils import timer_decorator
from agentforge.ai.cognition.planner import PlanningController
from agentforge.utils import async_execution_decorator

class Plan:
    ### Executes PDDL plans with help from LLM resource
    def __init__(self):
        self.service = interface_interactor.get_interface("llm")
        self.planner = PlanningController(self.service)

    @async_execution_decorator
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if self.detect_plan(context):
          input = {
              "prompt": context['input']['prompt'],
              "generation_config": context['model_profile']['generation_config'],
              "model_config": context['model_profile']['model_config'],
          }

          # response = self.service.call(input)
          response = self.planner.execute(input)

          context["response"] = response
        return context
