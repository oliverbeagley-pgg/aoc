import argparse
from functools import cache
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(puzzle_input: str) -> int:
    graph = {
        root: child_s.split(" ")
        for root, child_s in (line.split(": ") for line in puzzle_input.splitlines())
    }

    visited = set()

    # Using cache to be lazy and not track if a node previously visited will result in a
    # valid path
    @cache
    def dfs(node: str, dest: str, skip: str | None = None) -> int:
        if node == dest:
            return 1
        # for cases where destination is not out
        if node == "out":
            return 0
        # do not allow transiting via skip node
        if skip is not None and node == skip:
            return 0
        # Prevent cycles
        if node in visited:
            return 0
        visited.add(node)
        return sum(dfs(child, dest, skip) for child in graph[node])

    visited.clear()
    segment_1 = dfs("svr", "fft", "dac")
    visited.clear()
    segment_2 = dfs("fft", "dac")
    visited.clear()
    segment_3 = dfs("dac", "out")

    visited.clear()
    segment_4 = dfs("svr", "dac", "fft")
    visited.clear()
    segment_5 = dfs("dac", "fft")
    visited.clear()
    segment_6 = dfs("fft", "out")

    return (segment_1 * segment_2 * segment_3) + (segment_4 * segment_5 * segment_6)


TEST_INPUT = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 2),
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
