import argparse
from functools import cache
from itertools import batched
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


@cache
def factorise(n: int) -> list[int]:
    factors = [1]
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            factors.append(i)
            factors.append(n // i)

    return factors


def is_bad_code(id_str: str) -> bool:
    if len(id_str) == 1:
        return False

    return any(
        len(set(batched(id_str, factor, strict=True))) == 1
        for factor in factorise(len(id_str))
    )


def compute(puzzle_input: str) -> int:
    ids = [line.split("-") for line in puzzle_input.split(",")]

    bad_ids = [
        id_
        for id_pair in ids
        for id_ in range(int(id_pair[0]), int(id_pair[1]) + 1)
        if is_bad_code(str(id_))
    ]

    return sum(bad_ids)


TEST_INPUT = """\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 4174379265),
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
