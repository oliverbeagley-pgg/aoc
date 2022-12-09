from __future__ import annotations

import argparse
import os
from textwrap import dedent

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

MOVES: dict[str, tuple[int, int]] = {
    "L": (-1, 0),
    "R": (1, 0),
    "U": (0, -1),
    "D": (0, 1),
}
OPPOSITES: dict[str, tuple[int, int]] = {
    "L": (1, 0),
    "R": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


def compute(input: str) -> int:
    head = tail = (0, 0)
    visited = {tail}

    for line in input.splitlines():
        direction_s, length_s = line.split()
        length = int(length_s)

        for _ in range(length):
            head = head[0] + MOVES[direction_s][0], head[1] + MOVES[direction_s][1]
            if abs(head[0] - tail[0]) > 1 or abs(head[1] - tail[1]) > 1:
                tail = (
                    head[0] + OPPOSITES[direction_s][0],
                    head[1] + OPPOSITES[direction_s][1],
                )
                visited.add(tail)

    return len(visited)


TEST_INPUT = """
    R 4
    U 4
    L 3
    D 1
    R 4
    D 1
    L 5
    R 2
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 13),),
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
