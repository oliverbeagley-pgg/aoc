import argparse
from functools import reduce
from operator import iadd
from pathlib import Path

import pytest

import aoc_utils

INPUT_TXT = Path(__file__).parent / "input.txt"


def search_for_finish(
    start: complex,
    nodes: dict[complex, int],
    edges: dict[complex, set[complex]],
) -> list[complex]:
    """Search for trail ends from a given start position.

    Return a list of end positions.
    """
    trail_finish = 9

    if nodes[start] == trail_finish:
        return [start]

    return reduce(
        iadd,
        (
            search_for_finish(next_position, nodes, edges)
            for next_position in edges[start]
            if nodes[next_position] == nodes[start] + 1
        ),
        [],
    )


def compute(puzzle_input: str) -> int:
    nodes = {
        col_idx + row_idx * 1j: int(height)
        for row_idx, line in enumerate(puzzle_input.splitlines())
        for col_idx, height in enumerate(line)
    }
    edges = {
        node: {node + x for x in (1, 1j, -1, -1j)} & nodes.keys() for node in nodes
    }

    trailheads = (node for node in nodes if nodes[node] == 0)
    paths = (search_for_finish(trailhead, nodes, edges) for trailhead in trailheads)

    return sum(len(ends) for ends in paths)


TEST_INPUT = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 81),
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
