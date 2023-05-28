import os
import requests
from agentforge.adapters import APIClient

### API Service level handles calling the API using POST, handles fallback logic, and heartbeat logic
### for the service it is operating
class APIService:
    def __init__(self):
        self.client = APIClient()
        # Check if we are in a test environment
        if os.getenv("ENV") == "test":
            print("TEST ENVIRONMENT DETECTED")
            self.test = True

    def _heartbeat(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            print(f"Heartbeat failed for {self.service}. Error: {err}")
            return False
        return True

    def _fallback(self, service):
        print(f"Fallback initiated for {service}")
        # Implement fallback functionality here

    def call(self, form_data):
        if self.test:
            return self.test() # Return test fixture from Service
        # if not self._heartbeat():
        #     self._fallback(self.service)
        #     return None
        if not self.url:
            raise Exception(f"Service URL {self.service.upper()}_URL not set in .env")
        try:
            response = self.client.post(self.url, form_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            print(f"Error calling {self.service}. Error: {err}")
            return None