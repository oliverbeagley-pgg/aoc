import argparse
import os
from collections import deque
from itertools import islice
from textwrap import dedent

import pytest

import aoc_utils

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(input: str) -> int:
    numbers = aoc_utils.parse_numbers(input)

    window_size = 3

    it = iter(numbers)
    window = deque(islice(it, window_size), maxlen=window_size)

    window_sums = [sum(window)]

    for x in it:
        window.append(x)
        window_sums.append(sum(window))

    return sum(window_sums[i] > window_sums[i - 1] for i in range(1, len(window_sums)))


TEST_INPUT = """
    199
    200
    208
    210
    200
    207
    240
    269
    260
    263
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
