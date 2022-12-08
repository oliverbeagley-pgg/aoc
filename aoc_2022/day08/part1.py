from __future__ import annotations

import argparse
import os
from collections.abc import Sequence
from textwrap import dedent

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def get_visible_trees(stride: Sequence[int]) -> set[int]:
    visible_trees = {
        0,
        len(stride) - 1,
    }

    current_max = stride[0]
    for idx in range(1, len(stride)):
        if stride[idx] > current_max:
            visible_trees.add(idx)
            current_max = stride[idx]

    current_max = stride[-1]
    for idx in range(len(stride) - 2, -1, -1):
        if stride[idx] > current_max:
            visible_trees.add(idx)
            current_max = stride[idx]

    return visible_trees


def compute(input: str) -> int:
    trees = [[int(height) for height in row_s] for row_s in input.splitlines()]

    visible_trees: set[tuple[int, int]] = set()

    for y_idx, row in enumerate(trees):
        visible_trees.update({(x_idx, y_idx) for x_idx in get_visible_trees(row)})

    for x_idx, col in enumerate(zip(*trees)):
        visible_trees.update({(x_idx, y_idx) for y_idx in get_visible_trees(col)})

    return len(visible_trees)


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
    ((TEST_INPUT, 21),),
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
