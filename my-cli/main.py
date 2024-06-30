import typer

from github.cli import cli_app as github_cli_app

app = typer.Typer()

app.add_typer(github_cli_app, name="github")


if __name__ == "__main__":
    app()
