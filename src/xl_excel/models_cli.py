"""Module for controlling flow through this package when executing as a CLI 
application."""

from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path


class CLIVerb(StrEnum):
    """Supported verbs for control flow."""

    EXTRACT = auto()
    PRINT = auto()


@dataclass(slots=True, frozen=True)
class ExcelSheetSelection:
    """Models an Excel worksheet selection."""

    path: Path  # Path to the workbook
    sheet_index: int  # Worksheet selection by index where 0 is the leftmost tab


@dataclass(slots=True, frozen=True)
class ExcelColumnLetterSelection(ExcelSheetSelection):
    """Models an Excel column selection."""

    col: str  # Example "A" or "ABC"


@dataclass(slots=True, frozen=True)
class ExcelCellSelection:
    """Models a selection of cells within an Excel workbook."""

    fpath: Path  # Path to the workbook
    sheet: str | None  # Worksheet selection by its name
    sheet_index: int | None  # Worksheet selection where the left-most tab is sheet 0
    column: str | None  # Column A, B, ..., AA, AB etc.
    row: int | None  # Excel rows start at 1, not 0
    cells: set[str] | None  # Set of cells to select (e.g. {"A2", "BB8"})
