import typer

from github.cli import cli_app as github_cli_app
from github.automate_cli import cli_app as github_automate_cli_app
from password.cli import cli_app as password_cli_app

app = typer.Typer(pretty_exceptions_show_locals=True)

app.add_typer(github_cli_app, name="github", help="Interact directly with GitHub")
app.add_typer(
    github_automate_cli_app, name="github-automate", help="Automate tasks on GitHub"
)
app.add_typer(
    password_cli_app, name="password", help="Password manager & password generator"
)


if __name__ == "__main__":
    app()
