import os
import sys
from typing import List
from teamcity import is_running_under_teamcity
from pathlib import Path
import pytest

try:
    from pip import main as pipmain
except:
    from pip._internal import main as pipmain

only_teamcity = pytest.mark.skipif(
    not (is_running_under_teamcity() or "FORCE_TEAMCITY" in os.environ),
    reason="Console test only installed on TC.",
)


class TestUtils:

    _name_external = "external_test_data"
    _name_local = "test_files"
    _name_output = "test_output"

    @staticmethod
    def install_package(package: str):
        """Installs a package that is normally only used
        by a test configuration.

        Arguments:
            package {str} -- Name of the PIP package.
        """
        pipmain(["install", package])

    @staticmethod
    def get_test_files_from_local_test_dir(
        dir_name: str, glob_filter: str
    ) -> List[Path]:
        """Returns all the files that need to be used as test input parameters from a given directory.

        Args:
            dir_name (str): Name of the local test data directory.
            glob_filter (str): Filter that will be applied with the glob function.

        Returns:
            List[Path]: List of files matching the above criteria.
        """
        return [
            input_file
            for input_file in Path(TestUtils.get_local_test_data_dir(dir_name)).glob(
                glob_filter
            )
            if input_file.is_file()
        ]

    @staticmethod
    def get_output_test_data_dir(dir_name: str):
        """
        Returns the full path of a directory containing generated
        data from the tests. If it does not exist it creates it.
        """
        directory = TestUtils.get_test_data_dir(dir_name, TestUtils._name_output)
        if not directory.is_file():
            Path.mkdir(directory)
        return directory

    @staticmethod
    def get_local_test_file(filepath: str) -> Path:
        return Path(__file__).parent / TestUtils._name_local / filepath

    @staticmethod
    def get_local_test_data_dir(dir_name: str) -> Path:
        """
        Returns the desired directory relative to the test data.
        Avoiding extra code on the tests.
        """
        return TestUtils.get_test_data_dir(dir_name, TestUtils._name_local)

    @staticmethod
    def get_external_test_data_dir(dir_name: str) -> Path:
        """
        Returns the desired directory relative to the test external data.
        Avoiding extra code on the tests.
        """
        directory = TestUtils.get_test_data_dir(dir_name, TestUtils._name_external)
        return directory

    @staticmethod
    def get_test_data_dir(dir_name: str, test_data_name: str) -> Path:
        """
        Returns the desired directory relative to the test external data.
        Avoiding extra code on the tests.
        """
        test_dir = Path(__file__).parent
        try:
            test_dir = test_dir / test_data_name / dir_name
        except:
            print("An error occurred trying to find {}".format(dir_name))
        return test_dir

    @staticmethod
    def get_test_dir(dir_name: str) -> Path:
        """Returns the desired directory inside the Tests folder

        Arguments:
            dir_name {str} -- Target directory.

        Returns:
            {str} -- Path to the target directory.
        """
        test_dir = Path(__file__).parent
        dir_path = test_dir / dir_name
        return dir_path
