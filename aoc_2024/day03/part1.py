import argparse
import re
from math import prod
from pathlib import Path

import pytest

import aoc_utils

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(puzzle_input: str) -> int:
    pattern = re.compile(r"mul\((\d+),(\d+)\)")

    return sum(
        prod(map(int, match.groups())) for match in pattern.finditer(puzzle_input)
    )


TEST_INPUT = """\
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 161),
    ],
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, aoc_utils.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
