import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load .env file
load_dotenv()

CONFIG_DIR = os.environ.get("CONFIG_DIR")
VIDEO_SRC_PATH = os.environ.get("SRC_PATH")
DST_PATH = os.environ.get("DST_PATH")
LLM_CONFIG_FILE = os.path.join(CONFIG_DIR, "models.json")
SESSION_TYPE=os.environ.get("SESSION_TYPE")
REDIS_URL=os.environ.get("REDIS_URL")
REDIS_HOST=os.environ.get("REDIS_HOST")
REDIS_PORT=os.environ.get("REDIS_PORT")
REDIS_DB=os.environ.get("REDIS_DB")
MONGO_HOST=os.environ.get("MONGO_HOST")
MONGO_PORT=os.environ.get("MONGO_PORT")
MONGO_DB=os.environ.get("MONGO_DB")
ALLOWED_ORIGIN=os.environ.get("ALLOWED_ORIGIN")
ALLOW_CREDENTIALS=os.environ.get("ALLOW_CREDENTIALS")
AGENT_SECRET_KEY=os.environ.get("AGENT_SECRET_KEY")
DEEPLAKE_PATH=os.environ.get("DEEPLAKE_PATH")

db = SQLAlchemy()
