# pylint: disable=missing-docstring

from unittest import TestCase

from xl_excel import util as _mut  # Module-Under-Test


class TestUtil(TestCase):
    def test_converting_colstr_to_index(self):
        # UUT shall not be case sensitive and also start at index 0
        test_case_to_expected_map = {
            "aB": 27,
            "aa": 26,
            "a": 0,
            "A": 0,
            "z": 25,
            "Z": 25,
            "Ab": 27,
        }
        for test_case, expected in test_case_to_expected_map.items():
            uut = _mut.pyindex_for(col_name=test_case)
            self.assertEqual(uut, expected)

    def test_converting_index_to_excel_colname(self):
        # UUT shall return the correct column name given a zero-based index
        test_case_to_expected_map = {
            27: "AB",
            26: "AA",
            0: "A",
            25: "Z",
        }
        for test_case, expected in test_case_to_expected_map.items():
            uut = _mut.column_letter_for(pyindex=test_case)
            self.assertEqual(uut, expected)

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
                _mut.split_argstr_respecting_quotes(argstr=test_case[0]),
                test_case[-1],
            )
