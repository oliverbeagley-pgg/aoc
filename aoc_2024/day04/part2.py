import argparse
from pathlib import Path
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


def compute(puzzle_input: str) -> int:
    grid = {
        Point(row_idx, col_idx): char
        for row_idx, line in enumerate(puzzle_input.splitlines())
        for col_idx, char in enumerate(line)
    }

    mas = ("M", "S")
    sam = tuple(reversed(mas))
    massam = (mas, sam)
    offsets = (-1, 1)

    return sum(
        tuple(grid.get(coord + Point(offset, offset), "") for offset in offsets)
        in massam
        and tuple(grid.get(coord + Point(offset, -offset), "") for offset in offsets)
        in massam
        for coord in grid
        if grid[coord] == "A"
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
        (TEST_INPUT, 9),
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
