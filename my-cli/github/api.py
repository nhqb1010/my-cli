import json
from typing import Any, Optional

import requests

from constants.env import env
from core.errors import AppException
from core.utils import string_to_base64_string

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


def get_a_file_content(file_path: str, owner: str, repo: str, branch: str = "main"):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

    if branch:
        url += f"?ref={branch}"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    return data


def create_update_a_file_content(
    file_path: str,
    owner: str,
    repo: str,
    commit_message: str,
    content: str,
    sha: Optional[str],
    branch: Optional[str] = None,
):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

    data = {
        "message": commit_message,
        "content": string_to_base64_string(content),
        "branch": branch,
        "sha": sha,
    }

    data = {k: v for k, v in data.items() if v is not None}

    response = requests.put(url, headers=headers, data=json.dumps(data))
    data = response.json()

    return data
