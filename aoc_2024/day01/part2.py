import argparse
from collections import Counter
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(input: str) -> int:
    numbers = [[int(x) for x in line.split()] for line in input.splitlines()]

    left, right = zip(*numbers, strict=True)
    right = Counter(right)

    return sum(l * right[l] for l in left)


TEST_INPUT = """\
3   4
4   3
2   5
1   3
3   9
3   3
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 31),
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
