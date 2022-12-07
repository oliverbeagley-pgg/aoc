import argparse
import os
from collections.abc import Callable
from textwrap import dedent
from typing import Any

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(input: str) -> int:
    binary = input.splitlines()

    cols = list(zip(*binary))

    oxygen_rating_idx = filter_binary(cols, oxygen_rating_condition)
    co2_scrubber_rating_idx = filter_binary(cols, co2_scrubber_rating_condition)

    oxygen_rating = binary[oxygen_rating_idx]
    scrubbing_rating = binary[co2_scrubber_rating_idx]

    return int(oxygen_rating, 2) * int(scrubbing_rating, 2)


def filter_binary(
    columns: list[tuple[str, ...]],
    condition: Callable[[int, list[Any]], bool],
) -> int:
    keep_bits: list[str] = []
    remaining = list(range(len(columns[0])))

    while len(remaining) != 1:

        col = columns[len(keep_bits)]
        count = sum(int(col[idx]) for idx in remaining)

        keep_bits.append("1" if condition(count, remaining) else "0")
        remaining = [idx for idx in remaining if col[idx] == keep_bits[-1]]

    return remaining[0]


def oxygen_rating_condition(count: int, remaining: list[Any]) -> bool:
    return count >= len(remaining) / 2


def co2_scrubber_rating_condition(count: int, remaining: list[Any]) -> bool:
    return count < len(remaining) / 2


TEST_INPUT = """
    00100
    11110
    10110
    10111
    10101
    01111
    00111
    11100
    10000
    11001
    00010
    01010
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 230),),
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
