import argparse
import re
from math import prod
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


pat = re.compile(r"[*+]\s+")


def cephalopod_maths(nums: list[str], ops: str) -> int:
    ceph_nums = (
        int(digits)
        for idx in range(len(nums[0]))
        if (digits := ("".join(num[idx] for num in nums).strip())) != ""
    )

    if ops == "*":
        return prod(ceph_nums)

    return sum(ceph_nums)


def compute(puzzle_input: str) -> int:
    problems = puzzle_input.splitlines()

    numbers = problems[:-1]
    operations = problems[-1]

    spans = (slice(*match.span(0)) for match in pat.finditer(operations))

    return sum(
        cephalopod_maths(
            [numbers[i][span] for i in range(len(numbers))], operations[span.start]
        )
        for span in spans
    )


TEST_INPUT = "123 328  51 64 \n 45 64  387 23 \n  6 98  215 314\n*   +   *   +  \n"


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 3263827),
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
