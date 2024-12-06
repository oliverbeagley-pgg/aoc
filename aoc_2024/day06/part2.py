import argparse
from collections.abc import Callable
from copy import copy
from pathlib import Path

import pytest

import aoc_utils

INPUT_TXT = Path(__file__).parent / "input.txt"


def has_cycle(
    new_obstacle: complex,
    start: tuple[complex, complex],
    obstacles: set[complex],
    bounds_check: Callable[[complex], bool],
) -> bool:
    visited = {start}

    current_position, direction = start
    obstacles = copy(obstacles)
    obstacles.add(new_obstacle)

    while bounds_check(next_position := current_position + direction):
        if (next_position, direction) in visited:
            return True

        if next_position in obstacles:
            # anticlockwise turn
            direction *= 1j
        else:
            current_position = next_position
            visited.add((current_position, direction))

    return False


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

    direction = -1j
    start = (current_position, direction)
    visited = {start}

    def _bounds_check(point: complex) -> bool:
        return 0 <= point.real <= col_idx and 0 <= point.imag <= row_idx

    while _bounds_check(next_position := current_position + direction):
        if next_position in obstacles:
            # anticlockwise turn
            direction *= 1j
        else:
            current_position = next_position
            visited.add((current_position, direction))

    # visited are the only places that an obstruction can be put to create cycles
    obstacle_candidates = {position for position, _ in visited if position != start[0]}

    return sum(
        has_cycle(obstacle_candidate, start, obstacles, _bounds_check)
        for obstacle_candidate in obstacle_candidates
    )


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
        (TEST_INPUT, 6),
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
