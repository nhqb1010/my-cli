import csv
import sys
import json
import base64
from datetime import datetime
from pathlib import Path
from typing import Any

from rich import print_json
from rich.table import Table
from rich.console import Console

from core.constants import DefaultOutputFormats
from core.errors import AppException


def print_with_formats(data: list[dict[str, Any]], output_format: DefaultOutputFormats):
    fieldnames = data[0].keys()

    if output_format == DefaultOutputFormats.json:
        print_json(json.dumps(data))
    elif output_format == DefaultOutputFormats.table:
        table = Table()

        # Index column
        table.add_column("Index", style="cyan")

        # Add headers
        for fieldname in fieldnames:
            table.add_column(str(fieldname))

        for index, row in enumerate(data):
            _row = [str(cell) for cell in row.values()]
            table.add_row(str(index + 1), *_row)

        console = Console()
        console.print(table)
    elif output_format == DefaultOutputFormats.csv:
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    else:
        raise AppException(f"Output format {output_format} is not supported")


def string_to_base64_string(s: str) -> str:
    """
    Converts a string to a base64 encoded string.

    Args:
        s (str): The input string to be converted.

    Returns:
        str: The base64 encoded string.

    """
    return base64.b64encode(bytes(s, "utf-8")).decode("utf-8")


def base64_string_to_string(s: str) -> str:
    """
    Converts a base64 encoded string to a string.

    Args:
        s (str): The base64 encoded string to be converted.

    Returns:
        str: The decoded string.

    """
    return base64.b64decode(s).decode("utf-8")


def format_current_time(string_formatter: str = "%d_%m_%Y_%H_%M_%S"):
    """
    Formats the current date and time according to the specified string formatter.

    Parameters:
        string_formatter (str): The format string to be used for formatting the date and time.
                                Defaults to "%d_%m_%Y_%H_%M_%S".

    Returns:
        str: The formatted date and time string.
    """
    # Get the current date and time
    now = datetime.now()

    # Format the date and time as per the required format
    formatted_time = now.strftime(string_formatter)

    return formatted_time


def get_file_name_and_extension(file_path: str) -> tuple[str, str]:
    """
    Extracts the file name without extension and the extension from the given file path.

    Args:
        file_path (str): The path of the file.

    Returns:
        tuple[str, str]: A tuple containing the file name without extension and the extension.
    """
    # Create a Path object
    path = Path(file_path)

    # Extract the file name without extension and the extension
    file_name = path.stem
    file_extension = path.suffix

    return file_name, file_extension


def get_random_animal_icon() -> str:
    icons = [
        "🐶",
        "🐱",
        "🐭",
        "🐹",
        "🐰",
        "🦊",
        "🐻",
        "🐼",
        "🐨",
        "🐯",
        "🦁",
        "🐮",
        "🐷",
        "🐸",
        "🐵",
        "🐔",
        "🐧",
        "🐦",
        "🐤",
        "🐣",
        "🐥",
        "🦆",
        "🦅",
        "🦉",
        "🦇",
        "🐺",
        "🐗",
        "🐴",
        "🦄",
        "🐝",
        "🐛",
        "🦋",
        "🐌",
        "🐞",
        "🐜",
        "🦗",
        "🕷",
        "🦂",
        "🦟",
        "🦠",
        "🐢",
        "🐍",
        "🦎",
        "🦖",
        "🦕",
        "🐙",
        "🦑",
        "🦐",
        "🦀",
        "🐡",
        "🐠",
        "🐟",
        "🐬",
        "🐳",
        "🐋",
        "🦈",
        "🐊",
        "🐅",
        "🐆",
        "🦓",
        "🦍",
        "🦧",
        "🦣",
        "🐘",
        "🦛",
        "🦏",
        "🐪",
        "🐫",
        "🦒",
        "🦘",
        "🐃",
        "🐂",
        "🐄",
        "🐎",
        "🐖",
        "🐏",
        "🐑",
        "🦙",
        "🐐",
        "🦌",
        "🐕",
        "🐩",
        "🦮",
        "🐕‍🦺",
        "🦡",
        "🦨",
        "🦥",
        "🦦",
        "🦤",
        "🦭",
        "🦩",
        "🦜",
        "🦚",
        "🦇",
        "🐓",
        "🦃",
        "🦢",
        "🦜",
        "🦩",
    ]
    return icons[datetime.now().second % len(icons)]
