from enum import Enum

IMAGE_FILE_EXTENSION = "PNG"
IMAGE_FILENAME_FORMAT = "Page_{}." + IMAGE_FILE_EXTENSION


class EnvKey:
    """
    Environment variable keys.
    """

    LOG_LEVEL_KEY = "LOG_LEVEL"
    BE_HOST_KEY = "BE_SERVICE_HOST"
    BE_PORT_KEY = "BE_APP_PORT"


class ConversionStatus(Enum):
    """
    Conversion status.
    """

    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
