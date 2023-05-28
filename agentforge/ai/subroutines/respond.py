from typing import Any, Dict
from agentforge.factories import interface_factory

class Respond:
    def __init__(self):
        self.service_factory = interface_factory

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.service_factory.create_service("llm")
        service = self.service_factory.get_interface("service")
        response = service.call(context)

        if "choices" not in response:
            return {"error": True, "msg": response} # return error

        context["response"] = response["choices"][0]["text"]
        return response
