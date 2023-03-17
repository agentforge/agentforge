### Primary Class for Agent Executor 

from core.helpers.parser import Parser
import requests

URL="llm:3002"

class ExecutiveCognition():
  def __init__(self) -> None:
    self.parser = Parser()

  def respond(self, prompt):
    # Contacts the llm/inference and gets a response
    url = f"{URL}/llm/inference"

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
        print(response.content)
        return response.content
    else:
        # The request failed
        print(f"Request failed with status code {response.status_code}")
