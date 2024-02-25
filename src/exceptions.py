from fastapi import HTTPException


class TokenParseError(HTTPException):
    def __init__(self, detail: str = "Failed to parse token", status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class InvalidCredentials(HTTPException):
    def __init__(self, detail: str = "Invalid credentials", status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)
