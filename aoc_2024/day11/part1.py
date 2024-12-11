import argparse
from collections.abc import Generator
from functools import reduce
from math import log10
from operator import iadd
from pathlib import Path

import pytest

import aoc_utils

INPUT_TXT = Path(__file__).parent / "input.txt"


def blink(stone: int) -> Generator[int]:
    if stone == 0:
        yield 1
    elif (n_digits := (int(log10(stone)) + 1)) % 2 == 0:
        yield from map(int, divmod(stone, 10 ** (n_digits / 2)))
    else:
        yield stone * 2024


def compute(puzzle_input: str) -> int:
    stones = list(map(int, puzzle_input.strip().split()))
    for _ in range(25):
        stones = list(reduce(iadd, map(blink, stones), []))

    return len(stones)


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
