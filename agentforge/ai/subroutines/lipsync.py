from typing import Any, Dict
from agentforge.interfaces import APIService

### Handles conversion of text to speech
class Lipsync:
    def __init__(self):
        self.service = APIService()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = context['prompt']
        form_data = context['form_data']
        avatar = self.avatar.get_avatar(form_data["avatar"])
        form_data["avatar"] = avatar

        prompt = self.agent.parser.parse_prompt(prompt)
        wav_response = self.service.call_tts(form_data)

        if "lipsync" in form_data and form_data["lipsync"] != 'false':
            form_data["wav_file"] = wav_response["filename"]
            lipsync_response = self.service.call_lipsync(form_data)
            return {"filename": lipsync_response["filename"], "type": "video/mp4"}

        return {"filename": wav_response["filename"], "type": "audio/wav"}
