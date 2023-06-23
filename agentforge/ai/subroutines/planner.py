from typing import Any, Dict
from agentforge.interfaces import interface_interactor
from agentforge.utils import timer_decorator
from agentforge.ai import Planner

class Planner:
    ### Executes plans with help from LLM resource
    def __init__(self):
        self.service = interface_interactor.get_interface("llm")
        self.planner = Planner()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        input = {
            "prompt": context['input']['prompt'],
            "generation_config": context['model_profile']['generation_config'],
            "model_config": context['model_profile']['model_config'],
        }

        response = self.service.call(input)

        context["response"] = response["choices"][0]["text"]
        return context
