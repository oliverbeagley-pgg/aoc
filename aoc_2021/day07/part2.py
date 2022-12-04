import argparse
import math
import os
import statistics
from textwrap import dedent

import pytest

import aoc_utils

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def triangle_number(n: int) -> int:
    return n * (n + 1) // 2


def compute(input: str) -> int:
    positions = aoc_utils.parse_number_comma(input)

    mean = statistics.mean(positions)
    rounded = math.floor(mean), math.ceil(mean)
    fuel_costs = min(
        sum(triangle_number(abs(position - mean)) for position in positions)
        for mean in rounded
    )

    return fuel_costs


TEST_INPUT = """
    16,1,2,0,4,2,7,1,2,14
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 168),),
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
