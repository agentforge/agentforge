import os
from flask_sqlalchemy import SQLAlchemy

CONFIG_DIR = os.environ.get("CONFIG_DIR", "/app/agentforge/config")
VIDEO_SRC_PATH = os.environ.get("SRC_PATH", "/app/agentforge/web/public/videos")
DST_PATH = os.environ.get("DST_PATH", "/app/cache")
AUDIO_DST_PATH = DST_PATH + "/uploads/audio"
if not os.path.exists(AUDIO_DST_PATH):
    os.makedirs(AUDIO_DST_PATH)
DEFAULT_MAX_NEW_TOKENS = os.environ.get("DEFAULT_MAX_NEW_TOKENS", 2048)
LLM_CONFIG_FILE = os.path.join(CONFIG_DIR, "models.json")

db = SQLAlchemy()
