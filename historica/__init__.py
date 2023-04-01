import os
from flask_sqlalchemy import SQLAlchemy

CONFIG_DIR = os.environ.get("CONFIG_DIR", "/app/historica/config")
VIDEO_SRC_PATH = os.environ.get("SRC_PATH", "/app/agent_n/web/public/videos")
VIDEO_DST_PATH = os.environ.get("DST_PATH", "/app/cache")
DEFAULT_MAX_NEW_TOKENS = os.environ.get("DEFAULT_MAX_NEW_TOKENS", 2048)
CONFIG_FILE = os.path.join(CONFIG_DIR, "models.json")

db = SQLAlchemy()
