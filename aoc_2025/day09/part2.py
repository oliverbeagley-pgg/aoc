import argparse
import operator
from functools import reduce
from itertools import combinations
from itertools import pairwise
from pathlib import Path
from typing import NamedTuple
from typing import Self

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


class Point(NamedTuple):
    x: int
    y: int

    def area(self, other: Self) -> int:
        return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)

    @classmethod
    def from_string(cls, s: str) -> Self:
        x, y = map(int, s.split(","))
        return cls(x, y)


def line(tile_1: Point, tile_2: Point) -> set[Point]:
    (x1, x2), (y1, y2) = (sorted(pair) for pair in zip(tile_1, tile_2, strict=True))
    return {Point(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)}


def perimeter(tiles: list[Point]) -> set[Point]:
    _tiles = tiles.copy()
    _tiles.append(tiles[0])
    return reduce(operator.or_, (line(t1, t2) for t1, t2 in pairwise(_tiles)))


def within_perimeter(tile_1: Point, tile_2: Point, perimeter: set[Point]) -> bool:
    (x1, x2), (y1, y2) = (sorted(pair) for pair in zip(tile_1, tile_2, strict=True))

    return not any(x1 < p.x < x2 and y1 < p.y < y2 for p in perimeter)


def compute(puzzle_input: str) -> int:
    tiles = [Point.from_string(line) for line in puzzle_input.splitlines()]

    perimeter_tiles = perimeter(tiles)
    areas = sorted(
        (
            (tile_1.area(tile_2), (tile_1, tile_2))
            for tile_1, tile_2 in combinations(tiles, 2)
        ),
        reverse=True,
    )

    for area, (tile_1, tile_2) in areas:
        if within_perimeter(tile_1, tile_2, perimeter_tiles):
            return area

    msg = "No valid tile pairs found"
    raise ValueError(msg)


TEST_INPUT = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 24),
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
