import argparse
import heapq
from itertools import batched
from pathlib import Path
from typing import NamedTuple
from typing import Self

import pytest

import aoc_utils

INPUT_TXT = Path(__file__).parent / "input.txt"


class Blocks(NamedTuple):
    files: int = 0
    empties: int = 0

    @classmethod
    def from_tuple(cls, tup: tuple[int, ...]) -> "Self":
        return cls(*tup)


MAX_BLOCK_SIZE = 10


def heap_candidates(gaps: list[list[int]], file_size: int) -> list[tuple[int, int]]:
    # heap[0] will always be the smallest value
    return [
        (gaps[size][0], size)
        for size in range(file_size, MAX_BLOCK_SIZE)
        if len(gaps[size]) > 0
    ]


def compute(puzzle_input: str) -> int:
    files: list[tuple[int, int]] = [(0, 0)] * (len(puzzle_input.strip()) // 2 + 1)
    gaps: list[list[int]] = [[] for _ in range(MAX_BLOCK_SIZE)]

    start = 0
    for file_id, blocks in enumerate(
        map(
            Blocks.from_tuple,
            batched(map(int, puzzle_input.strip()), n=2),
        )
    ):
        # files index is file_id, value is (start, n_blocks)
        files[file_id] = (start, blocks.files)
        start += blocks.files

        # looping from smallest to largest and only appending, i.e. each gap is sorted
        # in ascending order and so will satisfy the heap invariant
        gaps[blocks.empties].append(start)
        start += blocks.empties

    for file_id, (file_start, file_size) in reversed(tuple(enumerate(files))):
        try:
            new_file_start, gap_size = min(heap_candidates(gaps, file_size))
        except ValueError:
            # no suitable gaps available
            continue

        if new_file_start > file_start:
            continue

        new_file_start = heapq.heappop(gaps[gap_size])

        new_gap_size = gap_size - file_size
        new_gap_start = new_file_start + file_size

        heapq.heappush(gaps[new_gap_size], new_gap_start)

        files[file_id] = (new_file_start, file_size)

    return sum(
        file_idx * pos
        for file_idx, (start, size) in enumerate(files)
        for pos in range(start, start + size)
    )


TEST_INPUT = """\
2333133121414131402
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 2858),
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
