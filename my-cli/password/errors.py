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


class MissingRequiredVarForPasswordServerException(PasswordException):
    def __init__(self, message: Optional[str] = None):
        message = (
            message
            if message
            else "Missing required environment variable for password server."
        )
        super().__init__(message, code=2002)


class PasswordServerLoadException(PasswordException):
    def __init__(self, message: Optional[str] = None):
        message = (
            message if message else "Error while loading password data from server."
        )
        super().__init__(message, code=2003)


class PasswordUsernameExist(PasswordException):
    def __init__(self, message: Optional[str] = None):
        message = message if message else "Username already exist for this domain."
        super().__init__(message, code=2004)
