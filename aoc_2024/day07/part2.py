import argparse
import heapq
from math import log10
from pathlib import Path

import pytest

import aoc_utils

INPUT_TXT = Path(__file__).parent / "input.txt"


def parse_line(line: str) -> tuple[int, list[int]]:
    parts = line.split(":")
    return int(parts[0]), [int(num) for num in parts[1].strip().split()]


def cat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def is_solvable(solution: int, numbers: list[int]) -> bool:
    # python uses a min-heap
    queue = [(solution, numbers)]

    while queue:
        cost, (*others, end) = heapq.heappop(queue)

        if len(others) == 0:
            if cost == end:
                return True
            continue

        if cost < 0:
            continue

        # add
        heapq.heappush(queue, (cost - end, others))

        # multiply
        q, r = divmod(cost, end)
        if r == 0:
            heapq.heappush(queue, (q, others))

        # concatenate
        digits_end = int(log10(end)) + 1
        q, r = divmod(cost - end, 10**digits_end)
        if r == 0:
            heapq.heappush(queue, (q, others))

    return False


def compute(puzzle_input: str) -> int:
    lines = [parse_line(line) for line in puzzle_input.splitlines()]

    return sum(line[0] for line in lines if is_solvable(*line))


TEST_INPUT = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 11387),
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
