from typing import Any, Dict
from agentforge.interfaces import interface_interactor

### Handles conversion of text to speech
class Lipsync:
    def __init__(self):
        self.service_factory = interface_interactor

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.service_factory.create_service("w2l")
        service = self.service_factory.get_interface("service")
        lipsync_response = service.call(context)

        context["filename"] = lipsync_response["filename"]
        context["type"] = "video/mp4"
        return context