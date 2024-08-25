import json

from constants.env import env
from core.utils import base64_string_to_string
from core.errors import GithubException
from github import api as github_api
from password.errors import (
    MissingRequiredVarForPasswordServerException,
    PasswordServerLoadException,
)


def _ensure_necessary_env_vars():
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


def get_password_data():
    _ensure_necessary_env_vars()

    try:
        file_content = github_api.get_a_file_content(
            file_path=env.get("SECRET_FILE_NAME"),
            owner=env.get("GITHUB_USER"),
            repo=env.get("SECRET_REPO_NAME"),
            raise_error=True,
        )
        return file_content
    except GithubException:
        raise PasswordServerLoadException()


def set_password(password: str, username: str, domain: str):
    _ensure_necessary_env_vars()

    current_data = get_password_data()

    try:
        sha = current_data.get("sha")
        content = json.loads(base64_string_to_string(current_data.get("content")))

        # Set the password
        if not content.get(domain):
            content[domain] = {}
            content[domain][username] = password
        elif not content[domain].get(username):
            content[domain][username] = password
        else:
            content[domain][username] = password

        new_file_content = json.dumps(content, indent=4)
        github_api.create_update_a_file_content(
            file_path=env.get("SECRET_FILE_NAME"),
            owner=env.get("GITHUB_USER"),
            repo=env.get("SECRET_REPO_NAME"),
            commit_message=f"Update password for {username} at {domain}",
            content=new_file_content,
            sha=sha,
            branch="main",
            raise_error=True,
        )
    except json.JSONDecodeError as e:
        print(e)
        raise PasswordServerLoadException()


def get_password(username: str, domain: str) -> str:
    _ensure_necessary_env_vars()

    current_data = get_password_data()

    try:
        content = json.loads(base64_string_to_string(current_data.get("content")))

        return content.get(domain, {}).get(username)
    except json.JSONDecodeError:
        raise PasswordServerLoadException()
