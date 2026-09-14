"""
Caleb Morris
Assignment03
this runs test_inputs.txt through my parser. I did have the help of Claude.ai when completing this assingment.

Reads test_inputs.txt (one command per line, '#' lines are comments/blank
lines ignored), runs each command through the tokenizer + parser, and
prints the resulting AST or the error raised.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shell_parser import parse, ParseError
from tokenizer import LexError

TEST_FILE = os.path.join(os.path.dirname(__file__), "test_inputs.txt")


def main():
    with open(TEST_FILE, "r") as f:
        lines = f.readlines()

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        try:
            ast = parse(line)
            print(f"{line!r:30} -> OK: {ast}")
        except (ParseError, LexError) as e:
            print(f"{line!r:30} -> ERROR ({type(e).__name__}): {e}")


if __name__ == "__main__":
    main()