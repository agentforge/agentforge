from typing import Optional, Protocol, Callable
from functools import wraps
from requests import Session, Response
from requests.exceptions import RequestException
from http import HTTPStatus
import logging, os, requests

# Generic APIClientProtocol metaclass 
class APIClientProtocol(Protocol):
    def get(self, endpoint: str, params: Optional[dict] = None) -> Response:
        pass
    def post(self, endpoint: str, data: Optional[dict] = None) -> Response:
        pass
    def put(self, endpoint: str, data: Optional[dict] = None) -> Response:
        pass
    def delete(self, endpoint: str) -> Response:
        pass

# Handles the Response object returned by requests
# Ensures that the response is checked for errors
# and logs the response status code
def handle_response(func: Callable[..., Response]) -> Callable[..., Response]:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            response.raise_for_status()
        except RequestException as e:
            logging.error(f'Request failed: {str(e)}')
            raise
        else:
            if response.status_code in {HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.NO_CONTENT}:
                logging.info(f'Successfully received response.')
            else:
                logging.warning(f'Unexpected status code: {response.status_code}.')
        return response
    return wrapper

# Session-based API client
class APIClient(APIClientProtocol):
    def __init__(self, base_url: Optional[str] = None) -> None:
        self.base_url = base_url
        self.session = Session()

        if not self.base_url:
            self.base_url = ""

        logging.info('APIClient initialized.')

    @handle_response
    def get(self, endpoint: str, params: Optional[dict] = None) -> Response:
        url = self.base_url + endpoint
        return self.session.get(url, params=params)

    @handle_response
    def post(self, endpoint: str, data: Optional[dict] = None) -> Response:
        url = self.base_url + endpoint
        return self.session.post(url, json=data)

    @handle_response
    def put(self, endpoint: str, data: Optional[dict] = None) -> Response:
        url = self.base_url + endpoint
        return self.session.put(url, json=data)

    @handle_response
    def delete(self, endpoint: str) -> Response:
        url = self.base_url + endpoint
        return self.session.delete(url)

### Handles the API calls to the LLM, TTS, and other internal generative services
class APIService():
    def __init__(self, endpoint):
        self.client = APIClient()
        self.url = os.getenv(endpoint)

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
