from core.helpers.parser import Parser
from core.agency.avatar import Avatar
from core.config.config import Config
import requests, json, os

def handle_response_error(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.status_code == 200:
            print(f"Request successful with status code {response.status_code}")
            print(response.json())
            return response.json()
        else:
            print(f"Request failed with status code {response.status_code}")
            return "ERROR PLEASE TRY AGAIN LATER"
    return wrapper

class ExecutiveCognition:
    def __init__(self) -> None:
        self.parser = Parser()
        self.avatar = Avatar()
        self.urls = Config("urls")

    @handle_response_error
    def post_request(self, url, json_data):
        return requests.post(url, json=json_data)

    def get_tts(self, form_data):
        url = self.urls["TTS_URL"]
        url = f"{url}/v1/tts"        
        return self.post_request(url, form_data)

    def lipsync(self, form_data):
        url = self.urls["W2L_URL"]
        url = f"{url}/v1/lipsync"
        return self.post_request(url, form_data)

    def parse_config(self, config):
        config = config.replace("=>", ":") # Fix for ruby hash syntax
        return json.loads(config)

    # Either return a wav file or a mp4 file based on flag
    def speak(self, prompt, config):
        # Get wav/tts file
        config = self.parse_config(config)
        avatar = self.avatar.get_avatar(config["avatar"])
        prompt = self.parser.parse_prompt(prompt)
        form_data = {"prompt": prompt, "avatar": avatar}
        wav_response = self.get_tts(form_data)

        # if we want to generate lipsync
        if config["lipsync"] != 'false':
            form_data = {"wav_file": wav_response["filename"], "avatar": avatar}
            lipsync_response = self.lipsync(form_data)
            return {"filename": lipsync_response["filename"], "type": "video/mp4"}

        # else just return the wav file
        return {"filename": wav_response["filename"], "type": "audio/wav"}

    def respond(self, prompt, config):
        url = self.urls["LLM_URL"]
        url = f"{url}/v1/completions"
        prompt = self.parser.parse_prompt(prompt)
        config = self.parse_config(config)
        config["avatar"] = self.avatar.get_avatar(config["avatar"])
        form_data = {"prompt": prompt, "config": config}
        response = self.post_request(url, form_data)
        return self.parse_response(response)
    
    def parse_response(self, response):
        response["response"] = self.parser.parse_response(response["response"])
        return response
