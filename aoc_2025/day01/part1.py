import argparse
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(puzzle_input: str) -> int:
    instructions = [(line[:1], int(line[1:])) for line in puzzle_input.splitlines()]

    start = 50
    zeros = 0
    mod = 100

    new_position = start

    for direction, times in instructions:
        old_position = new_position
        clicks = times % mod

        if direction == "L":
            clicks = -clicks

        new_position = (old_position + clicks) % mod

        if new_position == 0:
            zeros += 1

    return zeros


TEST_INPUT = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 3),
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
