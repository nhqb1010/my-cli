from typing import TypedDict

from dotenv import dotenv_values

ENV_PATH = ".env"


class Env(TypedDict):
    GITHUB_TOKEN: str


env: Env = dotenv_values(ENV_PATH)
