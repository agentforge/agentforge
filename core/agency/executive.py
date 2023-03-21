### Primary Class for Agent Executor 

from core.helpers.parser import Parser
import requests

TTS_URL="http://speech:3003"
LLM_URL="http://llm:3002"
W2L_URL="http://wav2lip:3004"

class ExecutiveCognition():
  def __init__(self) -> None:
    self.parser = Parser()


  # Given a text prompt we will use the TTS to generate a wav file
  # Response: wav filename on docker shared volume
  def get_tts(self, prompt):
    url = f"{TTS_URL}/tts/speech"

    # Parse the input message to remove any unnecessary spaces
    prompt = self.parser.parse(prompt)

    # Define the form data
    form_data = { "prompt": prompt }

    # Make a GET request to the API endpoint
    response = requests.post(url, json=form_data)

    # Check the response status code
    if response.status_code == 200:
        # The request was successful
        print(f"Request successful with status code {response.status_code}")
        print(response.json())
        return response.json()
    else:
        # The request failed
        print(f"Request failed with status code {response.status_code}")
        return "ERROR PLEASE TRY AGAIN LATER"

  # Given a wav file we will use Wav2Lip to generate a lip sync video
  # Response: mp4 filename on docker shared volume
  def lipsync(self, wav_file):
    url = f"{W2L_URL}/v1/lipsync"

    # Define the form data
    form_data = { "wav_file": wav_file, "avatar": "alpha" }

    response = requests.post(url, json=form_data)

    # Check the response status code
    if response.status_code == 200:
        # The request was successful
        print(f"Request successful with status code {response.status_code}")
        print(response.json())
        return response.json()
    else:
        # The request failed
        print(f"Request failed with status code {response.status_code}")
        return "ERROR PLEASE TRY AGAIN LATER"

  # Calls TTS and/or Lipsync to generate a response
  def speak(self, prompt, generate_lip_sync):

    wav_response = self.get_tts(prompt)
    if generate_lip_sync:
      lipsync_response = self.lipsync(wav_response["filename"])

      return {"filename": lipsync_response["filename"], "type": "mp4"}
    
    return {"file_name": wav_response["filename"], "type": "wav"}

  # Contacts the llm/inference and gets a response
  def respond(self, prompt):
    url = f"{LLM_URL}/llm/inference"

    # Parse the input message to remove any unnecessary spaces
    prompt = self.parser.parse(prompt)

    # Define the form data
    form_data = { "prompt": prompt }

    # Make a GET request to the API endpoint
    response = requests.post(url, json=form_data)

    # Check the response status code
    if response.status_code == 200:
        # The request was successful
        print("Response content:")
        print(response.json())
        return response.json()
    else:
        # The request failed
        print(f"Request failed with status code {response.status_code}")
        return "ERROR PLEASE TRY AGAIN LATER"
