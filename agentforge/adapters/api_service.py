import os
import requests
from abc import ABC, abstractmethod
from agentforge.adapters import APIClient

class APIService(ABC):
    def __init__(self, endpoint):
        self.client = APIClient()
        self.url = os.getenv(endpoint)

    @abstractmethod
    def call(self, form_data):
        pass

    def _heartbeat(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as err:
            print(f"Heartbeat failed for service at {self.url}. Error: {err}")
            return False

    def _fallback(self):
        print(f"Fallback initiated for service at {self.url}")
        # Implement fallback functionality here
