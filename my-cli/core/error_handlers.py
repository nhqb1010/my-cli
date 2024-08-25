from pprint import pformat
from typing import Any, Callable, Optional

from rich import print as cli_print
from rich.panel import Panel

from core.errors import AppException


def cli_error_handler(
    func: Callable,
    func_args: Optional[dict | None] = None,
    custom_err_message: str = None,
):
    """
    Error handler for CLI commands.

    Args:
        func (Callable): The function to be executed.
        func_args (dict | None): Arguments to be passed to the function.
        custom_err_message (str, optional): Custom error message to be displayed. Defaults to None.
    """

    try:
        if func_args:
            func(**func_args)
        else:
            func()
    except AppException as e:
        error_message = custom_err_message if custom_err_message else e.to_dict()
        print_app_error_message(error_message)

    except Exception as e:
        raise e


def print_app_error_message(error_message: Any) -> str:
    if isinstance(error_message, dict):
        # Separate each key-value pair with a newline
        error_message = "\n\n".join(
            [
                f" 🛑 {key.capitalize()}: [italic red]{value}[/italic red]"
                for key, value in error_message.items()
            ]
        )
    else:
        # Try to pretty print the error message
        try:
            error_message = pformat(error_message)
        except Exception:
            pass

    cli_print(
        Panel(
            f"\n{error_message}\n",
            title="Exception",
            title_align="left",
            border_style="bold red",
            expand=False,
        )
    )
