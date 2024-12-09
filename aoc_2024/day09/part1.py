import argparse
from collections import deque
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


def partial_checksum(position: int, file_id: int, n_blocks: int) -> int:
    return sum(pos * file_id for pos in range(position, position + n_blocks))


def compute(puzzle_input: str) -> int:
    # enumerate will give the (file_id, (file blocks, empty blocks))
    disk = deque(
        enumerate(map(Blocks.from_tuple, batched(map(int, puzzle_input.strip()), n=2)))
    )

    checksum = 0
    idx = 0
    while disk:
        file_id_l, blocks_l = disk.popleft()

        checksum += partial_checksum(idx, file_id_l, blocks_l.files)
        idx += blocks_l.files

        while blocks_l.empties > 0:
            file_id_r, blocks_r = disk.pop()

            if blocks_l.empties >= blocks_r.files:
                checksum += partial_checksum(idx, file_id_r, blocks_r.files)
                idx += blocks_r.files

                blocks_l = Blocks(empties=blocks_l.empties - blocks_r.files)
            else:
                checksum += partial_checksum(idx, file_id_r, blocks_l.empties)
                idx += blocks_l.empties

                disk.append(
                    (
                        file_id_r,
                        Blocks(blocks_r.files - blocks_l.empties),
                    )
                )
                break

    return checksum


TEST_INPUT = """\
2333133121414131402
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 1928),
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
