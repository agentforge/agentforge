### Worker abstracts services such as TTS, LLMs, and Wav2Lip into a single interface
### Loads a configuration file with API URL, keys and other information
### Runs via rq worker and listens to a queue for requests
### Sends requests to the appropriate service and returns the response

from core.config.config import Config
import requests
import logging

class Worker():

  def __init__(self) -> None:
    self.config = Config("worker")

  ## Sends a POST request to the given URL with the given data
  def post(self, url: str, data: dict, **kwargs) -> str:
    headers = {'Content-Type': 'application/json'}
    logging.info(f'Sending POST request to {url} with data: {data}')
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        logging.info(f'Response status code: {response.status_code}')
        logging.debug(f'Response data: {response.json()}')
        return response.json()
    else:
        logging.error(f'Error calling API. Response status code: {response.status_code}')
        return {'message': f"Error calling API at {url}"}

  ## Calls LLM service to generate a response
  def generate(self, prompt: str, **kwargs) -> str:
    url = self.config["llm_host"] + ":" + self.config["llm_port"] + "/llm/output"
    data = {
      "prompt": prompt
    }
    self.post(url, data)
  
  ## Calls TTS service to generate a wav file
  def text_to_speech(self, text: str, **kwargs) -> str:
    raise NotImplementedError
  
  ## Calls Wav2Lip service to generate a lip-synced video
  def wav_to_lip(self, wav_file: str, **kwargs) -> str:
    raise NotImplementedError
  
  ## Calls text classification service to generate topics
  def classify(self, text: str, **kwargs) -> str:
    raise NotImplementedError
  
  ## Calls summarization service to generate a summary
  def summarize(self, text: str, **kwargs) -> str:
    raise NotImplementedError
  
  ## Calls intent classification service to generate an intent
  def intent(self, text: str, **kwargs) -> str:
    raise NotImplementedError