#!/usr/bin/env python3
import io
import unittest
from unittest.mock import patch

from fbi import FizzBuzzLang

# The example scripts and the expected output for each
SCRIPTS_TO_TEST = {
    "flow_example.fb": "2\n1\n",
    "hello.fb": "Hello World\n",
    "hello_short.fb": "Hello World\n",
}


class TestOutput(unittest.TestCase):
    def test_scripts(self):
        for script, expected in SCRIPTS_TO_TEST.items():
            with patch('sys.stdout', new=io.StringIO()) as output:
                fbl = FizzBuzzLang()
                fbl.run_file(script)
                self.assertEqual(output.getvalue(), expected,
                                 f"Unexpected output from script {script}")


if __name__ == "__main__":
    unittest.main()
