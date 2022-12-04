import argparse
import collections
import os
from textwrap import dedent

import pytest

import aoc_utils

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(input: str) -> int:
    lanternfish = collections.Counter(aoc_utils.parse_number_comma(input))

    for _ in range(80):
        new_lanternfish = collections.Counter({8: lanternfish[0], 6: lanternfish[0]})
        new_lanternfish.update({k - 1: v for k, v in lanternfish.items() if k > 0})

        lanternfish = new_lanternfish

    return sum(lanternfish.values())


TEST_INPUT = """
    3,4,3,1,2
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 5934),),
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
