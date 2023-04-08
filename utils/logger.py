import logging
import os


LOGGER_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_FILE_PATH = "logs/output.log"

logger = logging.getLogger(__name__)
formatter = logging.Formatter(LOGGER_FORMAT)
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
