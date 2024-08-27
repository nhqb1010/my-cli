import json
from typing import Any

from constants.env import env
from core.utils import base64_string_to_string
from core.errors import GithubException
from github import api as github_api
from password.errors import (
    MissingRequiredVarForPasswordServerException,
    PasswordServerLoadException,
    PasswordUsernameExist,
)

COMMON_REQUEST_PAYLOAD = {
    "file_path": env.get("SECRET_FILE_NAME"),
    "owner": env.get("GITHUB_USER"),
    "repo": env.get("SECRET_REPO_NAME"),
    "branch": "main",
    "raise_error": True,
}


def _ensure_necessary_env_vars():
    """
    Ensures that the necessary environment variables are set.

    Raises:
        MissingRequiredVarForPasswordServerException: If any of the required environment variables are not set.
    """
    if not env.get("GITHUB_TOKEN"):
        raise MissingRequiredVarForPasswordServerException(
            "GITHUB_TOKEN is not set in .env file"
        )

    if not env.get("GITHUB_USER"):
        raise MissingRequiredVarForPasswordServerException(
            "GITHUB_USER is not set in .env file"
        )

    if not env.get("SECRET_REPO_NAME"):
        raise MissingRequiredVarForPasswordServerException(
            "SECRET_REPO_NAME is not set in .env file"
        )

    if not env.get("SECRET_FILE_NAME"):
        raise MissingRequiredVarForPasswordServerException(
            "SECRET_FILE_NAME is not set in .env file"
        )


def check_server_connection():
    """
    Check the server connection by getting or creating a file content in a GitHub repository.

    Returns:
        The content of the file.

    Raises:
        Exception: If there is an error while getting or creating the file content.
    """

    _ensure_necessary_env_vars()

    return github_api.get_or_create_a_file_content(
        file_path=env.get("SECRET_FILE_NAME"),
        owner=env.get("GITHUB_USER"),
        repo=env.get("SECRET_REPO_NAME"),
        default_content="{}",
        default_commit_message="Initial commit",
        branch="main",
        raise_error=True,
    )


def get_password_data() -> dict[str, Any]:
    """
    Retrieves the password data from a secret file in a GitHub repository.

    Returns:
        A dictionary containing the password data.

    Raises:
        PasswordServerLoadException: If there is an error loading the password data from the server.
    """

    _ensure_necessary_env_vars()

    try:
        file_content = github_api.get_a_file_content(**COMMON_REQUEST_PAYLOAD)
        return file_content
    except GithubException:
        raise PasswordServerLoadException()


def _set_password_data(
    password: str,
    username: str,
    domain: str,
    old_content: dict[str, Any],
    overwrite_password: bool = False,
):
    """
    Set the password data for a given username and domain.

    Args:
        password (str): The password to be set.
        username (str): The username associated with the password.
        domain (str): The domain associated with the password.
        old_content (dict[str, Any]): The existing password data.
        overwrite_password (bool, optional): Whether to overwrite the password if it already exists. Defaults to False.

    Returns:
        dict[str, Any]: The updated password data.

    Raises:
        PasswordUsernameExist: If the username already exists for the given domain and overwrite_password is False.
    """
    # If domain does not exist, create it
    if not old_content.get(domain):
        old_content[domain] = {}

    # If username does not exist, raise Error if overwrite_password is False
    if not overwrite_password and old_content[domain].get(username):
        raise PasswordUsernameExist()

    old_content[domain][username] = password
    return old_content


def set_password(password: str, username: str, domain: str):
    _ensure_necessary_env_vars()

    try:
        current_data = get_password_data()

        sha = current_data.get("sha")
        string_content = base64_string_to_string(current_data.get("content"))
        dict_content: dict[str, Any] = json.loads(string_content)

        dict_content = _set_password_data(password, username, domain, dict_content)
        new_file_content = json.dumps(dict_content, indent=4)
        github_api.create_update_a_file_content(
            commit_message=f"Update password for {username} at {domain}",
            content=new_file_content,
            sha=sha,
            **COMMON_REQUEST_PAYLOAD,
        )
    except json.JSONDecodeError:
        raise PasswordServerLoadException()


def get_password(username: str, domain: str) -> str:
    _ensure_necessary_env_vars()

    current_data = get_password_data()

    try:
        content = json.loads(base64_string_to_string(current_data.get("content")))

        return content.get(domain, {}).get(username)
    except json.JSONDecodeError:
        raise PasswordServerLoadException()
