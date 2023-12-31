"""Utility functions and classes for this module found here."""

from openpyxl.utils import column_index_from_string, get_column_letter


def pyindex_for(col_name: str) -> int:
    """Examples: given "A", this returns 0, given "AA" this returns 26."""
    return column_index_from_string(col_name.upper()) - 1


def column_letter_for(pyindex: int):
    """Examples: given 0, this returns "A", given 26 this returns "AA"."""
    return get_column_letter(pyindex + 1)
