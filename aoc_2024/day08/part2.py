import argparse
from itertools import permutations
from pathlib import Path

import pytest

import aoc_utils

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(puzzle_input: str) -> int:
    grid = {
        col_idx + row_idx * 1j: char
        for row_idx, line in enumerate(puzzle_input.splitlines())
        for col_idx, char in enumerate(line)
    }

    freqs = {*grid.values()}
    freqs.discard(".")

    max_t = int(max(k.real for k in grid)) + 1

    antinodes = {
        a + (b - a) * t
        for freq in freqs
        for a, b in permutations((p for p in grid if grid[p] == freq), r=2)
        for t in range(max_t)
    }

    return len(antinodes & set(grid))


TEST_INPUT = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 34),
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
