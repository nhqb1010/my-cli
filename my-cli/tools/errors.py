from typing import Optional

from core.errors import AppException


class ToolException(AppException):
    pass


class CopyToClipboardException(ToolException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(
            message=message if message else "Error while copy text to clipboard.",
            code=3000,
        )
