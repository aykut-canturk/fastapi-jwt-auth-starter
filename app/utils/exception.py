from fastapi.exceptions import RequestValidationError, FastAPIError


class ValidationError(RequestValidationError):
    def __init__(self, *messages: str):
        self.message = " ".join(messages) if messages else "Validation error"
        super().__init__(self)

    def __str__(self):
        return self.message


class CustomError(FastAPIError):
    def __init__(self, *messages: str):
        self.message = " ".join(messages) if messages else "Unknown error"
        super().__init__(self)

    def __str__(self):
        return self.message
