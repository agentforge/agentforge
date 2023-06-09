from typing import Any, Dict
from agentforge.interfaces import interface_interactor

### Handles conversion of lipsyncing operations
class Lipsync:
    def __init__(self):
        self.service = interface_interactor.get_interface("w2l")

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lipsync_response = self.service.call(context)

        context["video"] = {"filename": lipsync_response["filename"], "type":"video/mp4" }
        return context