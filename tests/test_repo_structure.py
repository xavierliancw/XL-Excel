# pylint: disable=missing-docstring
from pathlib import Path
from subprocess import PIPE, Popen
from sys import executable
from tomllib import load as toml_load
from typing import List, Tuple
from unittest import TestCase

from isort import check_file as isort_check_file

from xl_excel import __version__ as _module_under_test_version

DPATH_PROJECT = Path()
FPATH_PYPROJECTTOML = DPATH_PROJECT.joinpath("pyproject.toml")
with open(FPATH_PYPROJECTTOML, "rb") as fin_toml:
    TOML_PYPROJECT = toml_load(fin_toml)
MODULE_NAME: str = TOML_PYPROJECT["project"]["name"].replace("-", "_")
DPATH_MODULE = Path(__file__).parent.parent.joinpath("src").joinpath(MODULE_NAME)


class TestRepoIntegrity(TestCase):
    def test_no_prints_in_business_logic(self):
        bad_syntax = b"print("
        for fpath_pyfile_under_test in DPATH_MODULE.rglob("**/*.py"):
            if fpath_pyfile_under_test == DPATH_MODULE / "__main__.py":
                continue
            with open(fpath_pyfile_under_test, "rb") as fin:
                for line_index, line in enumerate(fin):
                    if bad_syntax in line:
                        self.fail(f"Line {line_index + 1} has a print statement!")

    def test_matching_versions(self):
        self.assertEqual(
            TOML_PYPROJECT["project"]["version"], _module_under_test_version
        )

    def test_isort_compliance(self):
        for fpath_pyfile in DPATH_PROJECT.rglob("**/*.py"):
            self.assertTrue(
                isort_check_file(
                    filename=fpath_pyfile, show_diff=True, profile="black"
                ),
                f"{fpath_pyfile} is not compliant!",
            )

    def test_black_check_on_tests(self):
        black_result = self._run_pymodule_through_cli(
            module_name="black",
            module_cli_args=[str(DPATH_PROJECT.joinpath("tests")), "--check", "--diff"],
        )
        self.assertEqual(black_result[2], 0, msg=black_result[0])

    def test_black_check_on_module(self):
        black_result = self._run_pymodule_through_cli(
            module_name="black",
            module_cli_args=[str(DPATH_MODULE), "--check", "--diff"],
        )
        self.assertTrue(black_result[2] == 0, msg=black_result[0])

    def test_pylint_module_passes(self):
        pylint_result = self._run_pymodule_through_cli(
            module_name="pylint", module_cli_args=[str(DPATH_MODULE)]
        )
        self.assertTrue(pylint_result[2] == 0, msg=pylint_result[0])

    def test_pylint_tests_passes(self):
        pylint_result = self._run_pymodule_through_cli(
            module_name="pylint", module_cli_args=[str(DPATH_PROJECT.joinpath("tests"))]
        )
        self.assertTrue(pylint_result[2] == 0, msg=pylint_result[0])

    def test_testdata_folder(self):
        # Sample data that other unit tests use shall exist in a certain location within
        # this repository
        uut = DPATH_PROJECT.joinpath("tests").joinpath("_data")
        self.assertTrue(uut.exists())
        self.assertTrue(uut.is_dir())

    def test_py_typed_exists(self):
        self.assertTrue(DPATH_MODULE.joinpath("py.typed").exists())

    def test_stuff_needed_for_proper_wheel_packaging(self):
        """These tests help ensure package building behaves as expected."""
        # The src folder shall exist
        dpath_src = Path(__file__).parent.parent.joinpath("src")
        self.assertTrue(dpath_src.is_dir())
        self.assertTrue(dpath_src.exists())

        # The src folder shall contain a directory with the package name
        src_contents = set(dpath_src.iterdir())
        self.assertTrue(MODULE_NAME in {x.name for x in src_contents if x.is_dir()})

        # The pyproject.toml shall exist
        self.assertTrue(FPATH_PYPROJECTTOML.exists())

        # The pyproject.toml shall package the typing information
        self.assertListEqual(
            TOML_PYPROJECT["tool"]["setuptools"]["packages"]["find"]["where"], ["src"]
        )
        self.assertListEqual(
            TOML_PYPROJECT["tool"]["setuptools"]["package-data"][MODULE_NAME],
            ["py.typed"],
        )
        self.assertTrue("setuptools" in TOML_PYPROJECT["build-system"]["requires"])

    def test_dpath_project_refers_to_the_right_path(self):
        # If this test doesn't pass, most of the other tests in this repo won't
        dpath_project = [x.name for x in DPATH_PROJECT.iterdir()]
        self.assertTrue("src" in dpath_project)
        self.assertTrue("README.md" in dpath_project)
        self.assertTrue("tests" in dpath_project)
        self.assertTrue(".gitignore" in dpath_project)
        self.assertTrue("pyproject.toml" in dpath_project)

    @staticmethod
    def _run_pymodule_through_cli(
        module_name: str, module_cli_args: List[str]
    ) -> Tuple[str, str, int]:
        with Popen(
            [executable, "-m", module_name] + module_cli_args, stdout=PIPE, stderr=PIPE
        ) as proc:
            out, err = proc.communicate()
            return (out.decode(), err.decode(), proc.returncode)
