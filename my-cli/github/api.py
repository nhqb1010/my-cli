from typing import Any

import requests

from constants.env import env
from core.errors import AppException

GITHUB_TOKEN = env.get("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise AppException("GITHUB_TOKEN is not set")

headers: dict[str, Any] = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}


def _format_repo_response(data: dict[str, Any]):
    repo_info = {
        "id": data.get("id"),
        "name": data.get("name"),
        "url": data.get("html_url"),
        "stars": data.get("stargazers_count"),
        "created_at": data.get("created_at"),
    }

    return repo_info


def get_repos_of_auth_user():
    url = "https://api.github.com/user/repos"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    return [_format_repo_response(repo) for repo in data]
