from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

### Init Fast API Function
def init_api():
  description = """
    AgentForge API 🚀
    Documentation for Public Facing API
  """
  app = FastAPI(
  title="AgentForge",
  description=description,
  version="0.0.1",
  contact={
        "name": "Admin",
        "url": "http://agentforge.ai",
        "email": "info@agentforge.ai",
  },
  license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
  },
  )
  cors_origins = ["*"]
  app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
  )
  return app