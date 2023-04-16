from historica.agent import Avatar
from historica.agent import Agent
from historica.config import Config
import requests, json, os
from flask_sse import sse

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

### Executive Cognition
### Handles Model Ensemble Coordination
### Higher level memory and reasoning loops
class ExecutiveCognition:
    def __init__(self) -> None:
        self.avatar = Avatar() # personality
        self.agent = Agent() # agency, reason, memory, prompt engineering
        self.urls = Config("urls")
        self.reflection = None

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

    def parse_config(self, config):
        return config
        # return json.loads(config)

    # Either return a wav file or a mp4 file based on flag
    def speak(self, prompt, form_data):
        # Get wav/tts file
        form_data = self.parse_config(form_data)

        avatar = self.avatar.get_avatar(form_data["avatar"])
        form_data["avatar"] = avatar

        prompt = self.agent.parser.parse_prompt(prompt)
        wav_response = self.call_tts(form_data)

        # if we want to generate lipsync
        if form_data["lipsync"] != 'false':
            form_data["wav_file"] = wav_response["filename"]
            lipsync_response = self.call_lipsync(form_data)
            return {"filename": lipsync_response["filename"], "type": "video/mp4"}

        # else just return the wav file
        return {"filename": wav_response["filename"], "type": "audio/wav"}

    # Takes a sound file and returns a text string
    def interpret(self, form_data):
        # Get wav/tts file
        form_data = self.parse_config(form_data)

        json_response = self.call_interpret(form_data)

        # else just return the wav file
        return json_response

    def respond(self, prompt, form_data):
        # Configure agent with new config
        form_data = self.parse_config(form_data)
        form_data["avatar"] = self.avatar.get_avatar(form_data["avatar"])
        self.agent.configure(form_data)

        # Record raw prompt in memory
        self.agent.save_speech(prompt)

        # Format prompt with our Prompt engineering
        formatted_prompt = self.agent.process_prompt(instruction=prompt, config=form_data)
        form_data["prompt"] = formatted_prompt
        if self.reflection is not None:
            form_data["avatar"]["prompt_context"]["reflection"] = self.reflection

        # Get response from LLM
        response = self.call_llm(form_data)
        print(response)
        if "choices" not in response:
            return {"error": response} # return error
        response = self.parse_and_save_response(response)

        # Reflection on this conversation
        self.reflect(prompt, response, form_data)

        return response

    def get_reflect_prompt(self, prompt, response):
        reflection_prompt = f"""Reflect on how the following statement statement makes you feel: {prompt}"""
        # reflection_prompt = f"""Reflect on the following statement: Does this response "{response}" match this prompt: "{prompt}"?"""
        # reflection_prompt = f"""
        #     You are [Name of famous expert 1], together with [Name of famous expert 2] you are reviewing this document:
        #     {prompt}
        #     You take turns discussing and suggesting improvement points, until you at the end, rewrite only the document and implement all the suggestions.
        # """

        reflexion = self.agent.prompt_manager.get_prompt("reflexion_prompt", instruction=reflection_prompt)
        return reflection_prompt

    def reflect(self, prompt, response, form_data):
        # Get reflection prompt
        reflection_prompt = self.get_reflect_prompt(prompt, response)

        # Format prompt with our Prompt engineering
        formatted_prompt = self.agent.process_prompt(instruction=reflection_prompt, config=form_data)
        form_data["prompt"] = formatted_prompt
        form_data["streaming"] = False
        form_data["max_new_tokens"] = 128

        response = self.call_llm(form_data)
        self.reflection = response["choices"][0]["text"] # Set the reflection for next time #TODO: This is a hack we need to use disk to store this
        print(f"### REFLECTION\n{response}")
        sse.publish({"reflection": response}, type='reflection')

    def parse_and_save_response(self, response):
        response["response"] = self.parse_llm_response(response["choices"][0]["text"]) # backwards compatibility
        response["choices"][0]["text"] =  response["response"]
        # Record response in memory
        self.agent.save_response(response["response"])
        return response

    # Keyed to alpaca-7b, needs to be updated for other models
    def parse_llm_response(self, text):
        bad_output_delimeters = ['# End of instruction', '# End of the output', '! # No answer', 'Output:', '"""', "### Input:", "#noinstantiation", "## Output:", "# End of Instruction", "### End", "### Instruction", "### Response", "# Python Responses", "# Output:", "#if __name__ == '__main__':", "#end document", "<# end of output #>", "% endinstruction", "# End of story"]
        for i in bad_output_delimeters:
            text = text.split(i)
            text = text[0]
        text = text.replace("\n", "<br>") # use br for new line
        print(text)
        return text.strip()
