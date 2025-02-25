import os
import logging

from lib.statics import EnvKey

# Set up logging
logger = logging.getLogger("streamlit-pdf2img")
logger.setLevel(os.getenv(EnvKey.LOG_LEVEL_KEY))
logging.basicConfig(
    format=" [%(levelname)s] %(asctime)s [%(filename)s %(funcName)s@%(lineno)d]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
