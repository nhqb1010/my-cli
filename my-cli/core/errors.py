from typing import Optional


class AppException(Exception):
    def __init__(self, message: str, code: Optional[int] = 1010):
        self.message = message
        self.code = code

    def to_dict(self):
        return dict(message=self.message, code=self.code)
