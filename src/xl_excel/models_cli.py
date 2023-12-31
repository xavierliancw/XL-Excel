"""Module for controlling flow through this package when executing as a CLI 
application. The names and layout of these classes are convenient to use with 
`argparse.ArgumentParser` to make my life easier."""

from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path


class CLIVerb(StrEnum):
    """Supported verbs for control flow."""

    EXTRACT = auto()
    PRINT = auto()


@dataclass(slots=True, frozen=True)
class ExcelWkbkSelection:
    """Models an Excel workbook selection."""

    path: Path  # Path to the workbook


@dataclass(slots=True, frozen=True)
class ExcelSheetIndexSelection:
    """Models an Excel worksheet selection."""

    sheet_index: int  # Worksheet selection by index where 0 is the leftmost tab


@dataclass(slots=True, frozen=True)
class ExcelSheetSelection:
    """Models an Excel worksheet selection."""

    sheet: str  # Name of worksheet to select


@dataclass(slots=True, frozen=True)
class ExcelColumnLetterSelection:
    """Models an Excel column selection."""

    col: str  # Example "A" or "ABC"
