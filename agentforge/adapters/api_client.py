from typing import Optional, Protocol, Callable
from functools import wraps
from requests import Session, Response
from requests.exceptions import RequestException
from http import HTTPStatus
import logging, os, requests, traceback
from agentforge.utils import logger

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
        # try:
        response = func(*args, **kwargs)
        # response.raise_for_status()
        # except RequestException as e:
        #     logger.error(f'Request failed: {str(e)}')
        #     # logger.error(traceback.format_exc())
        #     raise
        
        # else:
        if response.status_code in {HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.NO_CONTENT}:
            logger.info(f'Successfully received response.')
        else:
            logger.warning(f'Unexpected status code: {response.status_code}.')
        return response
    return wrapper

# Session-based API client
class APIClient(APIClientProtocol):
    def __init__(self, base_url: Optional[str] = None) -> None:
        self.base_url = base_url
        self.session = Session()

        if not self.base_url:
            self.base_url = ""

        logger.info('APIClient initialized.')

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
