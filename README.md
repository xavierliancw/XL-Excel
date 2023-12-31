# XL-Excel
---
## About

Xavier's Python package containing tools he uses to speed up his Excel workflows.

## Usage (Assuming Correct Installation)

```Bash
xl-excel print --path '/some_path_to/an_excel_doc.xlsx' --sheet-index \"Worksheet 1\" --col A |pbcopy
xl-excel print -p '/some_path_to/an_excel_doc.xlsx' -s \"Worksheet 1\" -c A |pbcopy
```
These both extract column A from the specified Excel workbook's first worksheet into my Mac's clipboard.
