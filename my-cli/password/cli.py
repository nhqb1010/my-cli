import typer
from rich import print as cli_print

from core.error_handlers import cli_error_handler
from tools import systems as system_functions
from password import core as password_core

cli_app = typer.Typer()


@cli_app.command("qgenerate", help="Quick password generator")
def quick_password_generator():
    password = password_core.generate_safe_token()
    cli_print(f"\nGenerated password: [bold]{password}[bold]\n")


@cli_app.command("generate", help="Generate a password with custom options")
def generate_password(
    length: int = typer.Option(20, "--length", "-l", help="Length of the password"),
    exclude_lowercase: bool = typer.Option(
        False, "--exclude-lowercase", help="Exclude lowercase letters"
    ),
    exclude_uppercase: bool = typer.Option(
        False, "--exclude-uppercase", help="Exclude uppercase letters"
    ),
    exclude_numbers: bool = typer.Option(
        False, "--exclude-numbers", help="Exclude numbers"
    ),
    exclude_special: bool = typer.Option(
        False, "--exclude-special", help="Exclude special characters"
    ),
    copy_to_clipboard: bool = typer.Option(
        False, "--copy", help="Copy the generated password to clipboard"
    ),
    hide_password: bool = typer.Option(
        False, "--hide", "-h", help="Hide the generated password"
    ),
):
    def _handle_generate_password():
        password = password_core.generate_password(
            length=length,
            with_lowercase=not exclude_lowercase,
            with_uppercase=not exclude_uppercase,
            with_number=not exclude_numbers,
            with_special=not exclude_special,
        )

        message = f"\nGenerated password: [bold green]{password}[bold green]\n"
        if hide_password:
            message = f"\nGenerated password [italic](hidden)[italic]: [bold green]{'*' * len(password)}[bold green]\n"

        cli_print(message)

        if copy_to_clipboard:
            success = system_functions.copy_to_clipboard(password)

            if success:
                cli_print("[italic]✨ Password copied to clipboard. ✨[italic]\n")

    cli_error_handler(func=_handle_generate_password)


@cli_app.command("test")
def test():
    cli_print(password_core.generate_safe_token_urls())
