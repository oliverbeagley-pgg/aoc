import argparse
from pathlib import Path

import pytest

import aoc_utils

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(puzzle_input: str) -> int:
    obstacles: set[complex] = set()

    for row_idx, line in enumerate(puzzle_input.splitlines()):
        for col_idx, char in enumerate(line):
            point = col_idx + row_idx * 1j
            if char == "#":
                obstacles.add(point)
            if char == "^":
                current_position = point

    assert current_position

    visited = {current_position}
    direction = -1j

    def _bounds_check(point: complex) -> bool:
        return 0 <= point.real <= col_idx and 0 <= point.imag <= row_idx

    while _bounds_check(next_position := current_position + direction):
        if next_position in obstacles:
            # anticlockwise turn
            direction *= 1j
        else:
            current_position = next_position
            visited.add(current_position)

    return len(visited)


TEST_INPUT = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 41),
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
