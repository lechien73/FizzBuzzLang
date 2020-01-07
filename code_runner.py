#!/usr/bin/env python3
import sys

from fbi import FizzBuzzLang


def run(script, debug=False):
    fbl = FizzBuzzLang(debug=debug)
    fbl.run_file(script)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} SCRIPT [--debug]')
        exit(1)
    script = sys.argv[1]
    debug = "--debug" in sys.argv
    run(script, debug)
