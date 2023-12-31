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
