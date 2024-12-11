import argparse
from functools import cache
from math import log10
from pathlib import Path

import pytest

import aoc_utils

INPUT_TXT = Path(__file__).parent / "input.txt"


@cache
def blink(stone: int, remaining_blinks: int) -> int:
    if remaining_blinks == 0:
        return 1

    if stone == 0:
        return blink(1, remaining_blinks - 1)

    if (n_digits := (int(log10(stone)) + 1)) % 2 == 0:
        q, r = divmod(stone, 10 ** (n_digits / 2))
        return blink(q, remaining_blinks - 1) + blink(r, remaining_blinks - 1)

    return blink(stone * 2024, remaining_blinks - 1)


def compute(puzzle_input: str) -> int:
    stones = list(map(int, puzzle_input.strip().split()))

    return sum(blink(stone, 75) for stone in stones)


TEST_INPUT = """\
125 17
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 55312),
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
