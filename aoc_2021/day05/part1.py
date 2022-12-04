import argparse
import collections
import os
from textwrap import dedent

import pytest

import aoc_utils

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(input: str) -> int:
    lines = input.splitlines()
    intersects = collections.Counter[tuple[int, int]]()
    for line in lines:
        start, end = line.split(" -> ")
        x1, y1 = aoc_utils.parse_number_comma(start)
        x2, y2 = aoc_utils.parse_number_comma(end)

        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                intersects[(x1, y)] += 1
        if y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                intersects[(x, y1)] += 1

    n = 0
    for _, score in intersects.most_common():
        if score > 1:
            n += 1

    return n


TEST_INPUT = """
    0,9 -> 5,9
    8,0 -> 0,8
    9,4 -> 3,4
    2,2 -> 2,1
    7,0 -> 7,4
    6,4 -> 2,0
    0,9 -> 2,9
    3,4 -> 1,4
    0,0 -> 8,8
    5,5 -> 8,2
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 5),),
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
