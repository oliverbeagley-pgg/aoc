import argparse
import os
from string import ascii_letters
from textwrap import dedent

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


priority = {letter: priority for priority, letter in enumerate(ascii_letters, 1)}


def compute(input: str) -> int:
    bags = input.splitlines()

    n = 0
    for bag in bags:
        n_items = len(bag)
        compartments = (bag[: n_items // 2], bag[n_items // 2 :])
        items = [set(compartment) for compartment in compartments]

        duplicated = items[0] & items[1]

        n += sum(priority[duplicate] for duplicate in duplicated)

    return n


TEST_INPUT = """
    vJrwpWtwJgWrhcsFMMfFFhFp
    jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    PmmdzqPrVvPwwTWBwg
    wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ttgJtRGJQctTZtZT
    CrZsJsPPZsGzwwsLwLmpwMDw
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 157),),
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
