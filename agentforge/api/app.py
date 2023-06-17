from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

### Init Fast API Function
def init_api():
  app = FastAPI()
  cors_origins = ["*"]
  app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
  )
  return app