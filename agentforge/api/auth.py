from fastapi.security.api_key import APIKeyHeader
from fastapi import HTTPException, Security

# Security
# TODO: Need to make this multi-user one day!
API_KEY = "test-api-key-for-agent-forge-banana-mark-one"
API_KEY_NAME = "X-API-KEY"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return api_key_header