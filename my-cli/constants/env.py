from typing import TypedDict

from dotenv import dotenv_values

ENV_PATH = ".env"


class Env(TypedDict):
    GITHUB_TOKEN: str
    GITHUB_USER: str
    SECRET_REPO_NAME: str | None
    SECRET_FILE_NAME: str | None


env: Env = dotenv_values(ENV_PATH)
