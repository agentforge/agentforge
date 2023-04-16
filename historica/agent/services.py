from historica.config import Config
import requests

def handle_response_error(func):
  def wrapper(*args, **kwargs):
    try:
        response = func(*args, **kwargs)
    except Exception as e:
        print(e)
        print("Request failed with status code 500")
        return "ERROR PLEASE TRY AGAIN LATER"
    if response.status_code == 200:
        print(f"Request successful with status code {response.status_code}")
        print(response.json())
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        return "ERROR PLEASE TRY AGAIN LATER"
  return wrapper

### Handles calls and error handling for external services 
class Service:
    def __init__(self):
      self.urls = Config("urls")

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