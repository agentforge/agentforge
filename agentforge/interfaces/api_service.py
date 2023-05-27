class LLMService(APIService):
    def __init__(self):
        super().__init__('LLM_ENDPOINT')

    def call(self, form_data):
        if not self._heartbeat():
            self._fallback()
            return None
        try:
            response = self.client.post(self.url, form_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            print(f"Error calling service at {self.url}. Error: {err}")
            return None

class TTSService(APIService):
    def __init__(self):
        super().__init__('TTS_ENDPOINT')

    def call(self, form_data):
        if not self._heartbeat():
            self._fallback()
            return None
        try:
            response = self.client.post(self.url, form_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            print(f"Error calling service at {self.url}. Error: {err}")
            return None

class W2LService(APIService):
    def __init__(self):
        super().__init__('W2L_ENDPOINT')

    def call(self, form_data):
        if not self._heartbeat():
            self._fallback()
            return None
        try:
            response = self.client.post(self.url, form_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            print(f"Error calling service at {self.url}. Error: {err}")
            return None
