# main.py

from agentforge.api.model_profiles import router as model_profiles_router
from agentforge.api.agent import router as agent_router
from agentforge.api.user import router as user_router
from agentforge.api.app import init_api
from agentforge.utils import logger

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response

app = init_api()
app.add_middleware(LoggingMiddleware)
app.include_router(model_profiles_router, prefix="/v1/model_profiles", tags=["model_profiles"])
app.include_router(user_router, prefix="/v1/user", tags=["users"])
app.include_router(agent_router, prefix="", tags=["main"])


@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    logger.error(f"An error occurred: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
