# Hack for deeplake issue
import deeplake
deeplake.__version__ = '3.6.2'

# main.py
from fastapi import Request, FastAPI
from agentforge.api.model_profiles import router as model_profiles_router
from agentforge.api.agent import router as agent_router
from agentforge.api.auth import router as token_router
from agentforge.api.user import router as user_router
from agentforge.api.app import init_api
from agentforge.utils import logger
from agentforge.interfaces import interface_interactor

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import traceback

from supertokens_python import get_all_cors_headers
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python import init, InputAppInfo, SupertokensConfig
from supertokens_python.recipe import emailpassword, session

from typing import Dict, Deque
from collections import deque
from datetime import datetime, timedelta

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int, time_window: int):
        super().__init__(app)
        self.max_requests = max_requests
        self.time_window = time_window
        self.request_logs: Dict[str, Deque[datetime]] = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = str(request.client.host)
        now = datetime.now()

        if client_ip not in self.request_logs:
            self.request_logs[client_ip] = deque()

        request_log = self.request_logs[client_ip]

        # Clean up the request log by removing timestamps older than the time window
        while request_log and now - request_log[0] > timedelta(seconds=self.time_window):
            request_log.popleft()

        # Enforce the rate limit
        if len(request_log) >= self.max_requests:
            return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})

        # Log the current request
        request_log.append(now)

        response = await call_next(request)
        return response

### TODO: limit to dev/test environment
from agentforge.interfaces import interface_interactor

# db = interface_interactor.get_interface("db")
# d = DomainBuilder(db)
# d.upload_documents_from_folder('garden', '/app/agentforge/agentforge/config/configs/planner/domains/garden', 'p_example')

app = init_api()
app.add_middleware(get_middleware())

# Supertokens
init(
    app_info=InputAppInfo(
        app_name="GreenSage",
        api_domain="https://mite-inspired-snipe.ngrok-free.app",
        website_domain="https://08d6f5767742.ngrok.app",
        api_base_path="/api/auth",
        website_base_path="/auth"
    ),
    supertokens_config=SupertokensConfig(
        # https://try.supertokens.com is for demo purposes. Replace this with the address of your core instance (sign up on supertokens.com), or self host a core.
        connection_uri="https://localhost:3567",
        # api_key=<API_KEY(if configured)>
    ),
    framework='fastapi',
    recipe_list=[
        session.init(
            expose_access_token_to_frontend_in_cookie_based_auth=True,
        ),
        emailpassword.init()
    ],
    mode='wsgi' # use wsgi if you are running using gunicorn
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(
    RateLimiterMiddleware,
    max_requests=100,
    time_window=60
)

app.include_router(model_profiles_router, prefix="/v1/model-profiles", tags=["model_profiles"])
app.include_router(user_router, prefix="/v1/user", tags=["users"])
app.include_router(token_router, prefix="/v1/access", tags=["tokens"])
app.include_router(agent_router, prefix="/v1", tags=["agent_forge"])

@app.on_event("startup")
def startup_event():
    print("[AGENTFORGE] Starting up...")
    app.state.redis = interface_interactor.create_redis_connection()

@app.on_event("shutdown")
def shutdown_event():
    app.state.redis.close()

@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    logger.info(f"An error occurred: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"err": exc, "detail": f"{traceback.format_exc()}"})

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://08d6f5767742.ngrok.app"
    ],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)