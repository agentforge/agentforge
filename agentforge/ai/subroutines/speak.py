from typing import Any, Dict
from agentforge.interfaces import interface_interactor

### Handles conversion of text to speech
class Speak:
    def __init__(self):
        self.service = interface_interactor.get_interface("tts")

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        wav_response = self.service.call({'response': context['response'], 'avatar_config': context['model_profile']['avatar_config']})
        if wav_response is not None:
            context['audio'] = {"audio_response": wav_response["filename"], "type": "audio/wav"}
        return context

