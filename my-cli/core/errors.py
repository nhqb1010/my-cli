from typing import Any, Optional


class AppException(Exception):
    def __init__(self, message: str, code: Optional[int] = 1010):
        self.message = message
        self.code = code

    def to_dict(self):
        return dict(message=self.message, code=self.code)


class GithubException(AppException):
    def __init__(
        self,
        status_code: int,
        data: dict[str, Any],
        message: str,
        code: Optional[int] = 1011,
    ):
        self.status_code = status_code
        self.data = data
        super().__init__(message, code)
