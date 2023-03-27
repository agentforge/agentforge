from core.helpers.parser import Parser
import requests, json

TTS_URL = "http://speech:3003"
LLM_URL = "http://llm:3002"
W2L_URL = "http://wav2lip:3004"

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

    @handle_response_error
    def post_request(self, url, json_data):
        return requests.post(url, json=json_data)

    def get_tts(self, form_data):
        url = f"{TTS_URL}/v1/tts"        
        return self.post_request(url, form_data)

    def lipsync(self, form_data):
        url = f"{W2L_URL}/v1/lipsync"
        return self.post_request(url, form_data)

    def parse_config(self, config):
        config = config.replace("=>", ":") # Fix for ruby hash syntax
        return json.loads(config)

    # Either return a wav file or a mp4 file based on flag
    def speak(self, prompt, config):
        # Get wav/tts file
        prompt = self.parser.parse(prompt)
        form_data = {"prompt": prompt}
        wav_response = self.get_tts(form_data)

        config = self.parse_config(config)
        # if we want to generate lipsync
        if opts["lipsync"]:
            form_data = {"wav_file": wav_response["filename"], "avatar": config["avatar"]}
            lipsync_response = self.lipsync(form_data)
            return {"filename": lipsync_response["filename"], "type": "video/mp4"}
        
        # else just return the wav file
        return {"file_name": wav_response["filename"], "type": "audio/wav"}

    def respond(self, prompt, config):
        url = f"{LLM_URL}/v1/completions"
        prompt = self.parser.parse(prompt)
        form_data = {"prompt": prompt, "config": self.parse_config(config)}
        return self.post_request(url, form_data)
