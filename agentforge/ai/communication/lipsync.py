from typing import Any, Dict
from agentforge.interfaces import interface_interactor

### COMMUNUCATION: Handles conversion of lipsyncing operations
class Lipsync:
    def __init__(self):
        self.service = interface_interactor.get_interface("w2l")

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not context.has_key('audio') or not context.has_key('model_profile'):
            return context
        if context.get('model.model_config.video') and 'audio' in context:
            lipsync_response = self.service.call({'avatar_config': context('model_profile.avatar_config'), 'audio_response': context('audio.audio_response')})
            if lipsync_response is not None:
                context["video"] = {"lipsync_response": lipsync_response["filename"], "type":"video/mp4" }
        return context
