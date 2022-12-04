import argparse
import os
import statistics
from textwrap import dedent

import pytest

import aoc_utils

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(input: str) -> int:
    positions = aoc_utils.parse_number_comma(input)

    median = round(statistics.median(positions))

    fuel_costs = sum(abs(position - median) for position in positions)

    return fuel_costs


TEST_INPUT = """
    16,1,2,0,4,2,7,1,2,14
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 37),),
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
