from typing import Any

from constants.env import env
from core.errors import AppException

GITHUB_TOKEN = env.get("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise AppException("GITHUB_TOKEN is not set")

DEFAULT_HEADERS: dict[str, Any] = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}


ACCEPTABLE_GITHUB_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
ACCEPTABLE_GITHUB_STATUS_CODES = [200, 201]
