import typer

from core.errors import AppException
from core.error_handlers import cli_error_handler
from core.rich import cli_iso_print, cli_print
from tools import systems as system_functions
from password import core as password_core, services as password_services

cli_app = typer.Typer()


@cli_app.command(
    "qgenerate",
    help="Quick password generator",
    rich_help_panel="Password Generator",
)
def quick_password_generator():
    password = password_core.generate_safe_token()
    cli_print(f"\nGenerated password: [bold]{password}[bold]\n")


@cli_app.command(
    "generate",
    help="Generate a password with custom options",
    rich_help_panel="Password Generator",
)
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


@cli_app.command(
    "check_pw_connection",
    help="Check the connection to the password server",
    rich_help_panel="Password Manager",
)
def check_password_server_connection():
    def _handle_copy_password():
        try:
            data, _ = password_services.check_server_connection()
            if data is not None:
                cli_iso_print(
                    "✅ Connection to password server is [bold green]successful[bold green]"
                )
                return

        except AppException as _:
            cli_iso_print(
                "❌ Connection to password server [italic red]failed[italic red]"
            )

    cli_error_handler(func=_handle_copy_password)


@cli_app.command(
    "set_password",
    help="Set a new password in the password server",
    rich_help_panel="Password Manager",
)
def set_password():
    def _handle_set_password():
        password_services.set_password(
            password="123",
            username="test",
            domain="test",
        )

    cli_error_handler(func=_handle_set_password)


@cli_app.command(
    "get_password",
    help="Get a password from the password server",
    rich_help_panel="Password Manager",
)
def get_password():
    def _handle_get_password():
        password = password_services.get_password(
            username="test",
            domain="test",
        )
        cli_print(f"\nPassword: [bold green]{password}[bold green]\n")

    cli_error_handler(func=_handle_get_password)
