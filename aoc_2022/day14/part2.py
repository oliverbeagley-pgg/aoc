from __future__ import annotations

import argparse
import itertools
import os
from collections.abc import Iterator
from textwrap import dedent

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def place_rocks(
    coord_sequence: Iterator[list[tuple[int, int]]]
) -> set[tuple[int, int]]:
    coords: set[tuple[int, int]] = set()

    for sequence in coord_sequence:

        for (cur_x, cur_y), (cand_x, cand_y) in itertools.pairwise(sequence):

            if cand_x == cur_x:
                coords.update(
                    (cand_x, y)
                    for y in range(min(cand_y, cur_y), max(cand_y, cur_y) + 1)
                )
            else:
                coords.update(
                    (x, cand_y)
                    for x in range(min(cand_x, cur_x), max(cand_x, cur_x) + 1)
                )

    return coords


def coord_from_comma(coord_s: str) -> tuple[int, int]:
    x, y = coord_s.split(",")

    return int(x), int(y)


def compute(input: str) -> int:
    rock_sequences = (
        [coord_from_comma(pair) for pair in line.split(" -> ")]
        for line in input.splitlines()
    )

    cave_map = place_rocks(rock_sequences)
    max_y = max(y for _, y in cave_map) + 1

    n_grains = 0
    while True:
        g_x, g_y = 500, 0
        while True:
            if (g_x, g_y) in cave_map:
                return n_grains
            elif g_y == max_y:
                cave_map.add((g_x, g_y))
                break
            elif (g_x, g_y + 1) not in cave_map:
                g_y += 1
            elif (g_x - 1, g_y + 1) not in cave_map:
                g_x -= 1
                g_y += 1
            elif (g_x + 1, g_y + 1) not in cave_map:
                g_x += 1
                g_y += 1
            else:
                cave_map.add((g_x, g_y))
                break

        n_grains += 1


TEST_INPUT = """
    498,4 -> 498,6 -> 496,6
    503,4 -> 502,4 -> 502,9 -> 494,9
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 93),),
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
