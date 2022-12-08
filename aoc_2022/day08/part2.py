from __future__ import annotations

import argparse
import math
import os
from textwrap import dedent

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def get_viewing_distances(
    x: int,
    y: int,
    grid: list[list[int]],
) -> tuple[int, int, int, int]:
    up = down = left = right = 0

    height = grid[y][x]

    for best_y in range(y - 1, -1, -1):
        up += 1
        if grid[best_y][x] >= height:
            break

    for best_y in range(y + 1, len(grid)):
        down += 1
        if grid[best_y][x] >= height:
            break

    for best_x in range(x - 1, -1, -1):
        left += 1
        if grid[y][best_x] >= height:
            break

    for best_x in range(x + 1, len(grid[0])):
        right += 1
        if grid[y][best_x] >= height:
            break

    return up, down, left, right


def compute(input: str) -> int:
    trees = [[int(height) for height in row_s] for row_s in input.splitlines()]

    distances = [
        math.prod(get_viewing_distances(x, y, trees))
        for x in range(len(trees[0]))
        for y in range(len(trees))
    ]

    return max(distances)


TEST_INPUT = """
    30373
    25512
    65332
    33549
    35390
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 8),),
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
