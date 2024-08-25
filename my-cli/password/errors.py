from typing import Optional

from core.errors import PasswordException


class InvalidPasswordOptionsException(PasswordException):
    def __init__(self, message: Optional[str] = None):
        message = (
            message
            if message
            else "Password must contain at least one of the following: lowercase, uppercase"
        )
        super().__init__(message, code=2001)


class InvalidPasswordLengthException(PasswordException):
    def __init__(self, message: Optional[str] = None):
        message = message if message else "Invalid password length."
        super().__init__(message, code=2000)
