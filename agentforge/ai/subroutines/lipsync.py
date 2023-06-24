from typing import Any, Dict
from agentforge.interfaces import interface_interactor

### Handles conversion of lipsyncing operations
class Lipsync:
    def __init__(self):
        self.service = interface_interactor.get_interface("w2l")

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if 'audio' not in context or 'model_profile' not in context:
            return context
        if context['model_profile']['model_config']['video'] and 'audio' in context:
            lipsync_response = self.service.call({'avatar_config': context['model_profile']['avatar_config'], 'audio_response': context['audio']['audio_response']})
            if lipsync_response is not None:
                context["video"] = {"lipsync_response": lipsync_response["filename"], "type":"video/mp4" }
        return context
    