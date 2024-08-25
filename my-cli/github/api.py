import json
from pprint import pformat
from typing import Any, Optional

import requests
from rich import print as cli_print

from core.errors import GithubException
from core.utils import string_to_base64_string
from github.constants import (
    DEFAULT_HEADERS,
    ACCEPTABLE_GITHUB_METHODS,
    ACCEPTABLE_GITHUB_STATUS_CODES,
)


def handle_github_error_for_cli(response: requests.Response, url: str, method: str):
    """
    Handles errors returned by the GitHub API.

    Args:
        response (requests.Response): The response object returned by the API request.
        url (str): The URL of the API request.
        method (str): The HTTP method used for the API request.
    """
    message = response.text
    code = response.status_code
    if code == 404:
        message = "Branch/File path not found"
    elif code == 400:
        message = "Bad request, invalid data or query param"

    error_data = {
        "status_code": code,
        "message": message,
        "url": url,
        "method": method,
    }
    cli_print(
        f"[italic red]\n\nGithub API Error: \n{pformat(error_data, sort_dicts=False)}[/italic red]"
    )


def handle_github_api(
    method: str,
    url: str,
    headers: dict[str, Any] = None,
    query_params: dict[str, Any] = None,
    data: dict[str, Any] = None,
    retry: int = 3,
    raise_error: bool = False,
) -> dict[str, Any] | None:
    """
    Sends a request to the GitHub API.

    Args:
        method (str): The HTTP method to use for the request.
        url (str): The URL of the API endpoint.
        headers (dict[str, Any], optional): Additional headers to include in the request. Defaults to None.
        query_params (dict[str, Any], optional): Query parameters to include in the request. Defaults to None.
        data (dict[str, Any], optional): The request payload. Defaults to None.
        retry (int, optional): The number of times to retry the request in case of failure. Defaults to 3.
        raise_error (bool, optional): If set to True, raises an exception if the request fails. Defaults to False.

    Returns:
        dict[str, Any]: The JSON response from the API.

    Raises:
        ValueError: If the specified HTTP method is not supported.
        AppException: If the API request fails after the specified number of retries.
    """
    if method not in ACCEPTABLE_GITHUB_METHODS:
        raise ValueError(f"Method {method} is not supported")

    headers = DEFAULT_HEADERS if headers is None else {**DEFAULT_HEADERS, **headers}

    if data:
        data = {k: v for k, v in data.items() if v is not None}

    response = None
    for _ in range(retry):
        response = requests.request(
            method, url, headers=headers, params=query_params, data=json.dumps(data)
        )

        if response.status_code in ACCEPTABLE_GITHUB_STATUS_CODES:
            return response.json()

    if raise_error:
        raise GithubException(
            status_code=response.status_code,
            data=response.json(),
            message="Failed to make a request to the GitHub API",
        )

    handle_github_error_for_cli(response, url, method)


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
    response = requests.get(url, headers=DEFAULT_HEADERS)
    response.raise_for_status()
    data = response.json()

    return [_format_repo_response(repo) for repo in data]


def get_a_file_content(
    file_path: str,
    owner: str,
    repo: str,
    branch: str = "main",
    raise_error: bool = False,
):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

    query_params = None
    if branch:
        query_params = {"ref": branch}

    return handle_github_api(
        "GET", url, query_params=query_params, raise_error=raise_error
    )


def create_update_a_file_content(
    file_path: str,
    owner: str,
    repo: str,
    commit_message: str,
    content: str,
    sha: Optional[str],
    branch: Optional[str] = None,
    raise_error: bool = False,
):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

    data = {
        "message": commit_message,
        "content": string_to_base64_string(content),
        "branch": branch,
        "sha": sha,
    }

    return handle_github_api("PUT", url, data=data, raise_error=raise_error)


def get_or_create_a_file_content(
    file_path: str,
    owner: str,
    repo: str,
    default_content: str = "",
    default_commit_message: str = "Initial commit",
    branch: str = "main",
    raise_error: bool = False,
) -> tuple[dict[str, Any] | None, bool]:
    """
    Retrieves the content of a file from a GitHub repository, or creates a new file with the specified content if the file does not exist.
    Args:
        file_path (str): The path of the file.
        owner (str): The owner of the GitHub repository.
        repo (str): The name of the GitHub repository.
        default_content (str, optional): The default content to use when creating a new file. Defaults to an empty string.
        default_commit_message (str, optional): The commit message to use when creating a new file. Defaults to "Initial commit".
        branch (str, optional): The branch to use. Defaults to "main".
        raise_error (bool, optional): Whether to raise an error if the file does not exist. Defaults to False.
    Returns:
        tuple[dict[str, Any] | None, bool]: A tuple containing the file content and a boolean indicating whether a new file was created.
    Raises:
        GithubException: If an error occurs while retrieving the file content and `raise_error` is set to True.
    """

    try:
        return get_a_file_content(
            file_path=file_path,
            owner=owner,
            repo=repo,
            branch=branch,
            raise_error=raise_error,
        ), False

    except GithubException as e:
        if e.status_code != 404:
            raise e

    create_update_a_file_content(
        file_path=file_path,
        owner=owner,
        repo=repo,
        commit_message=default_commit_message,
        content=default_content,
        sha=None,
        branch=branch,
        raise_error=raise_error,
    )

    return {"content": default_content}, True
