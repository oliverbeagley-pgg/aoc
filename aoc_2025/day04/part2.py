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


def remove_rolls(grid: set[Point]) -> set[Point]:
    roll_limit = 3

    return {
        roll
        for roll in grid
        if sum(roll + direction.value in grid for direction in Direction) > roll_limit
    }


def compute(puzzle_input: str) -> int:
    grid = {
        Point(row_idx, col_idx)
        for row_idx, line in enumerate(puzzle_input.splitlines())
        for col_idx, char in enumerate(line)
        if char == "@"
    }

    old_grid = grid
    while len(new_grid := remove_rolls(old_grid)) != len(old_grid):
        old_grid = new_grid

    return len(grid) - len(new_grid)


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
        (TEST_INPUT, 43),
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
