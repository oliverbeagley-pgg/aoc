import argparse
from math import prod
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(puzzle_input: str) -> int:
    problems = [line.split() for line in puzzle_input.splitlines()]

    return sum(
        prod(nums) if op == "*" else sum(nums)
        for nums, op in zip(
            zip(*((int(x) for x in row) for row in problems[:-1]), strict=True),
            problems[-1],
            strict=True,
        )
    )


TEST_INPUT = """\
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 4277556),
    ],
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
