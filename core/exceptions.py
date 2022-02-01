class StariKolomoniException(Exception):
    """
    Base class for ANY backend exception.
    """


class GeneralBackendException(StariKolomoniException):
    """
    Base exception for any backend code specific exception.
    """
    message: str
    code: int

    def __init__(self, code: int = 500, message: str = ""):
        self.message = message
        self.code = code


class ConfigurationException(StariKolomoniException):
    """
    Raised when an issue with the configuration file or its values arises.
    """
