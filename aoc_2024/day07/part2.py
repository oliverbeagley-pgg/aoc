import argparse
import heapq
from collections.abc import Callable
from operator import add
from operator import mul
from pathlib import Path
from typing import cast

import pytest

import aoc_utils

INPUT_TXT = Path(__file__).parent / "input.txt"


def parse_line(line: str) -> tuple[int, list[int]]:
    parts = line.split(":")
    return int(parts[0]), [int(num) for num in parts[1].strip().split()]


def cat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def is_solvable(solution: int, numbers: list[int]) -> bool:
    ops = cast(tuple[Callable[[int, int], int]], (add, mul, cat))
    # python uses a min-heap
    queue = [(-solution, numbers)]

    while queue:
        _, remaining_numbers = heapq.heappop(queue)

        first, second, *others = remaining_numbers

        for op in ops:
            new_answer = op(first, second)
            new_numbers = [new_answer, *others]

            if (new_cost := new_answer - solution) > 0:
                continue

            if len(new_numbers) == 1:
                if new_answer == solution:
                    return True

                continue

            heapq.heappush(queue, (new_cost, new_numbers))

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
