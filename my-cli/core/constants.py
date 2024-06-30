from enum import Enum


class DefaultOutputFormats(str, Enum):
    json = "json"
    table = "table"
    csv = "csv"
