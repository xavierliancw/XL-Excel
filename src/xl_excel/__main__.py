"""Entry-point for executing this package as a standalone CLI application."""

from argparse import ArgumentParser
from dataclasses import fields
from sys import argv
from typing import Any as __Any

import xl_excel
from xl_excel import __version__ as pkg_version_str
from xl_excel import models_cli


def main(args: list[str]) -> str:
    """Executes this program with Python arguments"""
    verb, args_after_parsing_for_verb = __parse_verb_from_cli_args(args=args)
    __route(verb=verb, leftover_args=args_after_parsing_for_verb)
    raise SystemExit(0)


# Privates =============================================================================


def __parse_verb_from_cli_args(args: list[str]) -> tuple[models_cli.CLIVerb, list[str]]:
    """Parses CLI args into the object this module needs to run."""
    parser = ArgumentParser()

    parser.add_argument("--version", action="version", version=pkg_version_str)
    added_arg = parser.add_argument(
        dest="verb",
        type=str,  # Don't use the enum here or else the stderr output will look ugly
        help="desired action",
        action="store",
        choices=[e.value for e in models_cli.CLIVerb],
    )
    ns_stage1, args_after_stage1_parsing = parser.parse_known_args(args=args)
    return (
        models_cli.CLIVerb(getattr(ns_stage1, added_arg.dest)),
        args_after_stage1_parsing,
    )


def __route(verb: models_cli.CLIVerb, leftover_args: list[str]):
    match verb:
        case models_cli.CLIVerb.EXTRACT | models_cli.CLIVerb.PRINT:
            wkbk_selection: models_cli.ExcelWkbkSelection
            wkst_selection: (
                models_cli.ExcelSheetSelection | models_cli.ExcelSheetIndexSelection
            )
            col_selection: models_cli.ExcelColumnLetterSelection
            wkbk_selection, leftover_args = (
                __try_parsing_args_with_dynamic_dataclass_instantiation(
                    args=leftover_args,
                    dc_to_init=models_cli.ExcelWkbkSelection,
                )
            )
            for sheet_selection_technique in [
                models_cli.ExcelSheetIndexSelection,
                # This must be last because it's the most forgiving
                models_cli.ExcelSheetSelection,
            ]:
                try:
                    wkst_selection, leftover_args = (
                        __try_parsing_args_with_dynamic_dataclass_instantiation(
                            args=leftover_args,
                            dc_to_init=sheet_selection_technique,
                        )
                    )
                    break
                except SystemExit:
                    pass

            col_selection, _ = __try_parsing_args_with_dynamic_dataclass_instantiation(
                args=leftover_args, dc_to_init=models_cli.ExcelColumnLetterSelection
            )

            extracted_list = xl_excel.extract_column_as_list(
                fpath_wkbk=wkbk_selection.path,
                sheet=getattr(wkst_selection, fields(wkst_selection)[-1].name),
                col_name=col_selection.col,
            )
            print(
                (
                    extracted_list
                    if verb == models_cli.CLIVerb.EXTRACT
                    else "\n".join([cell or "" for cell in extracted_list])
                ),
                end="",
            )


def __try_parsing_args_with_dynamic_dataclass_instantiation(
    args: list[str], dc_to_init: type
) -> tuple[__Any, list[str]]:
    parsr = ArgumentParser()
    model_fields = fields(dc_to_init)
    first_letter_of_each_field = [f.name[0] for f in model_fields]
    add_flag = len(first_letter_of_each_field) == len(set(first_letter_of_each_field))

    for index, field in enumerate(model_fields):
        non_kwargs = [f"-{first_letter_of_each_field[index]}"] if add_flag else []
        non_kwargs.append(f'--{field.name.replace("_" , "-")}')
        parsr.add_argument(
            *non_kwargs,
            required=True,
            dest=field.name,
            type=field.type,
            action="store",
        )
    ns, leftover_args = parsr.parse_known_args(args=args)
    return dc_to_init(**vars(ns)), leftover_args


if __name__ == "__main__":
    # This MUST come last because Python uses block-scoping, not hoisting
    main(args=argv[1:])
