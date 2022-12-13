from __future__ import annotations

import argparse
import heapq
import os
from collections.abc import Iterator
from textwrap import dedent

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def surrounding(coord: tuple[int, int]) -> Iterator[tuple[int, int]]:
    yield coord[0] + 1, coord[1]
    yield coord[0] - 1, coord[1]
    yield coord[0], coord[1] + 1
    yield coord[0], coord[1] - 1


def compute(input: str) -> int:

    coords = {}

    for y, line in enumerate(input.splitlines()):
        for x, s in enumerate(line):
            coords[(y, x)] = ord(s)

            if s == "S":
                coords[(y, x)] = ord("a")
            elif s == "E":
                end = (y, x)
                coords[(y, x)] = ord("z")

    assert end

    visited: set[tuple[int, int]] = set()
    queue: list[tuple[int, tuple[int, int]]] = [(0, end)]

    while queue:
        cost, coord = heapq.heappop(queue)

        if coords[coord] == ord("a"):
            return cost
        elif coord in visited:
            continue
        else:
            visited.add(coord)

        for candidate in surrounding(coord):
            if candidate in coords:
                if coords[candidate] - coords[coord] >= -1:
                    heapq.heappush(queue, (cost + 1, candidate))

    raise AssertionError("Unreachable")


TEST_INPUT = """
    Sabqponm
    abcryxxl
    accszExk
    acctuvwj
    abdefghi
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 29),),
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
