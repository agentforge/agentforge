### Handles calls and error handling for internal services (LLM, TTS, etc)
### Also a good place to place any calls to external APIs

from agentforge.utils import logger
from agentforge.adapters import APIClient
from dotenv import load_dotenv
import os

# Handles calls to internal services
# Manages configuraiton and state
class APIService:
    def __init__(self):
        load_dotenv()  # Load environment variables from a .env file
        self.client = APIClient()
        self.llm_url = os.getenv('LLM_URL')
        self.tts_url = os.getenv('TTS_URL')
        self.w2l_url = os.getenv('W2L_URL')

    # Specific calls to services
    def call_llm(self, form_data):
        url = f"{self.llm_url}/v1/completions"
        return self.client.post(url, form_data).json()

    def call_tts(self, form_data):
        url = f"{self.tts_url}/v1/tts"
        return self.client.post(url, form_data).json()

    def call_interpret(self, form_data):
        url = f"{self.tts_url}/v1/interpret"
        return self.client.post(url, form_data).json()

    def call_lipsync(self, form_data):
        url = f"{self.w2l_url}/v1/lipsync"
        return self.client.post(url, form_data).json()
