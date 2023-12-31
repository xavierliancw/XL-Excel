# XL-Excel
---
## About

Xavier's Python package containing tools he uses to speed up his Excel workflows.

## Usage (Assuming Correct Installation)

```Bash
xl-excel print --path '/some_path_to/an_excel_doc.xlsx' --sheet-index 0 --col A |pbcopy
xl-excel print -p '/some_path_to/an_excel_doc.xlsx' -s 0 -c A |pbcopy
```
These both extract column A from the specified Excel workbook's first worksheet into my Mac's clipboard.

```Bash
xl-excel print --path './tests/_data/sample_wkbk.xlsx' --sheet "Sheet 1" --col A |pbcopy
xl-excel print -p './tests/_data/sample_wkbk.xlsx' -s "Sheet 1" -c A |pbcopy
```
Same thing, but the sheet name is specified instead of its tab number.

```Bash
xl-excel extract -p './tests/_data/sample_wkbk.xlsx' -s "Sheet 1" -c A
```
This example outputs the specified column as a Python list. This isn't super useful on the CLI, but it's really useful when imported as a dependency. For example:
```Python
from pathlib import Path

from xl_excel import extract_column_as_list

print(
    extract_column_as_list(
        fpath_wkbk=Path("tests/_data/sample_wkbk.xlsx"),
        sheet=0,
        col_name="A",
    )
)
```
