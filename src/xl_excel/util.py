"""Utility functions and classes for this module found here."""

from openpyxl.utils import column_index_from_string, get_column_letter


def pyindex_for(col_name: str) -> int:
    """Examples: given "A", this returns 0, given "AA" this returns 26."""
    return column_index_from_string(col_name.upper()) - 1


def column_letter_for(pyindex: int):
    """Examples: given 0, this returns "A", given 26 this returns "AA"."""
    return get_column_letter(pyindex + 1)


def split_argstr_respecting_quotes(argstr: str) -> list[str]:
    """Does the same thing as `str.split(" ")`, but combines quoted parts together."""
    if "'" not in argstr and '"' not in argstr:
        return argstr.split(" ")
    ret_me: list[str] = []
    within_quote = False
    cursor = 0
    for index, char in enumerate(argstr):
        match char:
            case " ":
                if not within_quote and cursor != index:
                    ret_me.append(argstr[cursor : index + 1].strip())
                    cursor = index
            case '"':
                if within_quote:
                    # Append the quoted argument without the trailing quote
                    ret_me.append(argstr[cursor:index].strip())
                    within_quote = False
                    cursor = index + 1
                else:
                    within_quote = True
                    cursor = index + 1  # Don't include the quote itself
    argstr_sz = len(argstr)
    if not within_quote and cursor != argstr_sz:
        # Mismatched quote, just return the rest
        ret_me.append(argstr[cursor:argstr_sz].strip())
    elif within_quote and cursor != argstr_sz:
        ret_me += argstr[cursor - 1 : argstr_sz].split(" ")
    return ret_me
