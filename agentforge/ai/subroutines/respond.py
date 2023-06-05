from typing import Any, Dict
from agentforge.interfaces import interface_interactor

class Respond:
    def __init__(self):
        self.service = interface_interactor.get_interface("llm")

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        input = {
            "prompt": context['input']['prompt'],
            "generation_config": context['model_profile']['generation_config'],
            "model_config": context['model_profile']['model_config'],
        }
        response = self.service.call(input)

        if response is None or "choices" not in response:
            return {"error": True, "msg": response} # return error

        context["response"] = response["choices"][0]["text"]
        return context
