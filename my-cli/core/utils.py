import csv
import sys
import json
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
