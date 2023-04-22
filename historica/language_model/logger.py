import logging.config
logging.config.fileConfig('../config/configs/logs/llm.conf')
logger = logging.getLogger(__name__)