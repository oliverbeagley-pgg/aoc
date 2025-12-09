import argparse
from itertools import combinations
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


def compute(puzzle_input: str) -> int:
    tiles = (Point.from_string(line) for line in puzzle_input.splitlines())

    return max(tile_1.area(tile_2) for tile_1, tile_2 in combinations(tiles, 2))


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
        (TEST_INPUT, 50),
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
