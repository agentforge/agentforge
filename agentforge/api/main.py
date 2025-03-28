# Hack for deeplake issue
import deeplake
deeplake.__version__ = '3.6.2'

# main.py
import os
from fastapi import Request, WebSocket
from agentforge.api.model_profiles import router as model_profiles_router
from agentforge.api.agent import router as agent_router
from agentforge.api.user import router as user_router
from agentforge.api.ws import router as ws_router
from agentforge.api.sim import router as sim_router
# from agentforge.api.events import router as events_router
from agentforge.api.subscription import router as subscription_router
from agentforge.api.supertokens import override_functions
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
from supertokens_python.recipe import dashboard
from agentforge.api.supertokens import override_emailpassword_functions
from supertokens_python.ingredients.emaildelivery.types import EmailDeliveryConfig, SMTPSettingsFrom, SMTPSettings

from typing import Dict, Deque
from collections import deque
from datetime import datetime, timedelta

# from celery_config import celery_app

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

# db = interface_interactor.get_interface("db")
# d = DomainBuilder(db)
# d.upload_documents_from_folder('garden', '/app/agentforge/agentforge/config/configs/planner/domains/garden', 'p_example')

app = init_api()
app.add_middleware(get_middleware())

smtp_settings = SMTPSettings(
    host="smtp.sendgrid.net",
    port=465,
    from_=SMTPSettingsFrom(
        name="GreenSage",
        email="noreply@greensage.app"
    ),
    password="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",
    secure=True,
    username="apikey"
)
api_domain = os.getenv("API_DOMAIN")
website_domain = os.getenv("WEBSITE_DOMAIN")

# Supertokens
init(
    app_info=InputAppInfo(
        app_name="GreenSage",
        # api_domain="https://mite-inspired-snipe.ngrok-free.app",
        api_domain=api_domain,
        # website_domain="https://greensage.app/",
        website_domain=website_domain,
        api_base_path="/api/auth",
        website_base_path="/auth"
    ),
    supertokens_config=SupertokensConfig(
        # https://try.supertokens.com is for demo purposes. Replace this with the address of your core instance (sign up on supertokens.com), or self host a core.
        connection_uri="http://supertokens:3567",
        # api_key=<API_KEY(if configured)>
    ),
    framework='fastapi',
    recipe_list=[
        session.init(
            expose_access_token_to_frontend_in_cookie_based_auth=True,
            override=session.InputOverrideConfig(
                functions=override_functions
            )
        ),
        emailpassword.init(
            override=emailpassword.InputOverrideConfig(
                functions=override_emailpassword_functions
            ),
            email_delivery=EmailDeliveryConfig(
                service=emailpassword.SMTPService(
                    smtp_settings=smtp_settings
                )
            )
        ),
        dashboard.init(),
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
app.include_router(agent_router, prefix="/v1", tags=["agent_forge"])
app.include_router(subscription_router, prefix="/v1", tags=["subscription"])
app.include_router(ws_router, prefix="/v1", tags=["ws"])
app.include_router(sim_router, prefix="/v1", tags=["sim"])
# app.include_router(events_router, prefix="/v1/events", tags=["events"])

@app.on_event("startup")
def startup_event():
    print("[AGENTFORGE] Starting up...")
    app.state.redis = interface_interactor.create_redis_connection()
    
    # Start Celery Beat schedule
    # celery_app.worker_main(['beat', '--detach'])

    # Start Celery task worker
    # celery_app.worker_main(['-A', 'main', 'worker', '--loglevel=info', '--concurrency=1'])

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
        website_domain,
        "https://agentforge.ngrok.dev",
        "https://agentforge-client-git-dev-agentforge-dev.vercel.app",
        "https://agentforge-client-4y81f0wsy-agentforge-dev.vercel.app"
        "https://agentforge-client.vercel.app",
        "https://greensage.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"] + get_all_cors_headers(),
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    to_print = {
        "method": request.method,
        "url": request.url._url,
        "headers": dict(request.headers),
        # ... add other fields as needed
    }
    logger.info(f"{to_print}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
