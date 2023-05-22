### Handles calls and error handling for internal services (LLM, TTS, etc)
### Also a good place to place any calls to external APIs

from agentforge.config import Config
import requests
from agentforge.agent.logger import logger

def handle_response_error(func):
  def wrapper(*args, **kwargs):
    try:
        response = func(*args, **kwargs)
    except Exception as e:
        logger.error(e)
        logger.error("Request failed with status code 500")
        return "ERROR PLEASE TRY AGAIN LATER"
    if response.status_code == 200:
        logger.error(f"Request successful with status code {response.status_code}")
        logger.error(response.json())
        return response.json()
    else:
        logger.error(f"Request failed with status code {response.status_code}")
        return "ERROR PLEASE TRY AGAIN LATER"
  return wrapper

class Service:
    def __init__(self):
      self.urls = Config("urls")
      self.models = Config("models")

    @handle_response_error
    def post_request(self, url, json_data):
        return requests.post(url, json=json_data)

    # Specific calls to services
    def call_llm(self, form_data):
        url = self.urls["LLM_URL"]
        url = f"{url}/v1/completions"
        return self.post_request(url, form_data)

    def call_tts(self, form_data):
        url = self.urls["TTS_URL"]
        url = f"{url}/v1/tts"
        return self.post_request(url, form_data)

    def call_interpret(self, form_data):
        url = self.urls["TTS_URL"]
        url = f"{url}/v1/interpret"
        return self.post_request(url, form_data)

    def call_lipsync(self, form_data):
        url = self.urls["W2L_URL"]
        url = f"{url}/v1/lipsync"
        return self.post_request(url, form_data)

    # Configuration-based services
    def get_llm_models(self):
        return self.models
