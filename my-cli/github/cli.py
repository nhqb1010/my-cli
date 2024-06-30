import typer

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
