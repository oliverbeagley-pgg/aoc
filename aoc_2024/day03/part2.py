import argparse
import re
from pathlib import Path

import pytest

import aoc_utils

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(puzzle_input: str) -> int:
    pattern = re.compile(r"(do|don't)\(\)|mul\((\d+),(\d+)\)")

    matches: list[tuple[str, str, str]] = pattern.findall(puzzle_input)

    matches_stack = list(reversed(matches))

    include = True
    operations = []
    while matches_stack:
        match = matches_stack.pop()
        match match[0]:
            case "do":
                include = True
            case "don't":
                include = False
            case _:
                if include:
                    operations.append(match[1:3])

    return sum(int(a) * int(b) for a, b in operations)


TEST_INPUT = """\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 48),
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
