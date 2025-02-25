class ProcessException(Exception):
    """
    Represents an exception that occurred during the process.
    """

    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
