import typer
from rich import print as cli_print
from requests import RequestException

from core.utils import (
    base64_string_to_string,
    format_current_time,
    get_file_name_and_extension,
    get_random_animal_icon,
)
from github import api as github_service


cli_app = typer.Typer()

AUTOMATE_GIT_REPO = "automation"
AUTOMATE_GIT_REPO_FILE = "my_generated_commit.txt"
AUTOMATE_GIT_AUTH_USER = "nhqb1010"


def handle_create_new_file(current_time: str) -> str:
    """
    Creates a new file name based on the current time.

    Args:
        current_time (str): The current time in string format.

    Returns:
        str: The new file name with the current time appended.

    """
    file_name, file_extension = get_file_name_and_extension(AUTOMATE_GIT_REPO_FILE)

    return f"{file_name}_{current_time}.{file_extension}"


@cli_app.command("commit", help="Generate an auto commit to the auth user github")
def generate_commit(
    new: bool = typer.Option(
        False, "--new", help="If set, will create a new file if not exists"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="If set, will print old content"
    ),
):
    # Try fetching the file content
    cli_print(
        f"==> Fetching current file content: file='{AUTOMATE_GIT_REPO_FILE}', repo='{AUTOMATE_GIT_REPO}' ..."
    )
    file_info = None
    try:
        file_info = github_service.get_a_file_content(
            file_path=AUTOMATE_GIT_REPO_FILE,
            owner=AUTOMATE_GIT_AUTH_USER,
            repo=AUTOMATE_GIT_REPO,
        )
    except RequestException as e:
        if e.response.status_code == 404:
            cli_print("\n[italic red]ERROR: File not found.[/italic red]")

            if not new:
                return
        else:
            cli_print(f"Github API Error: {e}")
            return

    current_time = format_current_time()
    commit_message = f"From QB_CLI, Auto commit at {current_time}"
    if file_info:
        content = base64_string_to_string(file_info.get("content"))
        sha = file_info.get("sha")
        if verbose:
            cli_print(f"\n==> Existing content: [bold green]'{content}'[/bold green]")

        cli_print(f"\n==> Updating file content: file='{AUTOMATE_GIT_REPO_FILE}' ...")
        animal_icon = get_random_animal_icon()
        updated_content = (
            f"{content}\n- {animal_icon} Auto commit at {current_time} by QB CLI"
        )
        data = github_service.create_update_a_file_content(
            file_path=AUTOMATE_GIT_REPO_FILE,
            owner=AUTOMATE_GIT_AUTH_USER,
            repo=AUTOMATE_GIT_REPO,
            commit_message=commit_message,
            content=updated_content,
            sha=sha,
        )
        if data.get("content"):
            cli_print("\n==> Successfully\n")
        else:
            cli_print("\n[italic red]ERROR: Failed to update file.[/italic red]")
            cli_print(data)

    else:
        new_file = handle_create_new_file(current_time)

        cli_print(f"\n==> Creating new file: [bold green]'{new_file}'[/bold green] ...")
        data = github_service.create_update_a_file_content(
            file_path=new_file,
            owner=AUTOMATE_GIT_AUTH_USER,
            repo=AUTOMATE_GIT_REPO,
            commit_message=commit_message,
            content="This is a new file",
            branch="main",
            sha=None,
        )
        if data.get("content"):
            cli_print("\n==> Successfully\n")
        else:
            cli_print("\n[italic red]ERROR: Failed to create new file.[/italic red]")
