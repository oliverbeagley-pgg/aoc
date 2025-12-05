import argparse
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(puzzle_input: str) -> int:
    ranges_str, ingredients_str = puzzle_input.split("\n\n")
    ranges = [
        tuple(int(r) for r in range_.split("-")) for range_ in ranges_str.splitlines()
    ]
    ingredients = [int(ingredient) for ingredient in ingredients_str.splitlines()]

    return sum(
        any(start <= ingredient <= end for start, end in ranges)
        for ingredient in ingredients
    )


TEST_INPUT = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 3),
    ],
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
