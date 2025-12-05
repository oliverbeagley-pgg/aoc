import argparse
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(puzzle_input: str) -> int:
    ranges_str, _ = puzzle_input.split("\n\n")
    ranges = iter(
        sorted(
            [int(r) for r in range_.split("-")] for range_ in ranges_str.splitlines()
        )
    )

    merged = [next(ranges)]
    for start, end in ranges:
        _, last_end = merged[-1]
        if start > last_end:
            merged.append([start, end])
        else:
            merged[-1][1] = max(last_end, end)

    return sum(end - start + 1 for start, end in merged)


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
        (TEST_INPUT, 14),
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
