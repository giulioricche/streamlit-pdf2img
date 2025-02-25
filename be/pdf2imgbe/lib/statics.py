from enum import Enum

RESULTS_FOLDER = "results"
IMAGE_FILE_EXTENSION = "PNG"
IMAGE_FILENAME_FORMAT = "Page_{}." + IMAGE_FILE_EXTENSION


class EnvKey:
    """
    Environment variable keys.
    """

    SIMULATE_PROCESS_DELAY_KEY = "SIMULATE_PROCESS_DELAY"
    LOG_LEVEL_KEY = "LOG_LEVEL"


class ConversionStatus(Enum):
    """
    Conversion status.
    """

    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
