import argparse
from enum import Enum
from pathlib import Path
from typing import NamedTuple

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: object) -> "Point":
        if not isinstance(other, Point):
            return NotImplemented

        return Point(self.x + other.x, self.y + other.y)


class Direction(Enum):
    NORTH = Point(0, 1)
    NORTH_EAST = Point(1, 1)
    EAST = Point(1, 0)
    SOUTH_EAST = Point(1, -1)
    SOUTH = Point(0, -1)
    SOUTH_WEST = Point(-1, -1)
    WEST = Point(-1, 0)
    NORTH_WEST = Point(-1, 1)


def compute(puzzle_input: str) -> int:
    grid = {
        Point(row_idx, col_idx)
        for row_idx, line in enumerate(puzzle_input.splitlines())
        for col_idx, char in enumerate(line)
        if char == "@"
    }

    roll_limit = 3

    return sum(
        sum(roll + direction.value in grid for direction in Direction) <= roll_limit
        for roll in grid
    )


TEST_INPUT = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 13),
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
