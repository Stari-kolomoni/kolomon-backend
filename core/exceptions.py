
class GeneralBackendException(Exception):
    message: str
    code: int

    def __init__(self, code: int = 500, message: str = ""):
        self.message = message
        self.code = code
