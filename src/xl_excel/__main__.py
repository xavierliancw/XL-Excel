"""Entry-point for executing this package as a standalone CLI application."""

from argparse import ArgumentParser
from dataclasses import fields
from sys import argv

import xl_excel
from xl_excel import __version__ as pkg_version_str
from xl_excel import models_cli


def main(args: list[str]) -> str:
    """Executes this program with Python arguments"""
    verb, args_after_parsing_for_verb = __parse_verb_from_cli_args(args=args)
    __route(verb=verb, args_after_parsing_for_verb=args_after_parsing_for_verb)
    raise SystemExit(0)


if __name__ == "__main__":
    main(args=argv[1:])

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


def __route(verb: models_cli.CLIVerb, args_after_parsing_for_verb: list[str]):
    match verb:
        case models_cli.CLIVerb.EXTRACT | models_cli.CLIVerb.PRINT:
            selection = __try_parsing_column_letter_selection(
                args=args_after_parsing_for_verb
            )
            extracted_list = xl_excel.extract_column_as_list(
                fpath_wkbk=selection.path,
                sheet_index=selection.sheet_index,
                col_name=selection.col,
            )
            print(
                (
                    extracted_list
                    if verb == models_cli.CLIVerb.EXTRACT
                    else "\n".join([cell or "" for cell in extracted_list])
                ),
                end="",
            )


def __try_parsing_column_letter_selection(
    args: list[str],
) -> models_cli.ExcelColumnLetterSelection:
    parsr = ArgumentParser()
    model_fields = fields(models_cli.ExcelColumnLetterSelection)
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
    return models_cli.ExcelColumnLetterSelection(**vars(parsr.parse_args(args=args)))
