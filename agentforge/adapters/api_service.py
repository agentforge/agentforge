import os
import requests
from agentforge.adapters import APIClient
from agentforge.utils import logger

### API Service level handles calling the API using POST, handles fallback logic, and heartbeat logic
### for the service it is operating
class APIService:
    def __init__(self):
        # Check if we are in a test environment
        self.test_env = True if os.getenv("ENV") == "test" else False
        self.client = APIClient()

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

    ## Test harness should 1-1 match output from Service
    def test(self):
        return "Test Not Implemented"

    def call(self, form_data):
        if self.test_env:
            return self.test() # Return test fixture from Service
        
        ## TODO: Implement heartbeat logic
        # if not self._heartbeat():
        #     self._fallback(self.service)
        #     return None

        if not self.url:
            raise Exception(f"Service URL {self.service.upper()}_URL not set in .env")
        try:
            response = self.client.post(self.url, form_data)
            response.raise_for_status()
            data = response.json()
            if 'error_type' in data:
                # if there is an error type we need to log the stacktrace
                # and raise the message for the end user
                logger.error(data)
                raise Exception(f"<{data['error_type']}> {data['error_message']}")
            else:
                return response.json()
        except requests.exceptions.RequestException as err:
            print(f"Error calling {self.service}. Error: {err}")
            return None