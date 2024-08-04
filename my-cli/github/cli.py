import typer
from rich import print as cli_print

from core.constants import DefaultOutputFormats
from core.utils import print_with_formats
from github import api as github_service

cli_app = typer.Typer()


@cli_app.command("list-repos", help="List all repositories of the authenticated user")
def list_repos_of_auth_user(
    output: DefaultOutputFormats = typer.Option(
        DefaultOutputFormats.json, "--output", "-o", help="Output format"
    ),
):
    data = github_service.get_repos_of_auth_user()
    print_with_formats(data, output)


@cli_app.command("get-file", help="Get the content of a file in a repository")
def get_file_content(
    file_path: str = typer.Option(..., "--file", "-f", help="Path to the file"),
    username: str = typer.Option(
        ..., "--username", "-u", help="Owner of the repository"
    ),
    repo: str = typer.Option(..., "--repo", "-r", help="Repository name"),
    branch: str = typer.Option("main", "--branch", "-b", help="Branch name"),
):
    data = github_service.get_a_file_content(file_path, username, repo, branch)
    cli_print(data)


@cli_app.command("update-file", help="Update the content of a file in a repository")
def update_file_content(
    file_path: str = typer.Option(..., "--file", "-f", help="Path to the file"),
    username: str = typer.Option(
        ..., "--username", "-u", help="Owner of the repository"
    ),
    repo: str = typer.Option(..., "--repo", "-r", help="Repository name"),
    branch: str = typer.Option("main", "--branch", "-b", help="Branch name"),
):
    data = github_service.get_a_file_content(file_path, username, repo, branch)
    cli_print(data)
