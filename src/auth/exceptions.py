from fastapi import HTTPException


class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Authentication failed", status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class UserAlreadyExists(HTTPException):
    def __init__(self, detail: str = "User with this email already exists!", status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class UserDoesntExist(HTTPException):
    def __init__(self, detail: str = "This user does not exist", status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class InvalidPassword(HTTPException):
    def __init__(self, detail: str = "Invalid password", status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)
