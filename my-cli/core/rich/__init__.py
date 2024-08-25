from typing import Any

from rich import print as cli_print


def cli_iso_print(message: str, *args: Any, **kwargs):
    cli_print(f"\n{message}\n", *args, **kwargs)


def cli_iso_print_newline(message: str, *args: Any, **kwargs):
    cli_print(f"{message}\n", *args, **kwargs)
