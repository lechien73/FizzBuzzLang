#!/usr/bin/env python3
import io
import os
import unittest
from unittest.mock import patch

from fbi import FizzBuzzLang, FBSyntaxError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXAMPLES_DIR = "example_scripts"

# The example scripts and the expected output for each
VALID_SCRIPTS = {
    "flow_example.fb": "2\n1\n",
    "hello.fb": "Hello World\n",
    "hello_short.fb": "Hello World\n",
}

INVALID_SCRIPTS = ["invalid_mode.fb", "invalid_submode.fb", "invalid_arg.fb"]

# TODO: Add a test for mul.fb


def path_to_script(filename):
    return os.path.join(BASE_DIR, EXAMPLES_DIR, filename)


class TestOutput(unittest.TestCase):
    def test_valid_scripts(self):
        for script, expected in VALID_SCRIPTS.items():
            with patch('sys.stdout', new=io.StringIO()) as output:
                fbl = FizzBuzzLang()
                fbl.run_file(path_to_script(script))
                self.assertEqual(output.getvalue(), expected,
                                 f"Unexpected output from script {script}")

    def test_invalid_scripts(self):
        for script in INVALID_SCRIPTS:
            with self.assertRaises(FBSyntaxError):
                fbl = FizzBuzzLang()
                fbl.run_file(path_to_script(script))


if __name__ == "__main__":
    unittest.main()
