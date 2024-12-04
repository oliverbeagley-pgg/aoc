import argparse
from enum import Enum
from pathlib import Path
from typing import Literal
from typing import NamedTuple

import pytest

import aoc_utils

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


next_character = {
    "X": "M",
    "M": "A",
    "A": "S",
}


def character_search(
    character: str,
    from_position: Point,
    direction: Direction,
    grid: dict[Point, str],
) -> Literal[0, 1]:
    # Out of bounds of grid
    try:
        grid_char = grid[from_position]
    except KeyError:
        return 0

    if grid_char == character:
        if grid_char == "S":
            return 1

        return character_search(
            next_character[character],
            from_position + direction.value,
            direction,
            grid,
        )

    return 0


def compute(puzzle_input: str) -> int:
    grid = {
        Point(row_idx, col_idx): char
        for row_idx, line in enumerate(puzzle_input.splitlines())
        for col_idx, char in enumerate(line)
    }
    return sum(
        character_search("X", coord, direction, grid)
        for coord in grid
        for direction in Direction
    )


TEST_INPUT = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 18),
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
