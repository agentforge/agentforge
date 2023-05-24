from typing import Any, Dict
from agentforge.ai import Subroutine

class Interpret(Subroutine):
    def __init__(self, service):
        self.service = service

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        json_response = self.service.call_interpret(context)
        return json_response
