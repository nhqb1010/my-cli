from typing import Any, Optional

import typer
from rich import print as cli_print

from core.utils import (
    base64_string_to_string,
    format_current_time,
    get_file_name_and_extension,
    get_random_animal_icon,
)
from github import api as github_service
from core.rich.console import process_function_with_status


cli_app = typer.Typer()

AUTOMATE_GIT_REPO = "automation"
AUTOMATE_GIT_REPO_FILE = "my_generated_commit.txt"
AUTOMATE_GIT_AUTH_USER = "nhqb1010"


def _try_fetch_file_content() -> dict[str, Any] | None:
    file_info = process_function_with_status(
        func=github_service.get_a_file_content,
        args={
            "file_path": AUTOMATE_GIT_REPO_FILE,
            "owner": AUTOMATE_GIT_AUTH_USER,
            "repo": AUTOMATE_GIT_REPO,
        },
        loading_message=f"==> Fetching current file content: file='{AUTOMATE_GIT_REPO_FILE}', repo='{AUTOMATE_GIT_REPO}'",
    )

    if file_info:
        cli_print(f"✅ File '{AUTOMATE_GIT_REPO_FILE}' fetched successfully\n")

    return file_info


def _update_file(file_info: dict[str, Any] | None, verbose: Optional[bool] = False):
    content = base64_string_to_string(file_info.get("content"))
    sha = file_info.get("sha")
    if verbose:
        cli_print(f"\n==> Existing content: '{content}'\n")

    current_time = format_current_time()
    commit_message = f"From QB_CLI, Auto commit at {current_time}"
    animal_icon = get_random_animal_icon()
    updated_content = (
        f"{content}\n- {animal_icon} Auto commit at {current_time} by QB CLI"
    )

    data = process_function_with_status(
        func=github_service.create_update_a_file_content,
        args={
            "file_path": AUTOMATE_GIT_REPO_FILE,
            "owner": AUTOMATE_GIT_AUTH_USER,
            "repo": AUTOMATE_GIT_REPO,
            "commit_message": commit_message,
            "content": updated_content,
            "sha": sha,
        },
        loading_message=f"==> Updating file content: file='{AUTOMATE_GIT_REPO_FILE}' ...",
    )

    if data.get("content"):
        cli_print("\n✅ Updated Successfully\n")
    else:
        cli_print("\n[italic red]ERROR: Failed to update file.[/italic red]")
        cli_print(data)

    return data


def _create_new_file(verbose: Optional[bool] = False):
    current_time = format_current_time()
    file_name, file_extension = get_file_name_and_extension(AUTOMATE_GIT_REPO_FILE)
    new_file_name = f"{file_name}_{current_time}.{file_extension}"
    content = f"{get_random_animal_icon()} New file created by QB CLI\n"

    data = process_function_with_status(
        func=github_service.create_update_a_file_content,
        args={
            "file_path": new_file_name,
            "owner": AUTOMATE_GIT_AUTH_USER,
            "repo": AUTOMATE_GIT_REPO,
            "commit_message": f"From QB_CLI, Auto commit at {current_time}",
            "content": content,
            "sha": None,
        },
        loading_message=f"==> Creating new file: [bold green]'{new_file_name}'[/bold green]",
    )

    if data is not None:
        if verbose:
            cli_print(f"\n==> New content: [bold green]'{content}'[/bold green]")

        cli_print("\n==> Successfully\n")


@cli_app.command("commit", help="Generate an auto commit to the auth user github")
def generate_commit(
    new: bool = typer.Option(
        False, "--new", help="If set, will create a new file if not exists"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="If set, print file contents"
    ),
):
    # Fetch file content if exists
    file_info = _try_fetch_file_content()
    if file_info is None and not new:
        cli_print(
            f"[italic red]ERROR: File '{AUTOMATE_GIT_REPO_FILE}' not found in repo '{AUTOMATE_GIT_REPO}'[/italic red]"
        )
        return

    # Update file content if file exists
    if file_info:
        _update_file(file_info, verbose)

    # Create new file if not exists
    else:
        _create_new_file(verbose)
