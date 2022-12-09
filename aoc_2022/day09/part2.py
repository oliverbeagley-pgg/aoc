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


def move_previous(head: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:
    head_x, head_y = head
    tail_x, tail_y = tail

    if abs(tail_y - head_y) > 1 and abs(tail_x - head_x) > 1:
        tail = (
            (head_x + tail_x) // 2,
            (head_y + tail_y) // 2,
        )
    elif abs(tail_y - head_y) > 1:
        tail = (
            head_x,
            (tail_y + head_y) // 2,
        )
    elif abs(tail_x - head_x) > 1:
        tail = (
            (tail_x + head_x) // 2,
            head_y,
        )

    return tail


def compute(input: str) -> int:
    positions = [(0, 0)] * 10
    visited = {positions[-1]}

    for line in input.splitlines():
        direction_s, length_s = line.split()
        length = int(length_s)

        for _ in range(length):
            positions[0] = (
                positions[0][0] + MOVES[direction_s][0],
                positions[0][1] + MOVES[direction_s][1],
            )

            current_knot = positions[0]
            for idx in range(1, len(positions)):
                positions[idx] = move_previous(current_knot, positions[idx])
                current_knot = positions[idx]

            visited.add(positions[-1])

    return len(visited)


TEST_INPUT = """
    R 5
    U 8
    L 8
    D 3
    R 17
    D 10
    L 25
    U 20
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 36),),
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
