import os
import requests
from agentforge.adapters import APIClient

class APIService:
    def __init__(self):
        self.client = APIClient()
        self.llm_url = os.getenv('LLM_ENDPOINT')
        self.tts_url = os.getenv('TTS_ENDPOINT')
        self.w2l_url = os.getenv('W2L_ENDPOINT')
        self.services = {
            'llm': self.llm_url,
            'tts': self.tts_url,
            'w2l': self.w2l_url,
        }

    def _heartbeat(self):
        for service, url in self.services.items():
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.exceptions.RequestException as err:
                print(f"Heartbeat failed for {service}. Error: {err}")
                return False
        return True

    def _fallback(self, service):
        print(f"Fallback initiated for {service}")
        # Implement fallback functionality here

    def call_service(self, service, form_data):
        if not self._heartbeat():
            self._fallback(service)
            return None

        url = self.services[service]
        try:
            response = self.client.post(url, form_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            print(f"Error calling {service}. Error: {err}")
            return None

    # Specific calls to services
    def call_llm(self, form_data):
        return self.call_service('llm', form_data)

    def call_tts(self, form_data):
        return self.call_service('tts', form_data)

    def call_interpret(self, form_data):
        return self.call_service('interpret', form_data)

    def call_lipsync(self, form_data):
        return self.call_service('w2l', form_data)
