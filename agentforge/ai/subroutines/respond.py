from typing import Any, Dict
from agentforge.interfaces import interface_interactor

class Respond:
    def __init__(self):
        self.service = interface_interactor.get_interface("llm")

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        response = self.service.call(context['input'])

        if "choices" not in response:
            return {"error": True, "msg": response} # return error

        context["response"] = response["choices"][0]["text"]
        return response
