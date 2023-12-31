# pylint: disable=missing-docstring

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import TestCase
from uuid import uuid4

from xl_excel import __version__ as puk_version  # Package-Under-Test
from xl_excel.__main__ import main as run_puk  # Package-Under-Test


class TestPkgStandaloneExecution(TestCase):
    def test_extract_column(self):
        fpath_sample_wkst = Path(__file__).parent / "_data" / "sample_wkbk.xlsx"
        for args_test_case in [
            # UUT shall be able to specify a worksheet with its name (including spaces)
            f'extract --path {fpath_sample_wkst} --sheet "Sheet 1" --col A',
            f"extract -p {fpath_sample_wkst} -s 0 --c A",
            # UUT shall be able to specify a worksheet with an index
            f"extract --path {fpath_sample_wkst} --sheet-index 0 --col A",
            f"extract -p {fpath_sample_wkst} -s 0 --c A",
        ]:
            captured_stdout = StringIO()
            with (
                self.assertRaises(SystemExit) as raised_assert,
                redirect_stdout(captured_stdout),
            ):
                run_puk(args=_split_respecting_quotes(argstr=args_test_case))
            # PUK shall have exited good status
            self.assertEqual(raised_assert.exception.code, 0)

            # PUK shall have output the contents of the column (such that if the output
            # were piped to pbcopy, I'd be able to just paste the contents straight into
            # Python, so I'd immediately have an array
            self.assertEqual(
                "['this', 'column', 'was', 'parsed', None, 'correctly']",
                captured_stdout.getvalue(),
            )

    def test_print(self):
        fpath_sample_wkst = Path(__file__).parent / "_data" / "sample_wkbk.xlsx"
        for args_test_case in [
            f"print --path {fpath_sample_wkst} --sheet-index 0 --col A",
            f"print -p {fpath_sample_wkst} -s 0 --c A",
        ]:
            captured_stdout = StringIO()
            with (
                self.assertRaises(SystemExit) as raised_assert,
                redirect_stdout(captured_stdout),
            ):
                run_puk(args=args_test_case.split(" "))
            # PUK shall have exited good status
            self.assertEqual(raised_assert.exception.code, 0)

            # PUK shall have output the contents of the column (such that if the output
            # were piped to pbcopy, I'd be able to just paste the contents into another
            # Excel worksheet, and it'd look just like what was being extracted)
            self.assertTrue(
                "".join(["this\ncolumn\nwas\nparsed\n\ncorrectly"])
                in captured_stdout.getvalue()
            )

    def test_bad_verbs(self):
        captured_stderr = StringIO()
        for bad_arg_test_case in ["", str(uuid4()), f"{uuid4()} {uuid4()}"]:
            with (
                self.assertRaises(SystemExit) as raised_assert,
                redirect_stderr(captured_stderr),
            ):
                run_puk(args=bad_arg_test_case.split(" "))
            # PUK shall not have exited good status
            self.assertNotEqual(raised_assert.exception.code, 0)

            # PUK shall have complained to stderr mentioning a choice of verbs
            self.assertTrue("invalid choice" in captured_stderr.getvalue())
            self.assertTrue("choose from" in captured_stderr.getvalue())

    def test_version(self):
        captured_stdout = StringIO()
        with (
            self.assertRaises(SystemExit) as raised_assert,
            redirect_stdout(captured_stdout),
        ):
            run_puk(args="--version".split(" "))
        # PUK shall have exited good status
        self.assertEqual(raised_assert.exception.code, 0)

        # PUK shall have mentioned the version in it's stdout
        self.assertTrue(puk_version in captured_stdout.getvalue())

    def test_help(self):
        captured_stdout = StringIO()
        for help_arg in ["-h", "--help"]:
            with (
                self.assertRaises(SystemExit) as raised_assert,
                redirect_stdout(captured_stdout),
            ):
                run_puk(args=help_arg.split(" "))
            # PUK shall have exited good status
            self.assertEqual(raised_assert.exception.code, 0)

            # PUK shall have output some help message to stdout
            self.assertTrue("usage:" in captured_stdout.getvalue())
            self.assertTrue("show this help message" in captured_stdout.getvalue())


def _split_respecting_quotes(argstr: str) -> list[str]:
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


class TestTestMetaTest(TestCase):
    def test_argstring_quote_splitting_behavior(self):
        testme_to_expected = [
            ("", "".split(" ")),
            (" ", " ".split(" ")),
            ("first", "first".split(" ")),
            ("first second", "first second".split(" ")),
            ("first second third", "first second third".split(" ")),
            (" hello ", " hello ".split(" ")),
            (" hello ", " hello ".split(" ")),
            ('"first arg"', ["first arg"]),
            ('"first arg" second_arg', ["first arg", "second_arg"]),
            (
                '"this path has spaces/sup.txt" -c 0',
                ["this path has spaces/sup.txt", "-c", "0"],
            ),
            ('"first arg second_arg', ['"first', "arg", "second_arg"]),
            (
                "'/some/path/to/an_excel_wkbk.xlsx' -c 1 -s \"XSIT Progress\"",
                [
                    "'/some/path/to/an_excel_wkbk.xlsx'",
                    "-c",
                    "1",
                    "-s",
                    "XSIT Progress",
                ],
            ),
        ]
        for test_case in testme_to_expected:
            self.assertListEqual(
                _split_respecting_quotes(argstr=test_case[0]),
                test_case[-1],
            )
