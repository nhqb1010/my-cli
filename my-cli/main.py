import typer

from github.cli import cli_app as github_cli_app
from github.automate_cli import cli_app as github_automate_cli_app

app = typer.Typer()

app.add_typer(github_cli_app, name="github", help="Interact directly with GitHub")
app.add_typer(
    github_automate_cli_app, name="github-automate", help="Automate tasks on GitHub"
)


if __name__ == "__main__":
    app()
